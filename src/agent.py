"""Central workflow orchestrator for AI Data Processor."""
import argparse
from pathlib import Path
import sys
from typing import Any, Dict
import yaml

from src.analyzer import get_analyzer
from src.cleaner import DataCleaner
from src.data_loader import load_csv_data
from src.logger import setup_logger
from src.reporter import DataReporter

logger = setup_logger("ai_data_processor")


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Loads configuration from YAML file defensively.

    Args:
        config_path: Path to config.yaml.

    Returns:
        Dict: Parsed configuration dictionary.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path.resolve()}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    logger.info(f"Loaded configuration from {path}")
    return config


def run_pipeline(config_path: str = "config.yaml", input_override: str = None) -> Dict[str, Any]:
    """Executes the complete ETL and AI Analysis pipeline.

    Args:
        config_path: Path to the YAML configuration file.
        input_override: Optional path to override the input dataset.

    Returns:
        Dict: Pipeline execution summary.
    """
    logger.info("=== Starting AI Data Processor Pipeline ===")
    config = load_config(config_path)

    # 1. Resolve paths and parameters
    data_cfg = config.get("data", {})
    cleaning_cfg = config.get("cleaning", {})

    input_path = input_override or data_cfg.get("input_path", "data/sample.csv")
    output_dir = data_cfg.get("output_dir", "output")
    cleaned_filename = data_cfg.get("cleaned_filename", "cleaned_data.csv")
    report_filename = data_cfg.get("report_filename", "analysis_report.md")

    # 2. Ingestion phase
    logger.info(f"Phase 1/4: Ingesting dataset from '{input_path}'...")
    required_columns = cleaning_cfg.get("required_columns")
    raw_df = load_csv_data(input_path, required_columns=required_columns)

    # 3. Cleaning & Normalization phase
    logger.info("Phase 2/4: Executing deterministic data cleaning...")
    cleaner = DataCleaner(
        strip_whitespace=cleaning_cfg.get("strip_whitespace", True),
        drop_duplicates=cleaning_cfg.get("drop_duplicates", True),
        handle_nulls=cleaning_cfg.get("handle_nulls", "fill_mean_or_mode"),
        numeric_columns=cleaning_cfg.get("numeric_columns", []),
    )
    cleaned_df, cleaning_summary = cleaner.clean(raw_df)

    # 4. AI Analytical Synthesis phase
    logger.info(f"Phase 3/4: Synthesizing analytical insights (Mode: {config.get('analysis', {}).get('mode')})...")
    analyzer = get_analyzer(config)
    sample_preview = cleaned_df.head(5).to_string(index=False)
    report_content = analyzer.analyze(cleaning_summary, sample_preview)

    # 5. Persistence phase
    logger.info(f"Phase 4/4: Persisting cleaned artifacts and report to '{output_dir}/'...")
    reporter = DataReporter(output_dir=output_dir)
    cleaned_csv_path = reporter.save_cleaned_data(cleaned_df, filename=cleaned_filename)
    report_path = reporter.save_report(report_content, filename=report_filename)

    logger.info("=== Pipeline Completed Successfully! ===")
    logger.info(f"Cleaned CSV: {cleaned_csv_path}")
    logger.info(f"Analysis Report: {report_path}")

    return {
        "status": "success",
        "cleaned_csv": str(cleaned_csv_path),
        "report": str(report_path),
        "summary": cleaning_summary,
    }


def main():
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="AI Data Processor Autonomous Pipeline")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to YAML configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Optional override path for input CSV file",
    )
    args = parser.parse_args()

    try:
        run_pipeline(config_path=args.config, input_override=args.input)
    except Exception as exc:
        logger.error(f"Pipeline execution halted due to error: {exc}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
