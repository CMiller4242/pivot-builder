"""Controller for validation operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.models.validation_model import ValidationReport
from pivot_builder.services.validation_service import ValidationService


class ValidationController:
    """Handles validation operations and UI updates."""

    def __init__(self, app_controller):
        """
        Initialize validation controller.

        Args:
            app_controller: Main application controller
        """
        self.app = app_controller
        self.validation_service = ValidationService()
        self.view = None

        # Latest validation report
        self.report = ValidationReport()

    def set_view(self, view):
        """Set the view for this controller."""
        self.view = view

    def refresh(self):
        """
        Run validation checks and update view.

        This should be called whenever:
        - Files are added/loaded/sheet selected
        - Mapping is rebuilt
        - Combined dataset is rebuilt
        - Pivot config changes / pivot is rebuilt
        - Export is attempted
        """
        logger.info("Running validation checks")

        # Run all validation checks
        self.report = self.validation_service.validate_all(self.app)

        # Update view if available
        if self.view:
            self.view.refresh_report(self.report)

        return self.report

    def get_report(self) -> ValidationReport:
        """
        Get the latest validation report.

        Returns:
            Current ValidationReport
        """
        return self.report

    def has_blocking_errors_for_export(self, export_type: str = None) -> bool:
        """
        Check if there are blocking errors for export.

        Args:
            export_type: Type of export (e.g., 'pivot', 'combined')

        Returns:
            True if export should be blocked
        """
        # Check for critical errors
        errors = self.report.errors()

        if export_type == 'pivot':
            # Block if no pivot data
            pivot_error_codes = ['NO_PIVOT_VALUES', 'PIVOT_NOT_BUILT']
            if any(err.code in pivot_error_codes for err in errors):
                return True

        elif export_type == 'combined':
            # Block if no combined dataset
            combined_error_codes = ['NO_COMBINED_DATASET', 'COMBINED_DATASET_EMPTY']
            if any(err.code in combined_error_codes for err in errors):
                return True

        # Block on any critical errors
        critical_codes = ['NO_FILES_LOADED', 'NO_FILES']
        if any(err.code in critical_codes for err in errors):
            return True

        return False
