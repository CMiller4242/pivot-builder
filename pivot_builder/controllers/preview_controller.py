"""Controller for data preview operations."""

from typing import Optional

from pivot_builder.config.logging_config import logger
from pivot_builder.config.app_config import DEFAULT_PREVIEW_ROWS
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
        """Refresh the data preview by updating the file list."""
        if self.view:
            files = self.app_controller.file_model.get_all_files()
            self.view.refresh_file_list(files)
            logger.debug(f"Refreshed preview file list with {len(files)} files")

    def show_preview_for(self, file_id: str):
        """
        Show preview for a specific file.

        Args:
            file_id: ID of the file to preview
        """
        logger.info(f"Showing preview for file ID: {file_id}")

        # Get file descriptor
        file_descriptor = self.app_controller.file_model.get_file(file_id)

        if not file_descriptor:
            logger.error(f"File descriptor not found for ID: {file_id}")
            if self.view:
                self.view.show_preview(None)
            return

        # Show the preview
        if self.view:
            self.view.show_preview(file_descriptor)

    def get_preview_for_file(self, file_id: str, n_rows: int = None):
        """
        Get preview data for a specific file.

        Args:
            file_id: ID of the file
            n_rows: Number of rows to preview (defaults to config value)

        Returns:
            Preview DataFrame or None
        """
        if n_rows is None:
            n_rows = DEFAULT_PREVIEW_ROWS

        file_descriptor = self.app_controller.file_model.get_file(file_id)

        if not file_descriptor:
            logger.error(f"File descriptor not found for ID: {file_id}")
            return None

        if not file_descriptor.has_dataframe:
            logger.warning(f"No dataframe loaded for file: {file_descriptor.filename}")
            return None

        # Return cached preview or generate new one
        if file_descriptor.preview_rows is not None:
            return file_descriptor.preview_rows
        else:
            file_descriptor.generate_preview(n_rows)
            return file_descriptor.preview_rows

    def on_filter_applied(self, filters):
        """Handle filter application (placeholder for future)."""
        logger.info(f"Filter applied: {filters}")

    def on_sort_applied(self, column, ascending):
        """Handle sorting (placeholder for future)."""
        logger.info(f"Sort applied: column={column}, ascending={ascending}")

    def update_preview(self, dataframe):
        """Update preview with new dataframe (placeholder for future)."""
        logger.info("Preview updated with new dataframe")
