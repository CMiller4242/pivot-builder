"""Model for file management."""

from pathlib import Path
from typing import Optional, List
import uuid


class FileDescriptor:
    """Descriptor for a loaded file with metadata."""

    def __init__(self, file_id: str, path: str, file_type: str):
        self.id = file_id
        self.path = Path(path)
        self.file_type = file_type  # "csv" or "xlsx"
        self.available_sheets = []  # When XLSX
        self.selected_sheet = None
        self.original_columns = []  # For CSV header preview
        self.status = "pending"     # pending | loaded | error
        self.error_message = None

        # DataFrame and preview
        self.dataframe = None  # The full pandas DataFrame
        self.preview_rows = None  # Cached preview (head N rows)
        self.needs_sheet_selection = (file_type == "xlsx")  # XLSX needs sheet selection

    @property
    def filename(self) -> str:
        """Get the filename without path."""
        return self.path.name

    @property
    def extension(self) -> str:
        """Get the file extension."""
        return self.path.suffix

    @property
    def has_dataframe(self) -> bool:
        """Check if DataFrame is loaded."""
        return self.dataframe is not None

    def set_error(self, message: str):
        """Set error status with message."""
        self.status = "error"
        self.error_message = message

    def set_loaded(self):
        """Set loaded status."""
        self.status = "loaded"
        self.error_message = None

    def set_dataframe(self, df):
        """
        Set the DataFrame for this file.

        Args:
            df: pandas DataFrame
        """
        self.dataframe = df
        if df is not None:
            self.original_columns = list(df.columns)
            self.generate_preview()

    def generate_preview(self, n_rows: int = 50):
        """
        Generate a preview of the first N rows.

        Args:
            n_rows: Number of rows to include in preview
        """
        if self.dataframe is not None:
            self.preview_rows = self.dataframe.head(n_rows)


class FileModel:
    """Manages the list of loaded files."""

    def __init__(self):
        self.files = {}  # Dict[str, FileDescriptor] - keyed by file_id
        self.selected_file_id = None

    def add_file(self, descriptor: FileDescriptor):
        """Add a file descriptor to the model."""
        self.files[descriptor.id] = descriptor

    def remove_file(self, file_id: str):
        """Remove a file from the model."""
        if file_id in self.files:
            del self.files[file_id]
            if self.selected_file_id == file_id:
                self.selected_file_id = None

    def get_file(self, file_id: str) -> Optional[FileDescriptor]:
        """Get a specific file descriptor by ID."""
        return self.files.get(file_id)

    def get_all_files(self) -> List[FileDescriptor]:
        """Get all file descriptors."""
        return list(self.files.values())

    def select_file(self, file_id: str):
        """Select a file by ID."""
        if file_id in self.files:
            self.selected_file_id = file_id

    def get_selected_file(self) -> Optional[FileDescriptor]:
        """Get the currently selected file descriptor."""
        if self.selected_file_id:
            return self.files.get(self.selected_file_id)
        return None

    @staticmethod
    def generate_file_id() -> str:
        """Generate a unique file ID."""
        return str(uuid.uuid4())
