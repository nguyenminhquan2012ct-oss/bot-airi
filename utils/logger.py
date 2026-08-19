"""
AIRi Logging Module

Provides centralized logging configuration with structured formatting.
Ensures secrets (tokens, API keys) are never logged.
"""

import logging
import sys
from typing import Optional
from config.settings import get_settings


class SecureFormatter(logging.Formatter):
    """
    Custom formatter that redacts sensitive information.
    Prevents logging of tokens, API keys, and other secrets.
    """
    
    SENSITIVE_KEYS = [
        "token",
        "api_key",
        "api-key",
        "key",
        "password",
        "secret",
        "auth",
        "discord",
    ]
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record while redacting sensitive data."""
        # Redact message if it contains sensitive keywords
        message = record.getMessage()
        for key in self.SENSITIVE_KEYS:
            if key.lower() in message.lower():
                message = f"[REDACTED: {key}]"
                break
        
        record.msg = message
        return super().format(record)


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    try:
        settings = get_settings()
        log_level = settings.get_log_level_int()
    except Exception:
        # Fallback if settings not loaded yet
        log_level = logging.INFO
    
    logger = logging.getLogger(name or "airi")
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(log_level)
    
    # Console handler with secure formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Format: [COMPONENT] Message
    formatter = SecureFormatter(
        fmt="[%(name)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Component-specific loggers
def get_bot_logger() -> logging.Logger:
    """Get logger for bot components."""
    return logging.getLogger("airi.bot")


def get_db_logger() -> logging.Logger:
    """Get logger for database operations."""
    return logging.getLogger("airi.database")


def get_ai_logger() -> logging.Logger:
    """Get logger for AI operations."""
    return logging.getLogger("airi.ai")


def get_world_logger() -> logging.Logger:
    """Get logger for world engine operations."""
    return logging.getLogger("airi.world")


def get_rpg_logger() -> logging.Logger:
    """Get logger for RPG system operations."""
    return logging.getLogger("airi.rpg")


def get_game_logger() -> logging.Logger:
    """Get logger for game operations."""
    return logging.getLogger("airi.game")


def get_monitor_logger() -> logging.Logger:
    """Get logger for activity monitoring."""
    return logging.getLogger("airi.monitor")


# Initialize root logger
_root_logger = setup_logging("airi")
