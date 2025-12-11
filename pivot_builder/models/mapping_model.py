"""Model for column mapping configuration."""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional


@dataclass
class MappingRule:
    """Rules for normalizing column names."""
    trim_whitespace: bool = True
    to_lower: bool = True
    replace_spaces_with_underscore: bool = True
    remove_special_chars: bool = True


@dataclass
class CanonicalField:
    """Represents a canonical field that columns from different files map to."""
    name: str
    dtype: Optional[str] = None
    origin_files: Set[str] = field(default_factory=set)

    def add_origin_file(self, file_id: str):
        """Add a file as an origin for this canonical field."""
        self.origin_files.add(file_id)

    def remove_origin_file(self, file_id: str):
        """Remove a file from origins."""
        if file_id in self.origin_files:
            self.origin_files.remove(file_id)


@dataclass
class ColumnMappingModel:
    """Model for managing column mappings across multiple files."""

    # For each file_id, maps original column name -> normalized name
    normalized_columns: Dict[str, Dict[str, str]] = field(default_factory=dict)

    # For each file_id, maps original column name -> canonical field name
    file_column_to_canonical: Dict[str, Dict[str, str]] = field(default_factory=dict)

    # List of canonical fields
    canonical_fields: List[CanonicalField] = field(default_factory=list)

    # Columns with no canonical mapping yet
    unmatched_columns: Dict[str, List[str]] = field(default_factory=dict)

    # Current normalization rules
    mapping_rule: MappingRule = field(default_factory=MappingRule)

    def get_canonical_for(self, file_id: str, column_name: str) -> Optional[str]:
        """
        Get the canonical field name for a given file's column.

        Args:
            file_id: ID of the file
            column_name: Original column name

        Returns:
            Canonical field name or None
        """
        if file_id in self.file_column_to_canonical:
            return self.file_column_to_canonical[file_id].get(column_name)
        return None

    def set_canonical_for(self, file_id: str, column_name: str, canonical_name: Optional[str]) -> None:
        """
        Set the canonical field name for a given file's column.

        Args:
            file_id: ID of the file
            column_name: Original column name
            canonical_name: Canonical field name (None to unmap)
        """
        if file_id not in self.file_column_to_canonical:
            self.file_column_to_canonical[file_id] = {}

        if canonical_name is None:
            # Remove mapping
            if column_name in self.file_column_to_canonical[file_id]:
                old_canonical = self.file_column_to_canonical[file_id][column_name]
                del self.file_column_to_canonical[file_id][column_name]

                # Remove file from canonical field's origins
                canonical_field = self.get_canonical_field(old_canonical)
                if canonical_field:
                    canonical_field.remove_origin_file(file_id)
        else:
            # Set mapping
            self.file_column_to_canonical[file_id][column_name] = canonical_name

            # Ensure canonical field exists
            canonical_field = self.get_canonical_field(canonical_name)
            if not canonical_field:
                canonical_field = CanonicalField(name=canonical_name)
                self.canonical_fields.append(canonical_field)

            # Add file to canonical field's origins
            canonical_field.add_origin_file(file_id)

    def get_all_canonical_names(self) -> List[str]:
        """Get list of all canonical field names."""
        return [field.name for field in self.canonical_fields]

    def get_canonical_field(self, canonical_name: str) -> Optional[CanonicalField]:
        """
        Get a CanonicalField by name.

        Args:
            canonical_name: Name of the canonical field

        Returns:
            CanonicalField or None
        """
        for field in self.canonical_fields:
            if field.name == canonical_name:
                return field
        return None

    def get_files_for_canonical(self, canonical_name: str) -> Set[str]:
        """
        Get all file IDs that map to a canonical field.

        Args:
            canonical_name: Name of the canonical field

        Returns:
            Set of file IDs
        """
        canonical_field = self.get_canonical_field(canonical_name)
        if canonical_field:
            return canonical_field.origin_files
        return set()

    def get_column_for_file_and_canonical(self, file_id: str, canonical_name: str) -> Optional[str]:
        """
        Get the original column name for a file that maps to a canonical field.

        Args:
            file_id: ID of the file
            canonical_name: Canonical field name

        Returns:
            Original column name or None
        """
        if file_id in self.file_column_to_canonical:
            for col, canonical in self.file_column_to_canonical[file_id].items():
                if canonical == canonical_name:
                    return col
        return None

    def clear(self):
        """Clear all mappings."""
        self.normalized_columns.clear()
        self.file_column_to_canonical.clear()
        self.canonical_fields.clear()
        self.unmatched_columns.clear()
