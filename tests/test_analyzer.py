"""Tests for analyzer module and hybrid mode."""
import pytest
from src.analyzer import (
    BaseAnalyzer,
    GeminiAnalyzer,
    AntigravityAnalyzer,
    get_analyzer,
)


def test_get_analyzer_gemini():
    """Test factory creates GeminiAnalyzer."""
    config = {"analysis": {"mode": "gemini", "gemini": {"model_name": "gemini-1.5-flash"}}}
    analyzer = get_analyzer(config)
    assert isinstance(analyzer, GeminiAnalyzer)
    assert analyzer.model_name == "gemini-1.5-flash"


def test_get_analyzer_antigravity():
    """Test factory creates AntigravityAnalyzer."""
    config = {"analysis": {"mode": "antigravity", "antigravity": {"model_target": "gemini-1.5-flash"}}}
    analyzer = get_analyzer(config)
    assert isinstance(analyzer, AntigravityAnalyzer)
    assert analyzer.model_target == "gemini-1.5-flash"


def test_get_analyzer_invalid_mode():
    """Test factory raises ValueError on unsupported mode."""
    config = {"analysis": {"mode": "unsupported_mode"}}
    with pytest.raises(ValueError):
        get_analyzer(config)


def test_gemini_analyzer_fallback():
    """Test GeminiAnalyzer produces report in deterministic fallback mode."""
    analyzer = GeminiAnalyzer()
    summary = {
        "initial_rows": 10,
        "final_rows": 8,
        "duplicates_removed": 2,
        "nulls_imputed": 3,
        "columns": ["id", "customer_name", "department"],
    }
    report = analyzer.analyze(summary, "sample data preview")
    assert "# AI Executive Data Analysis Report" in report
    assert "**8** valid instances" in report


def test_antigravity_analyzer_execution():
    """Test AntigravityAnalyzer synchronous analyze method."""
    analyzer = AntigravityAnalyzer()
    summary = {
        "initial_rows": 10,
        "final_rows": 9,
        "duplicates_removed": 1,
        "nulls_imputed": 2,
    }
    report = analyzer.analyze(summary, "sample data preview")
    assert "Antigravity" in report
    assert "Autonomous Execution Loop" in report
