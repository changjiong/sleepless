from __future__ import annotations

import os
import sys
from pathlib import Path

from loguru import logger


LOG_DIR = Path(os.getenv("CLOCKPLA_LOG_DIR", "logs"))
LOG_LEVEL = os.getenv("CLOCKPLA_LOG_LEVEL", "TRACE").upper()
LOG_RETENTION = os.getenv("CLOCKPLA_LOG_RETENTION", "14 days")
LOG_ROTATION = os.getenv("CLOCKPLA_LOG_ROTATION", "50 MB")

_CONFIGURED = False


def configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[component]} | {name}:{function}:{line} - {message}",
    )
    logger.add(
        LOG_DIR / "clockpla.trace.log",
        level="TRACE",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        retention=LOG_RETENTION,
        rotation=LOG_ROTATION,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[component]} | {name}:{function}:{line} - {message}",
    )
    logger.add(
        LOG_DIR / "clockpla.jsonl",
        level="TRACE",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        retention=LOG_RETENTION,
        rotation=LOG_ROTATION,
        serialize=True,
    )

    _CONFIGURED = True


def get_logger(component: str):
    configure_logging()
    return logger.bind(component=component)
