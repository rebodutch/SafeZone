# app/config/logger.py
import logging
from logging.handlers import RotatingFileHandler

from config.settings import LOG_LEVEL, MAX_LOG_FILE_SIZE
from config.settings import SERVICE_NAME

logger = logging.getLogger(SERVICE_NAME)


def setup_handlers():
    # Set the log level based on the LOG_LEVEL environment variable [DEBUG, INFO, WARNING]
    if LOG_LEVEL == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif LOG_LEVEL == "INFO":
        logger.setLevel(logging.INFO)
    elif LOG_LEVEL == "WARNING":
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        f"{SERVICE_NAME}.log", maxBytes=MAX_LOG_FILE_SIZE, backupCount=3
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


if not logger.handlers:
    setup_handlers()


def get_logger():
    return logger
