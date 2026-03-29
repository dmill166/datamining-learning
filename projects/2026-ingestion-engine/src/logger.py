"""
logger.py — Centralized Logging Configuration

All modules in this project obtain a logger via:

    from logger import get_logger
    logger = get_logger(__name__)

Why centralize?
    logging.basicConfig() is a one-shot root-logger config — Python honors
    only the first call and silently ignores all subsequent ones. If each
    module calls it independently, the format winner is whichever import
    runs first — non-deterministic and hard to debug.

    Centralizing here gives us:
        - One place to change format, level, or add a file/JSON handler
        - LOG_LEVEL from .env respected consistently across all modules
        - Module names in log output (%(name)s) for message traceability
        - The `if not logger.handlers` guard prevents duplicate handlers
          when modules are re-imported during test collection

Design choice: module-level loggers (not a Logger subclass).
    Python's logging docs recommend get_logger(__name__) over subclassing.
    A custom Logger class would require registering a custom factory —
    unnecessary complexity for no additional benefit.
"""

import logging
import os

from dotenv import load_dotenv

load_dotenv()

_FMT = "%(levelname)s [%(name)s]: %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Returns a configured module-level logger.

    Uses the `if not logger.handlers` guard to prevent duplicated log
    lines when a module is imported multiple times (common in pytest).

    Args:
        name: Typically passed as __name__ from the calling module.

    Returns:
        Configured Logger instance scoped to `name`.
    """
    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_FMT))
        logger.addHandler(handler)

    logger.setLevel(level)
    logger.propagate = False  # Don't pass to root logger; avoids duplicate output
    return logger
