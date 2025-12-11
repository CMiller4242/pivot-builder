"""Service for file operations."""

import os
from pathlib import Path
from typing import Tuple, Optional, Dict, List

from pivot_builder.config.logging_config import logger
from pivot_builder.config.app_config import MAX_FILE_SIZE_MB

try:
    import pandas as pd
except ImportError:
    pd = None


class FileService:
    """Handles file loading and validation."""

    def __init__(self):
        if pd is None:
            logger.warning("pandas not available - file loading will be limited")

    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file format and size.

        Returns:
            (is_valid, error_message)
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            return False, f"File does not exist: {file_path}"

        # Check if it's a file (not directory)
        if not path.is_file():
            return False, f"Path is not a file: {file_path}"

        # Check file extension
        extension = path.suffix.lower()
        if extension not in ['.csv', '.xlsx', '.xls']:
            return False, f"Unsupported file type: {extension}. Only CSV and XLSX files are supported."

        # Check file size
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            return False, f"File too large: {file_size_mb:.1f}MB (max: {MAX_FILE_SIZE_MB}MB)"

        return True, None

    def load_csv_metadata(self, file_path: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Load CSV file metadata (header row).

        Returns:
            (metadata_dict, error_message)
        """
        if pd is None:
            return None, "pandas is not installed"

        try:
            # Read just the first row to get column names
            df = pd.read_csv(file_path, nrows=0, sep=None, engine='python')

            metadata = {
                'columns': list(df.columns),
                'num_columns': len(df.columns),
                'file_type': 'csv'
            }

            logger.info(f"Loaded CSV metadata from {file_path}: {metadata['num_columns']} columns")
            return metadata, None

        except Exception as e:
            error_msg = f"Failed to load CSV: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def load_xlsx_metadata(self, file_path: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Load XLSX file metadata (sheet names).

        Returns:
            (metadata_dict, error_message)
        """
        if pd is None:
            return None, "pandas is not installed"

        try:
            # Use ExcelFile to efficiently get sheet names without loading data
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names

            metadata = {
                'sheets': sheet_names,
                'num_sheets': len(sheet_names),
                'file_type': 'xlsx'
            }

            logger.info(f"Loaded XLSX metadata from {file_path}: {len(sheet_names)} sheets")
            return metadata, None

        except Exception as e:
            error_msg = f"Failed to load XLSX: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def load_file_metadata(self, file_path: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Load file metadata based on file type.

        Returns:
            (metadata_dict, error_message)
        """
        # First validate the file
        is_valid, error = self.validate_file(file_path)
        if not is_valid:
            return None, error

        # Determine file type and load metadata
        extension = Path(file_path).suffix.lower()

        if extension == '.csv':
            return self.load_csv_metadata(file_path)
        elif extension in ['.xlsx', '.xls']:
            return self.load_xlsx_metadata(file_path)
        else:
            return None, f"Unsupported file extension: {extension}"

    def get_file_type(self, file_path: str) -> str:
        """Get the file type based on extension."""
        extension = Path(file_path).suffix.lower()
        if extension == '.csv':
            return 'csv'
        elif extension in ['.xlsx', '.xls']:
            return 'xlsx'
        else:
            return 'unknown'
