"""CSV data loader module with defensive validations."""
import os
from pathlib import Path
from typing import List, Optional, Union
import pandas as pd
from src.logger import setup_logger

logger = setup_logger(__name__)


class DataLoaderError(Exception):
    """Base exception for DataLoader errors."""
    pass


class EmptyFileDataLoaderError(DataLoaderError):
    """Raised when the target data file is empty."""
    pass


class SchemaValidationError(DataLoaderError):
    """Raised when required schema columns are missing."""
    pass


def load_csv_data(
    filepath: Union[str, Path],
    required_columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Loads a CSV file defensively with validation of existence, contents, and schema.

    Args:
        filepath: Path to the CSV file.
        required_columns: Optional list of expected column names.

    Returns:
        pd.DataFrame: Loaded pandas DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        EmptyFileDataLoaderError: If file size is 0 bytes or contains no rows.
        SchemaValidationError: If required columns are missing from the header.
        DataLoaderError: If an unexpected error occurs during reading.
    """
    path = Path(filepath)
    logger.info(f"Checking data source at: {path}")

    if not path.exists():
        msg = f"Data file does not exist: {path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    if not path.is_file():
        msg = f"Path is not a valid file: {path}"
        logger.error(msg)
        raise DataLoaderError(msg)

    if path.stat().st_size == 0:
        msg = f"Data file is empty (0 bytes): {path}"
        logger.error(msg)
        raise EmptyFileDataLoaderError(msg)

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        msg = f"CSV file contains no data or headers: {path}"
        logger.error(msg)
        raise EmptyFileDataLoaderError(msg)
    except Exception as exc:
        msg = f"Failed to parse CSV file at {path}: {exc}"
        logger.error(msg)
        raise DataLoaderError(msg) from exc

    if df.empty:
        msg = f"CSV file has header but zero data rows: {path}"
        logger.error(msg)
        raise EmptyFileDataLoaderError(msg)

    if required_columns:
        # Strip any extra whitespace from column names when checking
        current_cols = [str(c).strip() for c in df.columns]
        missing = [col for col in required_columns if col not in current_cols]
        if missing:
            msg = f"Schema validation failed. Missing required columns: {missing}. Found: {current_cols}"
            logger.error(msg)
            raise SchemaValidationError(msg)

    logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns from {path.name}")
    return df
