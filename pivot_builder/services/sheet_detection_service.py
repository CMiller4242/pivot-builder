"""Service for detecting sheets in Excel files."""

from pivot_builder.config.logging_config import logger


class SheetDetectionService:
    """Detects and lists sheets in Excel files."""

    def __init__(self):
        pass

    def detect_sheets(self, file_path):
        """Detect all sheets in an Excel file."""
        pass

    def get_sheet_names(self, file_path):
        """Get list of sheet names."""
        pass

    def load_sheet(self, file_path, sheet_name):
        """Load a specific sheet."""
        pass
