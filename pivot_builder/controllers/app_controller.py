"""Main application controller."""

from pivot_builder.config.logging_config import logger
from pivot_builder.models.file_model import FileModel
from pivot_builder.models.dataset_model import DatasetModel
from pivot_builder.models.mapping_model import MappingModel
from pivot_builder.models.pivot_model import PivotModel
from pivot_builder.models.validation_model import ValidationModel
from pivot_builder.models.export_model import ExportModel


class AppController:
    """Main application controller coordinating all sub-controllers."""

    def __init__(self):
        # Initialize models
        self.file_model = FileModel()
        self.dataset_model = DatasetModel()
        self.mapping_model = MappingModel()
        self.pivot_model = PivotModel()
        self.validation_model = ValidationModel()
        self.export_model = ExportModel()

        # Sub-controllers will be initialized later
        self.file_controller = None
        self.mapping_controller = None
        self.preview_controller = None
        self.pivot_controller = None
        self.export_controller = None

    def set_file_controller(self, controller):
        """Set the file controller."""
        self.file_controller = controller

    def set_mapping_controller(self, controller):
        """Set the mapping controller."""
        self.mapping_controller = controller

    def set_preview_controller(self, controller):
        """Set the preview controller."""
        self.preview_controller = controller

    def set_pivot_controller(self, controller):
        """Set the pivot controller."""
        self.pivot_controller = controller

    def set_export_controller(self, controller):
        """Set the export controller."""
        self.export_controller = controller

    def register_file(self, file_descriptor):
        """
        Register a file descriptor in the file model.

        Args:
            file_descriptor: FileDescriptor instance to register
        """
        self.file_model.add_file(file_descriptor)
        logger.info(f"Registered file: {file_descriptor.filename} (ID: {file_descriptor.id})")

    def on_add_files(self):
        """Handle add files action (delegates to file controller)."""
        if self.file_controller:
            self.file_controller.on_add_files()
        else:
            logger.warning("File controller not initialized")

    def refresh_all(self):
        """Refresh all views."""
        if self.file_controller:
            self.file_controller.refresh_file_list()
