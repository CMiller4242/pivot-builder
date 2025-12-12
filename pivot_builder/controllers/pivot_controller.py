"""Controller for pivot table operations."""

from typing import List, Dict, Optional
import pandas as pd

from pivot_builder.config.logging_config import logger
from pivot_builder.models.pivot_model import PivotConfig, PivotValueField
from pivot_builder.services.pivot_engine_service import PivotEngineService
from pivot_builder.services.pivot_config_service import PivotConfigService


class PivotController:
    """Handles pivot table operations and UI updates."""

    def __init__(self, app_controller, pivot_engine_service: PivotEngineService):
        """
        Initialize pivot controller.

        Args:
            app_controller: Main application controller
            pivot_engine_service: Service for building pivots
        """
        self.app = app_controller
        self.pivot_engine = pivot_engine_service
        self.config_service = PivotConfigService()
        self.view = None

        # Current pivot configuration
        self.config = PivotConfig()

        # Latest pivot result
        self.pivot_df = None

    def set_view(self, view):
        """Set the view for this controller."""
        self.view = view

    def update_rows(self, rows: List[str]):
        """
        Update row fields in pivot configuration.

        Args:
            rows: List of column names to use as rows
        """
        logger.info(f"Updating rows: {rows}")
        self.config.rows = rows.copy()

    def update_columns(self, columns: List[str]):
        """
        Update column fields in pivot configuration.

        Args:
            columns: List of column names to use as columns
        """
        logger.info(f"Updating columns: {columns}")
        self.config.columns = columns.copy()

    def update_values(self, values: List[PivotValueField]):
        """
        Update value fields in pivot configuration.

        Args:
            values: List of PivotValueField objects
        """
        logger.info(f"Updating values: {values}")
        self.config.values = values.copy()

    def update_filters(self, filters: Dict[str, List[str]]):
        """
        Update filters in pivot configuration.

        Args:
            filters: Dict mapping column names to allowed values
        """
        logger.info(f"Updating filters: {filters}")
        self.config.filters = filters.copy()

    def rebuild_pivot(self):
        """
        Rebuild the pivot table using current configuration.

        This method:
        1. Gets the combined dataset from app controller
        2. Calls pivot engine to build pivot
        3. Stores result
        4. Notifies view to refresh
        """
        logger.info("Rebuilding pivot table")

        try:
            # Get combined dataset
            if not hasattr(self.app, 'combined_dataset'):
                logger.error("No combined dataset available")
                if self.view:
                    self.view.show_error("No combined dataset. Please build combined dataset first.")
                return

            combined_dataset = self.app.combined_dataset

            if combined_dataset.df is None or len(combined_dataset.df) == 0:
                logger.warning("Combined dataset is empty")
                if self.view:
                    self.view.show_error("Combined dataset is empty. Please load files and build dataset.")
                return

            # Validate configuration
            if not self.config.is_valid():
                logger.warning("Pivot configuration invalid - no values defined")
                if self.view:
                    self.view.show_error("Please add at least one value field with aggregation.")
                return

            # Build pivot
            self.pivot_df = self.pivot_engine.build_pivot(combined_dataset.df, self.config)

            if self.pivot_df is not None and len(self.pivot_df) > 0:
                logger.info(f"Pivot rebuilt successfully: {self.pivot_df.shape}")

                # Notify view to refresh
                if self.view:
                    self.view.load_pivot_preview(self.pivot_df)
            else:
                logger.warning("Pivot result is empty")
                if self.view:
                    self.view.show_error("Pivot result is empty. Check configuration and data.")

        except Exception as e:
            logger.error(f"Error rebuilding pivot: {e}", exc_info=True)
            if self.view:
                self.view.show_error(f"Failed to build pivot: {str(e)}")

    def get_available_fields(self) -> List[str]:
        """
        Get list of available field names from combined dataset.

        Returns:
            List of column names, excluding metadata columns
        """
        if not hasattr(self.app, 'combined_dataset'):
            return []

        combined_dataset = self.app.combined_dataset

        if combined_dataset.df is None:
            return []

        # Get canonical columns (excludes __source_file etc.)
        return combined_dataset.get_canonical_columns()

    def add_row_field(self, field: str):
        """Add a field to rows."""
        self.config.add_row(field)
        logger.debug(f"Added row field: {field}")

    def remove_row_field(self, field: str):
        """Remove a field from rows."""
        self.config.remove_row(field)
        logger.debug(f"Removed row field: {field}")

    def add_column_field(self, field: str):
        """Add a field to columns."""
        self.config.add_column(field)
        logger.debug(f"Added column field: {field}")

    def remove_column_field(self, field: str):
        """Remove a field from columns."""
        self.config.remove_column(field)
        logger.debug(f"Removed column field: {field}")

    def add_value_field(self, column: str, aggregation: str):
        """Add a value field with aggregation."""
        self.config.add_value(column, aggregation)
        logger.debug(f"Added value field: {column} ({aggregation})")

    def remove_value_field(self, index: int):
        """Remove a value field by index."""
        if 0 <= index < len(self.config.values):
            removed = self.config.values[index]
            self.config.remove_value(index)
            logger.debug(f"Removed value field at index {index}: {removed}")

    def clear_configuration(self):
        """Clear all pivot configuration."""
        self.config.clear_all()
        self.pivot_df = None
        logger.info("Pivot configuration cleared")

    def export_pivot(self) -> Optional[pd.DataFrame]:
        """
        Export the current pivot DataFrame.

        Returns:
            Current pivot DataFrame or None
        """
        return self.pivot_df

    def save_config(self, path: str) -> bool:
        """
        Save current pivot configuration to JSON file.

        Args:
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Saving pivot configuration to {path}")
        success = self.config_service.save(self.config, path)

        if success:
            logger.info("Pivot configuration saved successfully")
        else:
            logger.error("Failed to save pivot configuration")
            if self.view:
                self.view.show_error("Failed to save configuration. Check logs for details.")

        return success

    def load_config(self, path: str) -> bool:
        """
        Load pivot configuration from JSON file.

        Args:
            path: File path to load from

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Loading pivot configuration from {path}")
        loaded_config = self.config_service.load(path)

        if loaded_config:
            self.config = loaded_config
            logger.info("Pivot configuration loaded successfully")

            # Refresh view to show loaded configuration
            if self.view:
                self.view.refresh_available_fields()

            return True
        else:
            logger.error("Failed to load pivot configuration")
            if self.view:
                self.view.show_error("Failed to load configuration. Check file format and logs.")
            return False
