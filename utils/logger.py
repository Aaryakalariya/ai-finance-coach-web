"""
logger.py - Centralized logging configuration for AI Finance Coach.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.environ.get("LOG_DIR", "logs")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logger(name="ai_finance_coach"):
    """
    Configure and return the application's root-ish logger.
    Writes to both console and a rotating file under LOG_DIR/app.log.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        # Already configured (avoids duplicate handlers on reload)
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name="ai_finance_coach"):
    return logging.getLogger(name)