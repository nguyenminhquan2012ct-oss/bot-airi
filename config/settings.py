"""
AIRi Configuration Module

Handles all environment variables and settings validation.
Supports Pydantic settings for type safety and validation.
"""

from pydantic_settings import BaseSettings
from typing import Literal
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    AIRi Configuration Settings
    
    All configuration comes from environment variables.
    See .env.example for reference.
    """
    
    # Discord Configuration
    discord_token: str
    
    # AI Provider Configuration
    ai_provider: Literal["ollama", "openai", "openrouter", "groq"] = "ollama"
    ai_base_url: str = "http://localhost:11434/v1"
    ai_api_key: str = ""
    ai_model: str = "qwen2.5:7b"
    ai_timeout: int = 30
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///airi.db"
    
    # RPG & Gameplay Configuration
    xp_cooldown: int = 60  # seconds between XP gains
    xp_per_message: int = 10
    level_base_xp: int = 100
    level_multiplier: float = 1.5
    
    # World Engine Configuration
    world_tick_interval: int = 300  # seconds (5 minutes)
    world_event_chance: float = 0.15  # 15% chance per tick
    
    # Feature Toggles
    enable_roast: bool = True
    enable_world_events: bool = True
    enable_detective: bool = True
    enable_whatif: bool = True
    
    # Logging Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def validate_critical_settings(self) -> bool:
        """
        Validate critical settings that must be present.
        
        Returns:
            bool: True if all critical settings are valid
            
        Raises:
            ValueError: If critical settings are missing or invalid
        """
        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN is required")
        
        if not self.ai_model:
            raise ValueError("AI_MODEL is required")
        
        if self.xp_cooldown < 0:
            raise ValueError("XP_COOLDOWN must be >= 0")
        
        if not (0 < self.world_event_chance < 1):
            raise ValueError("WORLD_EVENT_CHANCE must be between 0 and 1")
        
        logger.info("[CONFIG] All critical settings validated")
        return True
    
    def get_log_level_int(self) -> int:
        """Convert log level string to logging module level."""
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(self.log_level.upper(), logging.INFO)


# Global settings instance
settings: Settings | None = None


def load_settings() -> Settings:
    """
    Load and validate settings from environment.
    
    Returns:
        Settings: Validated settings object
        
    Raises:
        ValueError: If critical settings are missing
    """
    global settings
    
    try:
        settings = Settings()
        settings.validate_critical_settings()
        logger.info("[CONFIG] Settings loaded successfully")
        return settings
    except Exception as e:
        logger.error(f"[CONFIG] Failed to load settings: {e}")
        raise


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: Global settings object
        
    Raises:
        RuntimeError: If settings haven't been loaded yet
    """
    global settings
    
    if settings is None:
        raise RuntimeError("Settings not loaded. Call load_settings() first.")
    
    return settings
