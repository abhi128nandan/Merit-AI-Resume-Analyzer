import logging
import sys
from pathlib import Path

from app.core.config import settings
from app.core.constants import DEFAULT_LOG_DIR


def setup_logger() -> logging.Logger:
    """Configures and returns a centralized application logger."""
    logger = logging.getLogger("ai_resume_analyzer")
    logger.setLevel(settings.LOG_LEVEL.upper())

    # Avoid duplicate handlers if logger is configured multiple times
    if logger.handlers:
        return logger

    # Formatter for structured logs
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_dir = Path(DEFAULT_LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
