# core/logger.py

import logging
import os
from rich.logging import RichHandler


def setup_logger(config):

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("HunterX")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler("logs/hunterx.log")
    file_handler.setFormatter(formatter)

    rich_handler = RichHandler(
        rich_tracebacks=True,
        markup=True
    )

    logger.addHandler(file_handler)
    logger.addHandler(rich_handler)

    return logger