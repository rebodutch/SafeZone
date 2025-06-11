# app/config/logger.py
import sys
import logging
import contextvars
from logging import StreamHandler

from pythonjsonlogger import jsonlogger # type: ignore

from config.settings import LOG_LEVEL

trace_id_var = contextvars.ContextVar("trace_id", default="-")

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        return True

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # for loki JSON logs
    json_handler = StreamHandler(sys.stdout)
    json_formatter = jsonlogger.JsonFormatter(
        '[%(trace_id)s] %(asctime)s %(levelname)s %(name)s %(message)s'
    )
    json_handler.setFormatter(json_formatter)
    json_handler.addFilter(TraceIdFilter())
    logger.addHandler(json_handler)

    # for human-readable logs
    if logger.level == logging.DEBUG:
        text_handler = logging.StreamHandler(sys.stderr)
        text_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        text_handler.setFormatter(text_formatter)
        logger.addHandler(text_handler)
    
    logger.addFilter(TraceIdFilter())