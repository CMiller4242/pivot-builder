"""Model for file management."""


class FileModel:
    """Manages the list of loaded files."""

    def __init__(self):
        self.files = []
        self.selected_file = None

    def add_file(self, file_path):
        """Add a file to the model."""
        pass

    def remove_file(self, file_path):
        """Remove a file from the model."""
        pass

    def get_files(self):
        """Get all files."""
        pass

    def select_file(self, file_path):
        """Select a file."""
        pass
