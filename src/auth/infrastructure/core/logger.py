import json
import logging
import logging.config
from logging import Logger, getLogger

__all__ = ("logger",)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": record.created,
            "path": record.pathname,
            "line": record.lineno,
        }
        return json.dumps(log_entry)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json": {
            "()": JsonFormatter,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}


logging.config.dictConfig(LOGGING_CONFIG)
logger: Logger = getLogger(__name__)
