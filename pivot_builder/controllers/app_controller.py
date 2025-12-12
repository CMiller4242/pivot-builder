"""Main application controller."""

from pivot_builder.config.logging_config import logger
from pivot_builder.models.file_model import FileModel
from pivot_builder.models.dataset_model import DatasetModel, CombinedDataset
from pivot_builder.models.mapping_model import ColumnMappingModel, MappingRule
from pivot_builder.models.pivot_model import PivotModel
from pivot_builder.models.validation_model import ValidationModel
from pivot_builder.models.export_model import ExportModel
from pivot_builder.services.column_normalization_service import ColumnNormalizationService
from pivot_builder.services.column_matching_service import ColumnMatchingService
from pivot_builder.services.dataset_builder_service import DatasetBuilderService
from pivot_builder.services.pivot_engine_service import PivotEngineService


class AppController:
    """Main application controller coordinating all sub-controllers."""

    def __init__(self):
        # Initialize models
        self.file_model = FileModel()
        self.dataset_model = DatasetModel()

        # Initialize mapping services and model
        self.mapping_rule = MappingRule()  # Default normalization rule
        self.column_normalization_service = ColumnNormalizationService(self.mapping_rule)
        self.column_matching_service = ColumnMatchingService(self.column_normalization_service)
        self.column_mapping_model = ColumnMappingModel()

        # Initialize dataset builder service and combined dataset
        self.dataset_builder_service = DatasetBuilderService()
        self.combined_dataset = CombinedDataset()

        # Initialize pivot engine service
        self.pivot_engine_service = PivotEngineService()

        # Other models
        self.pivot_model = PivotModel()
        self.validation_model = ValidationModel()
        self.export_model = ExportModel()

        # Sub-controllers will be initialized later
        self.file_controller = None
        self.mapping_controller = None
        self.preview_controller = None
        self.pivot_controller = None
        self.export_controller = None

    @property
    def files(self):
        """Convenience property to access files dictionary directly."""
        return self.file_model.files

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

    def on_request_file_preview(self, file_id: str):
        """
        Handle file preview request.

        Args:
            file_id: ID of the file to preview
        """
        logger.info(f"Preview requested for file ID: {file_id}")

        if self.preview_controller:
            # Show preview for the file
            self.preview_controller.show_preview_for(file_id)

            # Switch to preview tab (will be implemented in main_window)
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.show_preview_tab()
        else:
            logger.warning("Preview controller not initialized")

    def set_main_window(self, main_window):
        """Set reference to main window for tab switching."""
        self.main_window = main_window

    def refresh_all(self):
        """Refresh all views."""
        if self.file_controller:
            self.file_controller.refresh_file_list()

        if self.preview_controller:
            self.preview_controller.refresh_preview()
