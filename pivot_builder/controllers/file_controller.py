"""Controller for file operations."""

from typing import List

from pivot_builder.config.logging_config import logger
from pivot_builder.config.app_config import SUPPORTED_FILE_TYPES
from pivot_builder.services.file_service import FileService
from pivot_builder.services.sheet_detection_service import SheetDetectionService
from pivot_builder.models.file_model import FileDescriptor, FileModel
from pivot_builder.widgets.dialog_widgets import DialogWidgets


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

    def on_add_files(self):
        """Handle add files action (opens file dialog)."""
        logger.info("Opening file dialog for adding files")

        # Open file dialog for multiple files
        file_paths = DialogWidgets.open_files_dialog(SUPPORTED_FILE_TYPES)

        if not file_paths:
            logger.info("No files selected")
            return

        # Process each selected file
        for file_path in file_paths:
            self.add_file(file_path)

    def add_file(self, file_path: str):
        """
        Add a single file to the application.

        Args:
            file_path: Path to the file to add
        """
        logger.info(f"Adding file: {file_path}")

        # Generate unique file ID
        file_id = FileModel.generate_file_id()

        # Detect file type
        file_type = self.file_service.get_file_type(file_path)

        # Create file descriptor
        descriptor = FileDescriptor(file_id, file_path, file_type)

        # Add to app controller (registers in model)
        self.app_controller.register_file(descriptor)

        # Load metadata based on file type
        self.load_file_metadata(descriptor)

        # Refresh UI
        self.refresh_file_list()

    def load_file_metadata(self, descriptor: FileDescriptor):
        """
        Load metadata for a file descriptor.

        Args:
            descriptor: FileDescriptor to populate with metadata
        """
        logger.info(f"Loading metadata for {descriptor.filename}")

        # Load metadata using file service
        metadata, error = self.file_service.load_file_metadata(str(descriptor.path))

        if error:
            # Set error status
            descriptor.set_error(error)
            logger.error(f"Failed to load {descriptor.filename}: {error}")
            return

        # Populate descriptor based on file type
        if descriptor.file_type == 'csv':
            descriptor.original_columns = metadata.get('columns', [])

            # For CSV, load DataFrame immediately
            df, df_error = self.file_service.load_csv_dataframe(str(descriptor.path))
            if df_error:
                descriptor.set_error(df_error)
                logger.error(f"Failed to load CSV DataFrame: {df_error}")
            else:
                descriptor.set_dataframe(df)
                descriptor.needs_sheet_selection = False
                descriptor.set_loaded()
                logger.info(f"CSV fully loaded: {descriptor.filename} with {len(df)} rows, {len(df.columns)} columns")

        elif descriptor.file_type == 'xlsx':
            descriptor.available_sheets = metadata.get('sheets', [])
            descriptor.set_loaded()
            logger.info(f"XLSX metadata loaded: {descriptor.filename} with {len(descriptor.available_sheets)} sheets")

    def on_remove_file(self, file_id: str):
        """
        Handle remove file action.

        Args:
            file_id: ID of the file to remove
        """
        logger.info(f"Removing file: {file_id}")

        # Remove from model
        self.app_controller.file_model.remove_file(file_id)

        # Refresh UI
        self.refresh_file_list()

    def on_file_selected(self, file_id: str):
        """
        Handle file selection.

        Args:
            file_id: ID of the selected file
        """
        logger.info(f"File selected: {file_id}")

        # Update selected file in model
        self.app_controller.file_model.select_file(file_id)

    def on_sheet_selected(self, file_id: str, sheet_name: str):
        """
        Handle sheet selection for XLSX files.
        Loads the DataFrame for the selected sheet.

        Args:
            file_id: ID of the file
            sheet_name: Name of the selected sheet
        """
        logger.info(f"Sheet selected: {sheet_name} for file {file_id}")

        # Get file descriptor
        descriptor = self.app_controller.file_model.get_file(file_id)
        if not descriptor:
            logger.error(f"File descriptor not found for ID: {file_id}")
            return

        # Update selected sheet
        descriptor.selected_sheet = sheet_name

        # Load DataFrame for the selected sheet
        df, error = self.file_service.load_xlsx_sheet(str(descriptor.path), sheet_name)

        if error:
            descriptor.set_error(error)
            logger.error(f"Failed to load sheet '{sheet_name}': {error}")
        else:
            descriptor.set_dataframe(df)
            descriptor.needs_sheet_selection = False
            descriptor.set_loaded()
            logger.info(f"XLSX sheet fully loaded: {descriptor.filename}[{sheet_name}] with {len(df)} rows, {len(df.columns)} columns")

        # Refresh UI to update the file item widget
        self.refresh_file_list()

    def refresh_file_list(self):
        """Refresh the file list in the UI."""
        if self.view:
            files = self.app_controller.file_model.get_all_files()
            self.view.refresh(files)
            logger.debug(f"Refreshed file list with {len(files)} files")
