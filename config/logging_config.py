"""
Logging configuration for the Ascend system.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Dict, Any

import structlog
from structlog.stdlib import LoggerFactory

from .settings import settings


def configure_logging() -> None:
    """Configure structured logging for the Ascend system."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Add file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=_parse_size(settings.LOG_MAX_SIZE),
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    
    # Set formatter for file handler
    if settings.LOG_FORMAT == "json":
        file_handler.setFormatter(logging.Formatter('%(message)s'))
    else:
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
    
    # Add file handler to root logger
    logging.getLogger().addHandler(file_handler)
    
    # Set specific log levels for noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google.generativeai").setLevel(logging.INFO)
    logging.getLogger("langchain").setLevel(logging.INFO)
    logging.getLogger("langgraph").setLevel(logging.INFO)


def _parse_size(size_str: str) -> int:
    """Parse size string (e.g., '10MB') to bytes."""
    size_str = size_str.upper()
    if size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        return int(size_str)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


def log_function_call(func):
    """Decorator to log function calls with parameters and results."""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Log function call
        logger.info(
            "Function called",
            function=func.__name__,
            args=args,
            kwargs=kwargs
        )
        
        try:
            result = func(*args, **kwargs)
            logger.info(
                "Function completed",
                function=func.__name__,
                success=True
            )
            return result
        except Exception as e:
            logger.error(
                "Function failed",
                function=func.__name__,
                error=str(e),
                error_type=type(e).__name__,
                success=False
            )
            raise
    
    return wrapper


def log_async_function_call(func):
    """Decorator to log async function calls with parameters and results."""
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Log function call
        logger.info(
            "Async function called",
            function=func.__name__,
            args=args,
            kwargs=kwargs
        )
        
        try:
            result = await func(*args, **kwargs)
            logger.info(
                "Async function completed",
                function=func.__name__,
                success=True
            )
            return result
        except Exception as e:
            logger.error(
                "Async function failed",
                function=func.__name__,
                error=str(e),
                error_type=type(e).__name__,
                success=False
            )
            raise
    
    return wrapper


class PerformanceLogger:
    """Logger for performance metrics and timing."""
    
    def __init__(self, name: str):
        self.logger = get_logger(f"performance.{name}")
        self.name = name
    
    def log_timing(self, operation: str, duration: float, **kwargs):
        """Log timing information for an operation."""
        self.logger.info(
            "Operation timing",
            operation=operation,
            duration=duration,
            **kwargs
        )
    
    def log_metric(self, metric_name: str, value: float, **kwargs):
        """Log a performance metric."""
        self.logger.info(
            "Performance metric",
            metric=metric_name,
            value=value,
            **kwargs
        )
    
    def log_error(self, operation: str, error: Exception, **kwargs):
        """Log an error with context."""
        self.logger.error(
            "Operation error",
            operation=operation,
            error=str(error),
            error_type=type(error).__name__,
            **kwargs
        )


# Initialize logging when module is imported
configure_logging()
