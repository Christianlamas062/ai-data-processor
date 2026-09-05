"""Deterministic pandas data cleaning and normalization module."""
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from src.logger import setup_logger

logger = setup_logger(__name__)


class CleanerError(Exception):
    """Base exception for Cleaner errors."""
    pass


class DataCleaner:
    """Performs deterministic cleaning and normalization on pandas DataFrames."""

    def __init__(
        self,
        strip_whitespace: bool = True,
        drop_duplicates: bool = True,
        handle_nulls: str = "fill_mean_or_mode",
        numeric_columns: Optional[List[str]] = None,
    ):
        self.strip_whitespace = strip_whitespace
        self.drop_duplicates = drop_duplicates
        self.handle_nulls = handle_nulls
        self.numeric_columns = numeric_columns or []

    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Cleans and standardizes the provided DataFrame.

        Args:
            df: Input pandas DataFrame.

        Returns:
            Tuple of (cleaned DataFrame, cleaning summary dictionary).

        Raises:
            CleanerError: If input is not a DataFrame or is empty.
        """
        if not isinstance(df, pd.DataFrame):
            msg = f"Expected pd.DataFrame, got {type(df)}"
            logger.error(msg)
            raise CleanerError(msg)

        if df.empty:
            msg = "Cannot clean an empty DataFrame"
            logger.error(msg)
            raise CleanerError(msg)

        logger.info("Initiating deterministic data cleaning pipeline...")
        cleaned_df = df.copy()
        initial_rows = len(cleaned_df)
        initial_nulls = int(cleaned_df.isnull().sum().sum())

        # 1. Strip whitespace from column headers
        cleaned_df.columns = [str(c).strip() for c in cleaned_df.columns]

        # 2. Strip whitespace from string values
        if self.strip_whitespace:
            for col in cleaned_df.select_dtypes(include=["object", "string"]).columns:
                cleaned_df[col] = cleaned_df[col].apply(
                    lambda val: val.strip() if isinstance(val, str) else val
                )
            logger.info("Trimmed whitespace across string columns")

        # 3. Deduplicate
        duplicates_removed = 0
        if self.drop_duplicates:
            before_dedup = len(cleaned_df)
            cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)
            duplicates_removed = before_dedup - len(cleaned_df)
            logger.info(f"Removed {duplicates_removed} duplicate records")

        # 4. Cast numeric columns
        for col in self.numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")

        # 5. Handle null values
        nulls_imputed = 0
        if self.handle_nulls == "fill_mean_or_mode":
            for col in cleaned_df.columns:
                col_nulls = int(cleaned_df[col].isnull().sum())
                if col_nulls > 0:
                    nulls_imputed += col_nulls
                    if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                        median_val = cleaned_df[col].median()
                        if pd.isna(median_val):
                            median_val = 0
                        cleaned_df[col] = cleaned_df[col].fillna(median_val)
                        logger.info(f"Imputed {col_nulls} nulls in numeric column '{col}' with median: {median_val}")
                    else:
                        modes = cleaned_df[col].mode(dropna=True)
                        mode_val = modes[0] if not modes.empty else "Unknown"
                        cleaned_df[col] = cleaned_df[col].fillna(mode_val)
                        logger.info(f"Imputed {col_nulls} nulls in column '{col}' with mode: '{mode_val}'")

        final_rows = len(cleaned_df)
        final_nulls = int(cleaned_df.isnull().sum().sum())

        summary: Dict[str, Any] = {
            "initial_rows": initial_rows,
            "final_rows": final_rows,
            "duplicates_removed": duplicates_removed,
            "initial_nulls": initial_nulls,
            "nulls_imputed": nulls_imputed,
            "final_nulls": final_nulls,
            "columns": list(cleaned_df.columns),
        }

        logger.info(
            f"Cleaning completed: {initial_rows} -> {final_rows} rows, "
            f"{duplicates_removed} duplicates dropped, {nulls_imputed} nulls imputed."
        )
        return cleaned_df, summary
