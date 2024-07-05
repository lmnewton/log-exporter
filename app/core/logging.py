import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(levelname)s:     %(asctime)s - %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
