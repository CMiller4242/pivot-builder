"""Model for dataset management."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PerFileDataset:
    """
    Represents a single file's dataset contribution to the combined dataset.

    Attributes:
        file_id: Unique identifier for the file
        df: The pandas DataFrame for this file (after mapping applied)
        column_mapping: Mapping from original column names to canonical names
        effective_columns: List of canonical field names included from this file
    """
    file_id: str
    df: object = None  # pandas DataFrame
    column_mapping: Dict[str, str] = field(default_factory=dict)  # original → canonical
    effective_columns: List[str] = field(default_factory=list)  # canonical fields included


@dataclass
class CombinedDataset:
    """
    Represents the combined dataset from all files.

    Attributes:
        df: The merged pandas DataFrame with aligned canonical columns
        source_metadata: List of PerFileDataset objects tracking per-file contributions
    """
    df: object = None  # pandas DataFrame
    source_metadata: List[PerFileDataset] = field(default_factory=list)

    def get_canonical_columns(self) -> List[str]:
        """
        Get list of canonical column names in the combined dataset.

        Returns:
            List of column names (excluding metadata columns like __source_file)
        """
        if self.df is None:
            return []

        # Filter out metadata columns
        return [col for col in self.df.columns if not col.startswith('__')]

    def get_row_count(self) -> int:
        """
        Get total number of rows in the combined dataset.

        Returns:
            Number of rows
        """
        if self.df is None:
            return 0
        return len(self.df)

    def get_file_count(self) -> int:
        """
        Get number of source files in the combined dataset.

        Returns:
            Number of source files
        """
        return len(self.source_metadata)


class DatasetModel:
    """Manages the combined dataset from multiple sources."""

    def __init__(self):
        self.dataframe = None
        self.source_files = []
        self.column_metadata = {}

    def set_dataframe(self, df):
        """Set the main dataframe."""
        self.dataframe = df

    def get_dataframe(self):
        """Get the main dataframe."""
        return self.dataframe

    def get_columns(self):
        """Get list of column names."""
        if self.dataframe is not None:
            return list(self.dataframe.columns)
        return []

    def get_column_dtypes(self):
        """Get column data types."""
        if self.dataframe is not None:
            return dict(self.dataframe.dtypes)
        return {}
