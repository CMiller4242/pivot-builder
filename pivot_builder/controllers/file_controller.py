"""Controller for file operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.services.file_service import FileService
from pivot_builder.services.sheet_detection_service import SheetDetectionService


class FileController:
    """Handles file-related operations and UI updates."""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.file_service = FileService()
        self.sheet_service = SheetDetectionService()
        self.view = None

    def set_view(self, view):
        """Set the view for this controller."""
        self.view = view

    def on_add_file(self):
        """Handle add file action."""
        pass

    def on_remove_file(self, file_path):
        """Handle remove file action."""
        pass

    def on_file_selected(self, file_path):
        """Handle file selection."""
        pass

    def on_sheet_selected(self, sheet_name):
        """Handle sheet selection."""
        pass

    def load_file(self, file_path):
        """Load a file."""
        pass
