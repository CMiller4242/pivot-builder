"""Model for pivot table configuration."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PivotValueField:
    """
    Represents a value field in a pivot table with its aggregation function.

    Attributes:
        column: Name of the column to aggregate
        aggregation: Aggregation function (sum, count, mean, min, max)
    """
    column: str
    aggregation: str  # sum, count, mean, min, max

    def __post_init__(self):
        """Validate aggregation function."""
        valid_aggs = ['sum', 'count', 'mean', 'min', 'max']
        if self.aggregation not in valid_aggs:
            raise ValueError(f"Aggregation must be one of {valid_aggs}, got: {self.aggregation}")


@dataclass
class PivotConfig:
    """
    Complete configuration for a pivot table.

    Attributes:
        rows: List of column names to use as row dimensions
        columns: List of column names to use as column dimensions
        values: List of PivotValueField objects defining aggregations
        filters: Dict mapping column names to list of allowed values
    """
    rows: List[str] = field(default_factory=list)
    columns: List[str] = field(default_factory=list)
    values: List[PivotValueField] = field(default_factory=list)
    filters: Dict[str, List[str]] = field(default_factory=dict)

    def is_valid(self) -> bool:
        """
        Check if pivot configuration is valid.

        Returns:
            True if configuration has at least values defined
        """
        return len(self.values) > 0

    def add_row(self, column: str):
        """Add a column to rows."""
        if column not in self.rows:
            self.rows.append(column)

    def remove_row(self, column: str):
        """Remove a column from rows."""
        if column in self.rows:
            self.rows.remove(column)

    def add_column(self, column: str):
        """Add a column to columns."""
        if column not in self.columns:
            self.columns.append(column)

    def remove_column(self, column: str):
        """Remove a column from columns."""
        if column in self.columns:
            self.columns.remove(column)

    def add_value(self, column: str, aggregation: str):
        """Add a value field with aggregation."""
        value_field = PivotValueField(column, aggregation)
        self.values.append(value_field)

    def remove_value(self, index: int):
        """Remove a value field by index."""
        if 0 <= index < len(self.values):
            self.values.pop(index)

    def clear_all(self):
        """Clear all configuration."""
        self.rows.clear()
        self.columns.clear()
        self.values.clear()
        self.filters.clear()

    def to_dict(self) -> dict:
        """
        Serialize pivot configuration to dictionary.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            'rows': self.rows.copy(),
            'columns': self.columns.copy(),
            'values': [
                {'column': vf.column, 'aggregation': vf.aggregation}
                for vf in self.values
            ],
            'filters': {k: v.copy() for k, v in self.filters.items()}
        }

    @staticmethod
    def from_dict(data: dict) -> "PivotConfig":
        """
        Deserialize pivot configuration from dictionary.

        Args:
            data: Dictionary with configuration data

        Returns:
            PivotConfig instance
        """
        config = PivotConfig()
        config.rows = data.get('rows', []).copy()
        config.columns = data.get('columns', []).copy()

        # Deserialize value fields
        for vf_data in data.get('values', []):
            value_field = PivotValueField(
                column=vf_data['column'],
                aggregation=vf_data['aggregation']
            )
            config.values.append(value_field)

        # Deserialize filters
        config.filters = {
            k: v.copy() for k, v in data.get('filters', {}).items()
        }

        return config


class PivotModel:
    """Manages pivot table configuration (legacy wrapper)."""

    def __init__(self):
        self.row_fields = []
        self.column_fields = []
        self.value_fields = []
        self.aggregations = {}
        self.filters = {}

    def add_row_field(self, field):
        """Add a field to rows."""
        if field not in self.row_fields:
            self.row_fields.append(field)

    def add_column_field(self, field):
        """Add a field to columns."""
        if field not in self.column_fields:
            self.column_fields.append(field)

    def add_value_field(self, field, aggregation):
        """Add a field to values with aggregation."""
        if field not in self.value_fields:
            self.value_fields.append(field)
            self.aggregations[field] = aggregation

    def remove_field(self, field):
        """Remove a field from pivot."""
        if field in self.row_fields:
            self.row_fields.remove(field)
        if field in self.column_fields:
            self.column_fields.remove(field)
        if field in self.value_fields:
            self.value_fields.remove(field)
            self.aggregations.pop(field, None)

    def get_pivot_config(self):
        """Get the complete pivot configuration."""
        return {
            'rows': self.row_fields.copy(),
            'columns': self.column_fields.copy(),
            'values': self.value_fields.copy(),
            'aggregations': self.aggregations.copy(),
            'filters': self.filters.copy()
        }
