"""Service for building combined datasets."""

from typing import Dict, List, Optional
import pandas as pd

from pivot_builder.config.logging_config import logger
from pivot_builder.models.file_model import FileDescriptor
from pivot_builder.models.mapping_model import ColumnMappingModel
from pivot_builder.models.dataset_model import CombinedDataset, PerFileDataset


class DatasetBuilderService:
    """Builds combined datasets from multiple sources."""

    def __init__(self):
        pass

    def build_combined_dataset(
        self,
        files: List[FileDescriptor],
        mapping_model: ColumnMappingModel,
        include_source_tracking: bool = True
    ) -> CombinedDataset:
        """
        Build a combined dataset from multiple files using canonical mappings.

        Args:
            files: List of FileDescriptor objects with loaded DataFrames
            mapping_model: ColumnMappingModel with canonical field mappings
            include_source_tracking: Whether to add __source_file column

        Returns:
            CombinedDataset with merged DataFrame and metadata
        """
        logger.info(f"Building combined dataset from {len(files)} files")

        # Initialize combined dataset
        combined_dataset = CombinedDataset()

        # Filter files that have DataFrames loaded
        valid_files = [f for f in files if f.has_dataframe and f.dataframe is not None]

        if not valid_files:
            logger.warning("No files with loaded DataFrames to combine")
            combined_dataset.df = pd.DataFrame()
            return combined_dataset

        # Get all canonical fields from mapping model
        all_canonical_fields = [cf.name for cf in mapping_model.canonical_fields]

        if not all_canonical_fields:
            logger.warning("No canonical fields defined in mapping model")
            combined_dataset.df = pd.DataFrame()
            return combined_dataset

        logger.info(f"Combining on {len(all_canonical_fields)} canonical fields")

        # Process each file
        per_file_frames = []
        for file_desc in valid_files:
            per_file_df = self._build_per_file_dataframe(
                file_desc,
                mapping_model,
                all_canonical_fields,
                include_source_tracking
            )

            if per_file_df is not None:
                per_file_frames.append(per_file_df)

                # Create metadata
                per_file_dataset = self._create_per_file_metadata(
                    file_desc,
                    mapping_model,
                    per_file_df
                )
                combined_dataset.source_metadata.append(per_file_dataset)

        # Combine all DataFrames
        if per_file_frames:
            try:
                combined_df = pd.concat(per_file_frames, ignore_index=True)
                combined_dataset.df = combined_df

                logger.info(
                    f"Combined dataset created: {len(combined_df)} rows, "
                    f"{len(combined_df.columns)} columns"
                )
            except Exception as e:
                logger.error(f"Error combining DataFrames: {e}", exc_info=True)
                combined_dataset.df = pd.DataFrame()
        else:
            logger.warning("No valid DataFrames to combine")
            combined_dataset.df = pd.DataFrame()

        return combined_dataset

    def _build_per_file_dataframe(
        self,
        file_desc: FileDescriptor,
        mapping_model: ColumnMappingModel,
        all_canonical_fields: List[str],
        include_source_tracking: bool
    ) -> Optional[pd.DataFrame]:
        """
        Build a DataFrame for a single file with canonical column names.

        Args:
            file_desc: FileDescriptor with loaded DataFrame
            mapping_model: ColumnMappingModel with mappings
            all_canonical_fields: List of all canonical field names
            include_source_tracking: Whether to add __source_file column

        Returns:
            DataFrame with canonical columns, or None if error
        """
        try:
            # Get the original DataFrame
            original_df = file_desc.dataframe.copy()

            # Get column mapping for this file
            file_mappings = mapping_model.file_column_to_canonical.get(file_desc.id, {})

            if not file_mappings:
                logger.warning(f"No column mappings for file {file_desc.filename}")
                return None

            # Build new DataFrame with canonical columns
            canonical_df = pd.DataFrame()

            # Map each original column to its canonical name
            for original_col, canonical_name in file_mappings.items():
                if original_col in original_df.columns:
                    canonical_df[canonical_name] = original_df[original_col]
                else:
                    logger.warning(
                        f"Column '{original_col}' not found in {file_desc.filename}"
                    )

            # Add missing canonical fields as NaN
            for canonical_field in all_canonical_fields:
                if canonical_field not in canonical_df.columns:
                    canonical_df[canonical_field] = pd.NA

            # Add source tracking column if requested
            if include_source_tracking:
                canonical_df['__source_file'] = file_desc.filename

            logger.debug(
                f"Built DataFrame for {file_desc.filename}: "
                f"{len(canonical_df)} rows, {len(canonical_df.columns)} columns"
            )

            return canonical_df

        except Exception as e:
            logger.error(
                f"Error building DataFrame for {file_desc.filename}: {e}",
                exc_info=True
            )
            return None

    def _create_per_file_metadata(
        self,
        file_desc: FileDescriptor,
        mapping_model: ColumnMappingModel,
        per_file_df: pd.DataFrame
    ) -> PerFileDataset:
        """
        Create metadata for a single file's contribution to the combined dataset.

        Args:
            file_desc: FileDescriptor
            mapping_model: ColumnMappingModel
            per_file_df: The processed DataFrame for this file

        Returns:
            PerFileDataset with metadata
        """
        # Get column mapping for this file
        file_mappings = mapping_model.file_column_to_canonical.get(file_desc.id, {})

        # Get effective canonical columns (excluding metadata columns)
        effective_columns = [
            col for col in per_file_df.columns
            if not col.startswith('__')
        ]

        return PerFileDataset(
            file_id=file_desc.id,
            df=per_file_df,
            column_mapping=file_mappings.copy(),
            effective_columns=effective_columns
        )

    def build_dataset(self, files, mappings):
        """Build a combined dataset from files and mappings (legacy method)."""
        logger.warning("Using legacy build_dataset method")
        # Delegate to new method
        if isinstance(files, list) and hasattr(mappings, 'canonical_fields'):
            return self.build_combined_dataset(files, mappings)
        return None

    def merge_dataframes(self, dataframes):
        """Merge multiple dataframes."""
        if not dataframes:
            return pd.DataFrame()
        try:
            return pd.concat(dataframes, ignore_index=True)
        except Exception as e:
            logger.error(f"Error merging DataFrames: {e}", exc_info=True)
            return pd.DataFrame()

    def apply_mappings(self, dataframe, mappings):
        """Apply column mappings to a dataframe."""
        if dataframe is None or not mappings:
            return dataframe

        try:
            # Rename columns according to mappings
            return dataframe.rename(columns=mappings)
        except Exception as e:
            logger.error(f"Error applying mappings: {e}", exc_info=True)
            return dataframe
