"""Model for pivot table configuration."""


class PivotModel:
    """Manages pivot table configuration."""

    def __init__(self):
        self.row_fields = []
        self.column_fields = []
        self.value_fields = []
        self.aggregations = {}
        self.filters = {}

    def add_row_field(self, field):
        """Add a field to rows."""
        pass

    def add_column_field(self, field):
        """Add a field to columns."""
        pass

    def add_value_field(self, field, aggregation):
        """Add a field to values with aggregation."""
        pass

    def remove_field(self, field):
        """Remove a field from pivot."""
        pass

    def get_pivot_config(self):
        """Get the complete pivot configuration."""
        pass
