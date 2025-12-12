"""Controller for column mapping operations."""

from typing import Dict, List, Optional

from pivot_builder.config.logging_config import logger
from pivot_builder.services.column_matching_service import ColumnMatchingService
from pivot_builder.services.column_normalization_service import ColumnNormalizationService
from pivot_builder.models.mapping_model import ColumnMappingModel, MappingRule


class MappingController:
    """Handles column mapping operations and UI updates."""

    def __init__(
        self,
        app_controller,
        normalization_service: ColumnNormalizationService,
        matching_service: ColumnMatchingService,
        mapping_model: ColumnMappingModel
    ):
        """
        Initialize mapping controller.

        Args:
            app_controller: Main application controller
            normalization_service: Service for normalizing column names
            matching_service: Service for matching columns across files
            mapping_model: Model holding current column mappings
        """
        self.app = app_controller
        self.normalization_service = normalization_service
        self.matching_service = matching_service
        self.mapping_model = mapping_model
        self.view = None

    def set_view(self, view):
        """
        Set the view for this controller.

        Args:
            view: The ColumnMappingView instance
        """
        self.view = view

    def rebuild_mapping_from_files(self):
        """
        Rebuild column mappings from all loaded files.

        This method:
        1. Gathers column names from all loaded FileDescriptors
        2. Calls matching service to build initial mapping
        3. Updates the mapping model
        4. Notifies view to refresh
        """
        logger.info("Rebuilding column mappings from loaded files")

        # Step 1: Gather column names from all loaded files
        files_columns = self._gather_files_columns()

        if not files_columns:
            logger.warning("No files with columns to map")
            self.mapping_model = ColumnMappingModel()
            if self.view:
                self.view.refresh_mapping(self.mapping_model)
            return

        # Step 2: Build initial mapping using matching service
        try:
            new_mapping = self.matching_service.build_initial_mapping(files_columns)
            self.mapping_model = new_mapping

            logger.info(
                f"Built mapping with {len(self.mapping_model.canonical_fields)} "
                f"canonical fields from {len(files_columns)} files"
            )

            # Step 3: Notify view to refresh
            if self.view:
                self.view.refresh_mapping(self.mapping_model)

        except Exception as e:
            logger.error(f"Error building mapping: {e}", exc_info=True)
            if self.view:
                self.view.show_error(f"Failed to build mapping: {str(e)}")

    def on_normalization_rule_changed(self, rule: MappingRule):
        """
        Handle changes to normalization rules.

        When user changes normalization settings (checkboxes),
        update the rule and rebuild mappings.

        Args:
            rule: The new MappingRule with updated settings
        """
        logger.info(f"Normalization rule changed: {rule}")

        # Update normalization service with new rule
        self.normalization_service.set_rule(rule)

        # Rebuild mappings with new rule
        self.rebuild_mapping_from_files()

    def on_manual_canonical_edit(
        self,
        file_id: str,
        original_column: str,
        new_canonical: Optional[str]
    ):
        """
        Handle manual edits to column mappings.

        When user manually changes a mapping in the grid,
        update the mapping model and refresh view.

        Args:
            file_id: ID of the file containing the column
            original_column: Original column name from the file
            new_canonical: New canonical field name (or None to unmap)
        """
        logger.info(
            f"Manual mapping edit: {file_id}:{original_column} -> {new_canonical}"
        )

        try:
            # Update the mapping model
            self.mapping_model.set_canonical_for(file_id, original_column, new_canonical)

            # Refresh view to show updated mapping
            if self.view:
                self.view.refresh_mapping(self.mapping_model)

        except Exception as e:
            logger.error(f"Error updating manual mapping: {e}", exc_info=True)
            if self.view:
                self.view.show_error(f"Failed to update mapping: {str(e)}")

    def get_current_mapping(self) -> ColumnMappingModel:
        """
        Get the current mapping model.

        Returns:
            Current ColumnMappingModel
        """
        return self.mapping_model

    def get_files_list(self) -> List:
        """
        Get list of loaded file descriptors.

        Returns:
            List of FileDescriptor objects with columns
        """
        if not self.app or not hasattr(self.app, 'files'):
            return []

        # Return only files that have DataFrames loaded
        return [
            fd for fd in self.app.files.values()
            if fd.has_dataframe and fd.dataframe is not None
        ]

    def _gather_files_columns(self) -> Dict[str, List[str]]:
        """
        Gather column names from all loaded files.

        Returns:
            Dict mapping file_id -> list of original column names
        """
        files_columns = {}

        if not self.app or not hasattr(self.app, 'files'):
            return files_columns

        # Get all file descriptors from files dictionary
        for file_desc in self.app.files.values():
            # Only include files that have DataFrames loaded
            if file_desc.dataframe is None:
                continue

            files_columns[file_desc.id] = list(file_desc.dataframe.columns)

        logger.debug(f"Gathered columns from {len(files_columns)} files")
        return files_columns

    def build_combined_dataset(self):
        """
        Build combined dataset from all loaded files using current mappings.

        This method:
        1. Gets all files with loaded DataFrames
        2. Calls dataset_builder_service to merge them using canonical mappings
        3. Stores result in app.combined_dataset
        4. Triggers preview refresh
        """
        logger.info("Building combined dataset from current mappings")

        try:
            # Get dataset builder service from app controller
            if not hasattr(self.app, 'dataset_builder_service'):
                logger.error("DatasetBuilderService not available in AppController")
                if self.view:
                    self.view.show_error("Dataset builder service not initialized")
                return

            # Get all loaded files
            files = self.get_files_list()

            if not files:
                logger.warning("No files with DataFrames to combine")
                if self.view:
                    self.view.show_error("No files loaded. Please add and load files first.")
                return

            # Build combined dataset
            combined_dataset = self.app.dataset_builder_service.build_combined_dataset(
                files,
                self.mapping_model
            )

            # Store in app controller
            self.app.combined_dataset = combined_dataset

            logger.info(
                f"Combined dataset built: {combined_dataset.get_row_count()} rows, "
                f"{len(combined_dataset.get_canonical_columns())} canonical columns"
            )

            # Refresh preview if available
            if self.app.preview_controller:
                self.app.preview_controller.refresh_combined_preview()

        except Exception as e:
            logger.error(f"Error building combined dataset: {e}", exc_info=True)
            if self.view:
                self.view.show_error(f"Failed to build combined dataset: {str(e)}")

    def export_mapping_config(self) -> dict:
        """
        Export current mapping configuration.

        Returns:
            Dictionary representation of current mapping
        """
        return {
            'mapping_rule': {
                'trim_whitespace': self.mapping_model.mapping_rule.trim_whitespace,
                'to_lower': self.mapping_model.mapping_rule.to_lower,
                'replace_spaces_with_underscore': self.mapping_model.mapping_rule.replace_spaces_with_underscore,
                'remove_special_chars': self.mapping_model.mapping_rule.remove_special_chars,
            },
            'canonical_fields': [
                {
                    'name': cf.name,
                    'dtype': cf.dtype,
                    'origin_files': list(cf.origin_files)
                }
                for cf in self.mapping_model.canonical_fields
            ],
            'file_mappings': {
                file_id: dict(mappings)
                for file_id, mappings in self.mapping_model.file_column_to_canonical.items()
            }
        }
