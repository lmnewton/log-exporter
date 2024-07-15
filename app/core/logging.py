import logging
import sys
import os
from .constants import READ_LOCATION, BUFFER_SIZE, READ_DEFAULT, BUFFER_DEFAULT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(levelname)s:     %(asctime)s - %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


def startup_log():
    logger.info(
        f"Starting with log directory set to {os.getenv(READ_LOCATION, READ_DEFAULT)} and buffer size {os.getenv(BUFFER_SIZE, BUFFER_DEFAULT)}."
    )
