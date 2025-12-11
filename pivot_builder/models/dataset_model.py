"""Model for dataset management."""


class DatasetModel:
    """Manages the combined dataset from multiple sources."""

    def __init__(self):
        self.dataframe = None
        self.source_files = []
        self.column_metadata = {}

    def set_dataframe(self, df):
        """Set the main dataframe."""
        pass

    def get_dataframe(self):
        """Get the main dataframe."""
        pass

    def get_columns(self):
        """Get list of column names."""
        pass

    def get_column_dtypes(self):
        """Get column data types."""
        pass
