import inspect
import logging
import sys
from types import FrameType

from loguru import logger
from pydantic import BaseModel


def _is_logging_frame(frame: FrameType) -> bool:
    return frame.f_code.co_filename == logging.__file__


def _get_caller_depth(frame: FrameType | None) -> int:
    """Count frames from ``frame`` up to the code that called the stdlib logger."""
    depth = 0
    while frame is not None and (depth == 0 or _is_logging_frame(frame)):
        frame = frame.f_back
        depth += 1
    return depth


class InterceptLoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        depth = _get_caller_depth(inspect.currentframe())
        message = record.getMessage()
        logger.opt(depth=depth, exception=record.exc_info).log(level, message)


class LoggerSettings(BaseModel):
    json_enabled: bool = False
    level: str = "INFO"


def setup_logging(settings: LoggerSettings) -> None:
    logging.basicConfig(
        handlers=[InterceptLoguruHandler()], level=getattr(logging, settings.level)
    )

    if settings.json_enabled:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "serialize": True,
                    "colorize": False,
                    "level": settings.level,
                    "enqueue": True,
                    "backtrace": False,
                }
            ],
        )


class LoggerMixin:
    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(self.__class__.__name__)

        return self._logger
