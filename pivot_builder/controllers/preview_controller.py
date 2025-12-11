"""Controller for data preview operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.services.dataset_builder_service import DatasetBuilderService


class PreviewController:
    """Handles data preview operations and UI updates."""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.dataset_service = DatasetBuilderService()
        self.view = None

    def set_view(self, view):
        """Set the view for this controller."""
        self.view = view

    def refresh_preview(self):
        """Refresh the data preview."""
        pass

    def on_filter_applied(self, filters):
        """Handle filter application."""
        pass

    def on_sort_applied(self, column, ascending):
        """Handle sorting."""
        pass

    def update_preview(self, dataframe):
        """Update preview with new dataframe."""
        pass
