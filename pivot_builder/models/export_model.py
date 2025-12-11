"""Model for export configuration."""


class ExportModel:
    """Manages export configuration and settings."""

    def __init__(self):
        self.export_format = "xlsx"
        self.export_path = None
        self.include_metadata = False
        self.export_options = {}

    def set_format(self, format_type):
        """Set export format."""
        pass

    def set_path(self, path):
        """Set export path."""
        pass

    def set_options(self, options):
        """Set export options."""
        pass

    def get_config(self):
        """Get export configuration."""
        pass
