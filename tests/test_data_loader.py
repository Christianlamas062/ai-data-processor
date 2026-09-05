"""Tests for data_loader module."""
import pytest
from pathlib import Path
from src.data_loader import (
    load_csv_data,
    DataLoaderError,
    EmptyFileDataLoaderError,
    SchemaValidationError,
)


def test_load_valid_csv(tmp_path):
    """Test loading a normal valid CSV file."""
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("id,customer_name,age,income,department\n1,Alice,30,50000,IT\n2,Bob,25,45000,HR\n")

    df = load_csv_data(csv_file)
    assert len(df) == 2
    assert list(df.columns) == ["id", "customer_name", "age", "income", "department"]


def test_load_nonexistent_file():
    """Test that FileNotFoundError is raised for missing file."""
    with pytest.raises(FileNotFoundError):
        load_csv_data("non_existent_file_path.csv")


def test_load_empty_file(tmp_path):
    """Test that EmptyFileDataLoaderError is raised for a 0-byte file."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")

    with pytest.raises(EmptyFileDataLoaderError):
        load_csv_data(empty_file)


def test_load_header_only_file(tmp_path):
    """Test that EmptyFileDataLoaderError is raised when file only has headers."""
    header_only = tmp_path / "header_only.csv"
    header_only.write_text("id,customer_name,age,income,department\n")

    with pytest.raises(EmptyFileDataLoaderError):
        load_csv_data(header_only)


def test_schema_validation_success(tmp_path):
    """Test schema validation succeeds when all required columns are present."""
    csv_file = tmp_path / "schema_valid.csv"
    csv_file.write_text("id,customer_name,age,income,department\n1,Alice,30,50000,IT\n")

    df = load_csv_data(csv_file, required_columns=["id", "customer_name", "department"])
    assert len(df) == 1


def test_schema_validation_failure(tmp_path):
    """Test SchemaValidationError is raised when required columns are absent."""
    csv_file = tmp_path / "schema_invalid.csv"
    csv_file.write_text("id,customer_name\n1,Alice\n")

    with pytest.raises(SchemaValidationError):
        load_csv_data(csv_file, required_columns=["id", "customer_name", "department"])
