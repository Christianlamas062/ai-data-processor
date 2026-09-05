"""Logging configuration with colorama support."""
import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter to color log levels using colorama."""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level = f"{color}[{record.levelname:<8}]{Style.RESET_ALL}"
        message = record.getMessage()
        return f"{Fore.LIGHTBLACK_EX}{timestamp}{Style.RESET_ALL} {level} {message}"


def setup_logger(name: str = "ai_data_processor", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a colorized logger instance.

    Args:
        name: Name of the logger.
        level: Minimum logging level.

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)
    return logger
