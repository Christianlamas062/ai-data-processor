"""Reporter module for disk persistence of cleaned datasets and markdown reports."""
import os
from pathlib import Path
from typing import Any, Dict, Union
import pandas as pd
from src.logger import setup_logger

logger = setup_logger(__name__)


class ReporterError(Exception):
    """Base exception for Reporter errors."""
    pass


class DataReporter:
    """Handles disk persistence for cleaned CSV outputs and analytical reports."""

    def __init__(self, output_dir: Union[str, Path] = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_cleaned_data(
        self, df: pd.DataFrame, filename: str = "cleaned_data.csv"
    ) -> Path:
        """Saves the cleaned DataFrame to CSV.

        Args:
            df: Cleaned pandas DataFrame.
            filename: Output filename.

        Returns:
            Path to the saved CSV file.
        """
        out_path = self.output_dir / filename
        logger.info(f"Saving cleaned dataset to: {out_path}")
        try:
            df.to_csv(out_path, index=False)
            logger.info(f"Successfully saved {len(df)} records to {out_path.name}")
            return out_path
        except Exception as exc:
            msg = f"Failed to save cleaned data to {out_path}: {exc}"
            logger.error(msg)
            raise ReporterError(msg) from exc

    def save_report(
        self,
        report_content: str,
        filename: str = "analysis_report.md",
    ) -> Path:
        """Saves the markdown analysis report to disk.

        Args:
            report_content: Markdown content string.
            filename: Output report filename.

        Returns:
            Path to the saved Markdown file.
        """
        out_path = self.output_dir / filename
        logger.info(f"Saving analytical report to: {out_path}")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            logger.info(f"Successfully wrote report to {out_path.name}")
            return out_path
        except Exception as exc:
            msg = f"Failed to write report to {out_path}: {exc}"
            logger.error(msg)
            raise ReporterError(msg) from exc
