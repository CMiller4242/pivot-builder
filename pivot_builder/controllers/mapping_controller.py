"""Controller for column mapping operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.services.column_matching_service import ColumnMatchingService
from pivot_builder.services.column_normalization_service import ColumnNormalizationService


class MappingController:
    """Handles column mapping operations and UI updates."""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.matching_service = ColumnMatchingService()
        self.normalization_service = ColumnNormalizationService()
        self.view = None

    def set_view(self, view):
        """Set the view for this controller."""
        self.view = view

    def on_column_mapped(self, standard_col, file_col):
        """Handle column mapping."""
        pass

    def on_mapping_removed(self, standard_col):
        """Handle mapping removal."""
        pass

    def on_auto_map(self):
        """Handle automatic mapping."""
        pass

    def refresh_mappings(self):
        """Refresh mapping view."""
        pass
