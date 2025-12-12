"""Service for comprehensive data validation."""

from typing import TYPE_CHECKING
import pandas as pd

from pivot_builder.config.logging_config import logger
from pivot_builder.models.validation_model import ValidationReport

if TYPE_CHECKING:
    from pivot_builder.controllers.app_controller import AppController


class ValidationService:
    """Validates files, mappings, combined dataset, and pivot configuration."""

    def validate_all(self, app: 'AppController') -> ValidationReport:
        """
        Run all validation checks on the application state.

        Args:
            app: Application controller with all state

        Returns:
            ValidationReport with all issues found
        """
        report = ValidationReport()

        # Validate files
        self._validate_files(app, report)

        # Validate mapping
        self._validate_mapping(app, report)

        # Validate combined dataset
        self._validate_combined_dataset(app, report)

        # Validate pivot configuration and data
        self._validate_pivot(app, report)

        logger.info(f"Validation complete: {len(report.errors())} errors, "
                   f"{len(report.warnings())} warnings, {len(report.infos())} infos")

        return report

    def _validate_files(self, app: 'AppController', report: ValidationReport):
        """Validate file loading state."""
        if not hasattr(app, 'file_model') or not app.file_model:
            report.add("error", "NO_FILES", "No file model available")
            return

        files = app.file_model.files
        if not files or len(files) == 0:
            report.add("error", "NO_FILES_LOADED", "No files have been loaded")
            return

        # Check for files with errors
        error_files = []
        missing_sheet_files = []

        for file_id, file_desc in files.items():
            if hasattr(file_desc, 'status') and file_desc.status == 'error':
                error_files.append(file_desc.filename)

            # Check XLSX files for selected sheet
            if file_desc.file_type == 'xlsx':
                if not hasattr(file_desc, 'selected_sheet') or not file_desc.selected_sheet:
                    missing_sheet_files.append(file_desc.filename)

        if error_files:
            report.add("warning", "FILES_WITH_ERRORS",
                      f"Files with errors: {', '.join(error_files[:3])}" +
                      (f" and {len(error_files) - 3} more" if len(error_files) > 3 else ""),
                      {"count": len(error_files)})

        if missing_sheet_files:
            report.add("warning", "MISSING_SHEET_SELECTION",
                      f"XLSX files missing sheet selection: {', '.join(missing_sheet_files[:3])}" +
                      (f" and {len(missing_sheet_files) - 3} more" if len(missing_sheet_files) > 3 else ""),
                      {"count": len(missing_sheet_files)})

        # Info about loaded files
        report.add("info", "FILES_LOADED",
                  f"Loaded {len(files)} file(s)",
                  {"count": len(files)})

    def _validate_mapping(self, app: 'AppController', report: ValidationReport):
        """Validate mapping configuration."""
        if not hasattr(app, 'mapping_controller') or not app.mapping_controller:
            report.add("warning", "NO_MAPPING_CONTROLLER", "Mapping controller not available")
            return

        mapping_model = app.mapping_controller.mapping_model
        if not mapping_model:
            report.add("warning", "NO_MAPPING_MODEL", "Mapping model not available")
            return

        # Check if mapping is empty
        if not mapping_model.canonical_fields or len(mapping_model.canonical_fields) == 0:
            report.add("warning", "EMPTY_MAPPING",
                      "No canonical fields defined in mapping")
            return

        # Check for high unmatched column count
        total_columns = 0
        mapped_columns = 0

        for field in mapping_model.canonical_fields:
            for file_id, col in field.source_columns.items():
                if col:  # Column is mapped
                    mapped_columns += 1
                total_columns += 1

        if total_columns > 0:
            unmapped_count = total_columns - mapped_columns
            if unmapped_count > total_columns * 0.5:  # More than 50% unmapped
                report.add("warning", "HIGH_UNMAPPED_COLUMNS",
                          f"High number of unmapped columns: {unmapped_count}/{total_columns}",
                          {"unmapped": unmapped_count, "total": total_columns})

        # Check for extremely sparse canonical fields
        if len(mapping_model.canonical_fields) > 0:
            total_mappings = len(mapping_model.canonical_fields) * len(app.file_model.files)
            actual_mappings = sum(
                len([c for c in field.source_columns.values() if c])
                for field in mapping_model.canonical_fields
            )

            if total_mappings > 0 and actual_mappings < total_mappings * 0.3:  # Less than 30% filled
                report.add("warning", "SPARSE_CANONICAL_FIELDS",
                          f"Canonical fields are very sparse ({actual_mappings}/{total_mappings} filled)",
                          {"filled": actual_mappings, "total": total_mappings})

    def _validate_combined_dataset(self, app: 'AppController', report: ValidationReport):
        """Validate combined dataset state."""
        if not hasattr(app, 'combined_dataset'):
            report.add("warning", "NO_COMBINED_DATASET", "Combined dataset not built yet")
            return

        combined_dataset = app.combined_dataset
        if not combined_dataset or combined_dataset.df is None:
            report.add("warning", "COMBINED_DATASET_EMPTY", "Combined dataset is empty")
            return

        df = combined_dataset.df
        rows, cols = df.shape

        # Info about combined dataset
        report.add("info", "COMBINED_DATASET_INFO",
                  f"Combined dataset: {rows} rows × {cols} columns",
                  {"rows": rows, "columns": cols})

        # Warning if 0 rows
        if rows == 0:
            report.add("warning", "COMBINED_DATASET_NO_ROWS",
                      "Combined dataset has 0 rows")

        # Check for duplicate canonical columns (shouldn't happen)
        canonical_cols = combined_dataset.get_canonical_columns()
        if len(canonical_cols) != len(set(canonical_cols)):
            duplicates = [col for col in set(canonical_cols) if canonical_cols.count(col) > 1]
            report.add("warning", "DUPLICATE_CANONICAL_COLUMNS",
                      f"Duplicate canonical columns detected: {', '.join(duplicates[:5])}",
                      {"duplicates": duplicates})

    def _validate_pivot(self, app: 'AppController', report: ValidationReport):
        """Validate pivot configuration and output."""
        if not hasattr(app, 'pivot_controller') or not app.pivot_controller:
            report.add("info", "NO_PIVOT_CONTROLLER", "Pivot controller not available")
            return

        pivot_controller = app.pivot_controller
        config = pivot_controller.config

        # Check if pivot config has values
        if not config.values or len(config.values) == 0:
            report.add("warning", "NO_PIVOT_VALUES",
                      "Pivot configuration has no value fields defined")
        else:
            # Check for dtype warnings (non-numeric aggregations)
            if hasattr(app, 'combined_dataset') and app.combined_dataset.df is not None:
                df = app.combined_dataset.df
                numeric_aggs = ['sum', 'mean']

                for value_field in config.values:
                    col = value_field.column
                    agg = value_field.aggregation

                    if agg in numeric_aggs and col in df.columns:
                        if not pd.api.types.is_numeric_dtype(df[col]):
                            report.add("warning", "NON_NUMERIC_AGGREGATION",
                                      f"Aggregation '{agg}' on non-numeric column '{col}'",
                                      {"column": col, "aggregation": agg})

        # Check if rows/cols are empty (allowed but warn)
        if not config.rows or len(config.rows) == 0:
            if config.values and len(config.values) > 0:
                report.add("info", "NO_PIVOT_ROWS",
                          "Pivot has no row fields (will create single-row summary)")

        if not config.columns or len(config.columns) == 0:
            if config.values and len(config.values) > 0:
                report.add("info", "NO_PIVOT_COLUMNS",
                          "Pivot has no column fields (simple aggregation)")

        # Check pivot output
        pivot_df = pivot_controller.pivot_df
        if pivot_df is not None and len(pivot_df) > 0:
            rows, cols = pivot_df.shape
            report.add("info", "PIVOT_OUTPUT_INFO",
                      f"Pivot output: {rows} rows × {cols} columns",
                      {"rows": rows, "columns": cols})
        elif config.values and len(config.values) > 0:
            report.add("warning", "PIVOT_NOT_BUILT",
                      "Pivot configuration exists but no output generated")
