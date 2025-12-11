"""Model for column mapping configuration."""


class MappingModel:
    """Manages column mapping between files."""

    def __init__(self):
        self.mappings = {}
        self.standard_columns = []
        self.file_columns = {}

    def add_mapping(self, standard_col, file_col, file_path):
        """Add a column mapping."""
        pass

    def remove_mapping(self, standard_col, file_path):
        """Remove a column mapping."""
        pass

    def get_mappings(self):
        """Get all mappings."""
        pass

    def set_standard_columns(self, columns):
        """Set the standard column definitions."""
        pass
