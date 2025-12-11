"""Service for exporting results."""

from pivot_builder.config.logging_config import logger


class ExportService:
    """Handles exporting pivot tables to various formats."""

    def __init__(self):
        pass

    def export_to_excel(self, dataframe, file_path):
        """Export dataframe to Excel."""
        pass

    def export_to_csv(self, dataframe, file_path):
        """Export dataframe to CSV."""
        pass

    def export_with_metadata(self, dataframe, metadata, file_path):
        """Export dataframe with metadata."""
        pass
