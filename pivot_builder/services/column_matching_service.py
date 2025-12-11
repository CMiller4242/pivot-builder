"""Service for matching columns across files."""

from typing import Dict, List
from collections import defaultdict

from pivot_builder.config.logging_config import logger
from pivot_builder.models.mapping_model import ColumnMappingModel, CanonicalField
from pivot_builder.services.column_normalization_service import ColumnNormalizationService


class ColumnMatchingService:
    """Matches columns across multiple files based on normalized names."""

    def __init__(self, normalization_service: ColumnNormalizationService):
        """
        Initialize column matching service.

        Args:
            normalization_service: Service for normalizing column names
        """
        self.normalization_service = normalization_service

    def build_initial_mapping(
        self,
        files_columns: Dict[str, List[str]]  # file_id -> original column names
    ) -> ColumnMappingModel:
        """
        Build initial column mappings across files.

        Logic:
        1. Normalize each column name
        2. Group columns by normalized name
        3. Create canonical fields for each group
        4. Map original columns to canonical fields

        Args:
            files_columns: Dict mapping file_id to list of original column names

        Returns:
            ColumnMappingModel with initial mappings
        """
        logger.info(f"Building initial mapping for {len(files_columns)} files")

        # Create new mapping model
        mapping_model = ColumnMappingModel()
        mapping_model.mapping_rule = self.normalization_service.rule

        # Track: normalized_name -> [(file_id, original_column), ...]
        normalized_to_origins = defaultdict(list)

        # Step 1: Normalize all columns and track origins
        for file_id, columns in files_columns.items():
            mapping_model.normalized_columns[file_id] = {}
            mapping_model.file_column_to_canonical[file_id] = {}

            for original_col in columns:
                normalized = self.normalization_service.normalize(original_col)
                mapping_model.normalized_columns[file_id][original_col] = normalized
                normalized_to_origins[normalized].append((file_id, original_col))

        # Step 2: Create canonical fields for each normalized name
        for normalized_name, origins in normalized_to_origins.items():
            # Create canonical field
            canonical_field = CanonicalField(name=normalized_name)

            # Add all origin files
            for file_id, original_col in origins:
                canonical_field.add_origin_file(file_id)
                # Map original column to canonical field
                mapping_model.file_column_to_canonical[file_id][original_col] = normalized_name

            # Add to canonical fields list
            mapping_model.canonical_fields.append(canonical_field)

        logger.info(f"Created {len(mapping_model.canonical_fields)} canonical fields")

        return mapping_model

    def find_matches(self, source_columns: List[str], target_columns: List[str]) -> Dict[str, str]:
        """
        Find matching columns between two sets based on normalized names.

        Args:
            source_columns: List of source column names
            target_columns: List of target column names

        Returns:
            Dict mapping source columns to matching target columns
        """
        matches = {}

        # Normalize all target columns
        target_normalized = {
            self.normalization_service.normalize(col): col
            for col in target_columns
        }

        # Find matches for source columns
        for source_col in source_columns:
            source_norm = self.normalization_service.normalize(source_col)
            if source_norm in target_normalized:
                matches[source_col] = target_normalized[source_norm]

        return matches

    def calculate_similarity(self, col1: str, col2: str) -> float:
        """
        Calculate similarity score between two column names.

        For now, uses exact match on normalized names (returns 1.0 or 0.0).
        Can be enhanced with fuzzy matching in the future.

        Args:
            col1: First column name
            col2: Second column name

        Returns:
            Similarity score (1.0 for exact match, 0.0 otherwise)
        """
        norm1 = self.normalization_service.normalize(col1)
        norm2 = self.normalization_service.normalize(col2)

        return 1.0 if norm1 == norm2 else 0.0

    def suggest_mappings(self, files_columns: Dict[str, List[str]]) -> Dict[str, Dict[str, str]]:
        """
        Suggest column mappings for multiple files.

        Args:
            files_columns: Dict mapping file_id to list of column names

        Returns:
            Dict mapping file_id -> (original_column -> suggested_canonical)
        """
        mapping_model = self.build_initial_mapping(files_columns)

        # Convert to suggestion format
        suggestions = {}
        for file_id in files_columns.keys():
            if file_id in mapping_model.file_column_to_canonical:
                suggestions[file_id] = mapping_model.file_column_to_canonical[file_id].copy()

        return suggestions
