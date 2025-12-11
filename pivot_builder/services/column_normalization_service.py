"""Service for normalizing column names."""

import re
from typing import List

from pivot_builder.config.logging_config import logger
from pivot_builder.models.mapping_model import MappingRule


class ColumnNormalizationService:
    """Normalizes column names across files according to configurable rules."""

    def __init__(self, rule: MappingRule = None):
        """
        Initialize normalization service.

        Args:
            rule: MappingRule to use for normalization (creates default if None)
        """
        self.rule = rule or MappingRule()

    def set_rule(self, rule: MappingRule):
        """Update the normalization rule."""
        self.rule = rule

    def normalize(self, name: str) -> str:
        """
        Normalize a column name according to the current rule.

        Args:
            name: Original column name

        Returns:
            Normalized column name
        """
        result = name

        # Apply trim whitespace
        if self.rule.trim_whitespace:
            result = result.strip()

        # Apply lowercase
        if self.rule.to_lower:
            result = result.lower()

        # Replace spaces with underscores
        if self.rule.replace_spaces_with_underscore:
            result = result.replace(' ', '_')

        # Remove special characters (keep only letters, digits, and underscores)
        if self.rule.remove_special_chars:
            result = re.sub(r'[^a-zA-Z0-9_]', '', result)

        return result

    def normalize_columns(self, columns: List[str]) -> List[str]:
        """
        Normalize a list of column names.

        Args:
            columns: List of original column names

        Returns:
            List of normalized column names
        """
        return [self.normalize(col) for col in columns]

    def normalize_column_name(self, column_name: str) -> str:
        """
        Normalize a single column name (alias for normalize).

        Args:
            column_name: Original column name

        Returns:
            Normalized column name
        """
        return self.normalize(column_name)

    def create_standard_name(self, column_name: str) -> str:
        """
        Create a standardized column name (uses default strict rules).

        Args:
            column_name: Original column name

        Returns:
            Standardized column name
        """
        # Always use strict normalization for standard names
        strict_rule = MappingRule(
            trim_whitespace=True,
            to_lower=True,
            replace_spaces_with_underscore=True,
            remove_special_chars=True
        )
        temp_service = ColumnNormalizationService(strict_rule)
        return temp_service.normalize(column_name)
