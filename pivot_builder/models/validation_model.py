"""Model for validation results."""


class ValidationModel:
    """Manages validation results and errors."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.validation_status = None

    def add_error(self, error_msg):
        """Add a validation error."""
        pass

    def add_warning(self, warning_msg):
        """Add a validation warning."""
        pass

    def clear_results(self):
        """Clear all validation results."""
        pass

    def get_errors(self):
        """Get all errors."""
        pass

    def get_warnings(self):
        """Get all warnings."""
        pass

    def is_valid(self):
        """Check if validation passed."""
        pass
