import logging
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get log level from environment or default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logger(name, log_level=None):
    """
    Set up a logger with the specified name and log level.

    Args:
        name: Logger name (typically __name__ of the calling module)
        log_level: Optional override for the default log level

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)

    # Set log level from parameter, environment, or default to INFO
    level = log_level or LOG_LEVEL
    logger.setLevel(getattr(logging, level))

    # Create console handler if logger has no handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Add formatter to handler
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

    return logger
