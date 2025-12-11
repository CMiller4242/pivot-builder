"""Controller for pivot table operations."""

from pivot_builder.config.logging_config import logger
from pivot_builder.services.pivot_service import PivotService


class PivotController:
    """Handles pivot table operations and UI updates."""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.pivot_service = PivotService()
        self.view = None

    def set_view(self, view):
        """Set the view for this controller."""
        self.view = view

    def on_field_added_to_rows(self, field):
        """Handle field added to rows."""
        pass

    def on_field_added_to_columns(self, field):
        """Handle field added to columns."""
        pass

    def on_field_added_to_values(self, field, aggregation):
        """Handle field added to values."""
        pass

    def on_field_removed(self, field):
        """Handle field removal."""
        pass

    def on_build_pivot(self):
        """Handle pivot table build."""
        pass

    def refresh_pivot(self):
        """Refresh pivot table."""
        pass
