"""Service for data type detection and conversion."""

from pivot_builder.config.logging_config import logger


class DtypeService:
    """Handles data type detection and conversion."""

    def __init__(self):
        pass

    def detect_column_types(self, dataframe):
        """Detect data types for all columns."""
        pass

    def convert_column_type(self, dataframe, column, target_type):
        """Convert a column to target type."""
        pass

    def suggest_types(self, dataframe):
        """Suggest optimal data types."""
        pass
