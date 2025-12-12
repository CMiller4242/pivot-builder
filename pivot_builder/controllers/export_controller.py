"""Controller for export operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.services.export_service import ExportService


class ExportController:
    """Handles export operations for pivot results."""

    def __init__(self, app_controller):
        """
        Initialize export controller.

        Args:
            app_controller: Main application controller
        """
        self.app_controller = app_controller
        self.export_service = ExportService()

    def export_csv(self, path: str) -> bool:
        """
        Export current pivot to CSV file.

        Args:
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        # Check validation before export
        if not self._check_validation_for_export('pivot'):
            return False

        pivot_df = self._get_pivot_dataframe()
        if pivot_df is None:
            logger.error("No pivot data to export")
            return False

        return self.export_service.export_csv(pivot_df, path)

    def export_xlsx(self, path: str) -> bool:
        """
        Export current pivot to Excel (XLSX) file.

        Args:
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        # Check validation before export
        if not self._check_validation_for_export('pivot'):
            return False

        pivot_df = self._get_pivot_dataframe()
        if pivot_df is None:
            logger.error("No pivot data to export")
            return False

        return self.export_service.export_xlsx(pivot_df, path)

    def export_json(self, path: str) -> bool:
        """
        Export current pivot to JSON file.

        Args:
            path: File path to save to

        Returns:
            True if successful, False otherwise
        """
        # Check validation before export
        if not self._check_validation_for_export('pivot'):
            return False

        pivot_df = self._get_pivot_dataframe()
        if pivot_df is None:
            logger.error("No pivot data to export")
            return False

        return self.export_service.export_json(pivot_df, path)

    def _check_validation_for_export(self, export_type: str) -> bool:
        """
        Check validation before export and refresh if needed.

        Args:
            export_type: Type of export ('pivot' or 'combined')

        Returns:
            True if export can proceed, False if blocked
        """
        # Get validation controller
        if not hasattr(self.app_controller, 'validation_controller'):
            logger.warning("Validation controller not available, allowing export")
            return True

        validation_controller = self.app_controller.validation_controller
        if validation_controller is None:
            logger.warning("Validation controller is None, allowing export")
            return True

        # Refresh validation
        validation_controller.refresh()

        # Check for blocking errors
        has_errors = validation_controller.has_blocking_errors_for_export(export_type)

        if has_errors:
            logger.error(f"Export blocked due to validation errors for type: {export_type}")
            report = validation_controller.get_report()
            error_messages = [err.message for err in report.errors()]
            logger.error(f"Blocking errors: {error_messages}")

        return not has_errors

    def _get_pivot_dataframe(self):
        """
        Get the current pivot DataFrame from pivot controller.

        Returns:
            Pivot DataFrame or None if not available
        """
        if not hasattr(self.app_controller, 'pivot_controller'):
            logger.warning("Pivot controller not available")
            return None

        pivot_controller = self.app_controller.pivot_controller
        if pivot_controller is None:
            logger.warning("Pivot controller is None")
            return None

        pivot_df = pivot_controller.export_pivot()
        if pivot_df is None or len(pivot_df) == 0:
            logger.warning("Pivot DataFrame is empty or None")
            return None

        return pivot_df
