"""Tests for cleaner module."""
import pytest
import pandas as pd
from src.cleaner import DataCleaner, CleanerError


def test_cleaner_invalid_input():
    """Test CleanerError when input is not a DataFrame."""
    cleaner = DataCleaner()
    with pytest.raises(CleanerError):
        cleaner.clean("not_a_dataframe")


def test_cleaner_empty_dataframe():
    """Test CleanerError when input DataFrame is empty."""
    cleaner = DataCleaner()
    with pytest.raises(CleanerError):
        cleaner.clean(pd.DataFrame())


def test_cleaner_whitespace_and_deduplication():
    """Test stripping whitespace and removing duplicate rows."""
    data = {
        "  customer_name  ": ["  Alice  ", "Bob", "  Alice  "],
        "department": ["  IT  ", "HR", "  IT  "],
    }
    df = pd.DataFrame(data)

    cleaner = DataCleaner(strip_whitespace=True, drop_duplicates=True)
    cleaned_df, summary = cleaner.clean(df)

    # Columns should be stripped
    assert "customer_name" in cleaned_df.columns
    assert "department" in cleaned_df.columns

    # Values should be stripped
    assert cleaned_df["customer_name"].iloc[0] == "Alice"
    assert cleaned_df["department"].iloc[0] == "IT"

    # Duplicates should be removed
    assert len(cleaned_df) == 2
    assert summary["duplicates_removed"] == 1


def test_cleaner_null_imputation():
    """Test numeric and categorical null imputation."""
    data = {
        "age": [20.0, 40.0, None],
        "department": ["Finance", "Finance", None],
    }
    df = pd.DataFrame(data)

    cleaner = DataCleaner(
        handle_nulls="fill_mean_or_mode",
        numeric_columns=["age"],
    )
    cleaned_df, summary = cleaner.clean(df)

    # Missing age (median of [20, 40] is 30.0)
    assert cleaned_df["age"].iloc[2] == 30.0

    # Missing department (mode is "Finance")
    assert cleaned_df["department"].iloc[2] == "Finance"

    assert summary["nulls_imputed"] == 2
    assert summary["final_nulls"] == 0
