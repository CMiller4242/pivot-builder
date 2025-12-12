"""Service for building pivot tables from DataFrames."""

from typing import Optional
import pandas as pd

from pivot_builder.config.logging_config import logger
from pivot_builder.models.pivot_model import PivotConfig, PivotValueField


class PivotEngineService:
    """Builds pivot tables from DataFrames using pivot configurations."""

    def __init__(self):
        pass

    def build_pivot(self, df: pd.DataFrame, config: PivotConfig) -> pd.DataFrame:
        """
        Build a pivot table from a DataFrame using the given configuration.

        Args:
            df: Source DataFrame (typically the combined dataset)
            config: PivotConfig with rows, columns, values, and filters

        Returns:
            Pivoted DataFrame with flattened columns and reset index
        """
        if df is None or len(df) == 0:
            logger.warning("Cannot build pivot from empty DataFrame")
            return pd.DataFrame()

        if not config.is_valid():
            logger.warning("Pivot configuration is not valid (no values defined)")
            return pd.DataFrame()

        try:
            # Step 1: Apply filters if any
            filtered_df = self._apply_filters(df, config.filters)

            if len(filtered_df) == 0:
                logger.warning("No data left after applying filters")
                return pd.DataFrame()

            # Step 2: Build aggregation function dictionary
            aggfunc_dict = self._build_aggfunc_dict(config.values)

            # Step 3: Determine index and columns
            index = config.rows if config.rows else None
            columns = config.columns if config.columns else None

            # Step 4: Extract value column names
            values = [v.column for v in config.values]

            # Step 5: Build pivot table
            logger.info(
                f"Building pivot: index={index}, columns={columns}, "
                f"values={values}, aggfunc={aggfunc_dict}"
            )

            pivot_df = pd.pivot_table(
                filtered_df,
                index=index,
                columns=columns,
                values=values,
                aggfunc=aggfunc_dict,
                fill_value=0
            )

            # Step 6: Flatten MultiIndex columns if present
            pivot_df = self._flatten_columns(pivot_df, config.values)

            # Step 7: Reset index to make it a flat DataFrame
            pivot_df = pivot_df.reset_index()

            logger.info(f"Pivot built successfully: shape={pivot_df.shape}")
            return pivot_df

        except Exception as e:
            logger.error(f"Error building pivot: {e}", exc_info=True)
            return pd.DataFrame()

    def _apply_filters(
        self,
        df: pd.DataFrame,
        filters: dict
    ) -> pd.DataFrame:
        """
        Apply filters to DataFrame.

        Args:
            df: Source DataFrame
            filters: Dict mapping column names to list of allowed values

        Returns:
            Filtered DataFrame
        """
        if not filters:
            return df

        filtered = df.copy()
        for column, allowed_values in filters.items():
            if column in filtered.columns and allowed_values:
                filtered = filtered[filtered[column].isin(allowed_values)]
                logger.debug(f"Applied filter on {column}: {len(filtered)} rows remain")

        return filtered

    def _build_aggfunc_dict(self, value_fields: list) -> dict:
        """
        Build aggregation function dictionary from value fields.

        Args:
            value_fields: List of PivotValueField objects

        Returns:
            Dict mapping column names to aggregation functions
        """
        aggfunc_dict = {}

        for value_field in value_fields:
            # Map aggregation string to pandas function
            agg_func = value_field.aggregation

            # pandas accepts these as strings: 'sum', 'mean', 'count', 'min', 'max'
            aggfunc_dict[value_field.column] = agg_func

        return aggfunc_dict

    def _flatten_columns(
        self,
        pivot_df: pd.DataFrame,
        value_fields: list
    ) -> pd.DataFrame:
        """
        Flatten MultiIndex columns into readable strings.

        Converts columns like ('sales', 'sum') to 'sales_sum'.

        Args:
            pivot_df: Pivot DataFrame with potentially MultiIndex columns
            value_fields: List of PivotValueField objects

        Returns:
            DataFrame with flattened column names
        """
        if isinstance(pivot_df.columns, pd.MultiIndex):
            # Flatten MultiIndex columns
            new_columns = []
            for col in pivot_df.columns:
                if isinstance(col, tuple):
                    # Join tuple elements with underscore
                    # Filter out empty strings
                    parts = [str(c) for c in col if str(c) != '']
                    new_col = '_'.join(parts)
                    new_columns.append(new_col)
                else:
                    new_columns.append(col)

            pivot_df.columns = new_columns
            logger.debug(f"Flattened columns: {new_columns}")

        return pivot_df
