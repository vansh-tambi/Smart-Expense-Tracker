import logging
import sys
from flask import has_request_context, g


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = 'SYSTEM'
        return True


def get_logger(name: str) -> logging.Logger:
    """
    Returns a consistently configured logger.
    All loggers write to stdout with a structured format.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.addFilter(RequestIdFilter())
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | ReqID: %(request_id)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger
