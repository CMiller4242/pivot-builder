"""Service for detecting sheets in Excel files."""

from typing import List, Optional, Tuple
from pathlib import Path

from pivot_builder.config.logging_config import logger

try:
    import pandas as pd
except ImportError:
    pd = None


class SheetDetectionService:
    """Detects and lists sheets in Excel files."""

    def __init__(self):
        if pd is None:
            logger.warning("pandas not available - sheet detection will be limited")

    def detect_sheets(self, file_path: str) -> Tuple[Optional[List[str]], Optional[str]]:
        """
        Detect all sheets in an Excel file.

        Returns:
            (sheet_names_list, error_message)
        """
        if pd is None:
            return None, "pandas is not installed"

        try:
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            logger.info(f"Detected {len(sheet_names)} sheets in {file_path}")
            return sheet_names, None
        except Exception as e:
            error_msg = f"Failed to detect sheets: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def get_sheet_names(self, file_path: str) -> List[str]:
        """
        Get list of sheet names.

        Returns:
            List of sheet names (empty list on error)
        """
        sheet_names, error = self.detect_sheets(file_path)
        if error:
            logger.error(f"Error getting sheet names: {error}")
            return []
        return sheet_names or []

    def load_sheet(self, file_path: str, sheet_name: str) -> Tuple[Optional[object], Optional[str]]:
        """
        Load a specific sheet (returns DataFrame).

        Returns:
            (dataframe, error_message)
        """
        if pd is None:
            return None, "pandas is not installed"

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded sheet '{sheet_name}' from {file_path}: {len(df)} rows, {len(df.columns)} columns")
            return df, None
        except Exception as e:
            error_msg = f"Failed to load sheet '{sheet_name}': {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def populate_file_descriptor_sheets(self, file_descriptor):
        """
        Populate a FileDescriptor's available_sheets list for XLSX files.

        Args:
            file_descriptor: FileDescriptor instance to populate
        """
        if file_descriptor.file_type != 'xlsx':
            logger.debug(f"Skipping sheet detection for non-XLSX file: {file_descriptor.filename}")
            return

        sheet_names, error = self.detect_sheets(str(file_descriptor.path))

        if error:
            file_descriptor.set_error(error)
        else:
            file_descriptor.available_sheets = sheet_names
            logger.info(f"Populated {len(sheet_names)} sheets for {file_descriptor.filename}")
