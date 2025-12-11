"""Logging configuration for Pivot Builder."""

import logging
import sys


def setup_logging(level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger('pivot_builder')
    logger.setLevel(level)

    return logger


# Default logger instance
logger = setup_logging()
