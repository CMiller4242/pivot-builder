"""Controller for export operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.services.export_service import ExportService


class ExportController:
    """Handles export operations."""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.export_service = ExportService()

    def on_export(self, format_type, file_path):
        """Handle export action."""
        pass

    def export_to_excel(self, file_path):
        """Export to Excel format."""
        pass

    def export_to_csv(self, file_path):
        """Export to CSV format."""
        pass

    def validate_export_path(self, file_path):
        """Validate export path."""
        pass
