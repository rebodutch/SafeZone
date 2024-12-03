# app/config/logger.py
import logging
from logging.handlers import RotatingFileHandler

MAX_LOG_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_LEVEL = logging.DEBUG

logger = logging.getLogger("logs/app.logger")

def setup_handlers():
    logger.setLevel(LOG_LEVEL)    
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=MAX_LOG_FILE_SIZE, backupCount=3
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

if not logger.handlers:
    setup_handlers()

def get_logger():
    """
    Returns the logger instance for the application.

    This logger is configured with both file and console handlers.
    The file handler writes logs to 'app.log' with a maximum size of 5 MB and keeps 3 backup files.
    The console handler outputs logs to the console.

    Returns:
        logging.Logger: The configured logger instance.
    """
    return logger
