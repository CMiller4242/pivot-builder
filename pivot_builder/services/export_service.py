"""Service for exporting data to various formats."""

import pandas as pd
from typing import Optional

from pivot_builder.config.logging_config import logger


class ExportService:
    """Service for exporting DataFrames to CSV, XLSX, and JSON formats."""

    def export_csv(self, df: pd.DataFrame, path: str) -> bool:
        """
        Export DataFrame to CSV file.

        Args:
            df: DataFrame to export
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_csv(path, index=False)
            logger.info(f"Exported data to CSV: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False

    def export_xlsx(self, df: pd.DataFrame, path: str) -> bool:
        """
        Export DataFrame to Excel (XLSX) file.

        Args:
            df: DataFrame to export
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_excel(path, index=False, engine='openpyxl')
            logger.info(f"Exported data to XLSX: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export XLSX: {e}")
            return False

    def export_json(self, df: pd.DataFrame, path: str, orient: str = 'records') -> bool:
        """
        Export DataFrame to JSON file.

        Args:
            df: DataFrame to export
            path: File path to save to
            orient: JSON orientation (records, index, columns, values, table)

        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_json(path, orient=orient, indent=2)
            logger.info(f"Exported data to JSON: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export JSON: {e}")
            return False
