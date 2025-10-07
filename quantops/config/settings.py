"""Configuration management for the trading engine."""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file and environment variables.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config = get_default_config()
    
    # Load from file if specified
    if config_path and Path(config_path).exists():
        with open(config_path, "r") as f:
            file_config = json.load(f)
            config.update(file_config)
        logger.info(f"Loaded config from {config_path}")
    
    # Override with environment variables
    config = _apply_env_overrides(config)
    
    return config


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration.
    
    Returns:
        Default configuration dictionary
    """
    return {
        "initial_capital": 100000.0,
        "cycle_interval": 1.0,
        "stop_on_error": False,
        "symbols": ["BTC/USDT", "ETH/USDT"],
        "exchanges": {},
        "strategies": [],
        "agent_swarm": {
            "enabled": True,
            "consensus_threshold": 0.6,
            "agents": []
        },
        "risk_management": {
            "max_position_size": 0.1,
            "max_drawdown": 0.2,
            "stop_loss": 0.05
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }


def _apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply environment variable overrides to configuration.
    
    Args:
        config: Base configuration
        
    Returns:
        Updated configuration
    """
    # Trading settings
    if os.getenv("INITIAL_CAPITAL"):
        config["initial_capital"] = float(os.getenv("INITIAL_CAPITAL"))
    
    if os.getenv("CYCLE_INTERVAL"):
        config["cycle_interval"] = float(os.getenv("CYCLE_INTERVAL"))
    
    # Exchange API keys
    if os.getenv("BINANCE_API_KEY") and os.getenv("BINANCE_SECRET"):
        config["exchanges"]["binance"] = {
            "apiKey": os.getenv("BINANCE_API_KEY"),
            "secret": os.getenv("BINANCE_SECRET"),
            "enableRateLimit": True
        }
    
    if os.getenv("COINBASE_API_KEY") and os.getenv("COINBASE_SECRET"):
        config["exchanges"]["coinbase"] = {
            "apiKey": os.getenv("COINBASE_API_KEY"),
            "secret": os.getenv("COINBASE_SECRET"),
            "enableRateLimit": True
        }
    
    # Logging level
    if os.getenv("LOG_LEVEL"):
        config["logging"]["level"] = os.getenv("LOG_LEVEL")
    
    return config


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    logger.info(f"Saved config to {config_path}")


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Setup logging based on configuration.
    
    Args:
        config: Configuration dictionary
    """
    logging_config = config.get("logging", {})
    level = logging_config.get("level", "INFO")
    format_str = logging_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    logging.basicConfig(
        level=getattr(logging, level),
        format=format_str
    )
    
    logger.info(f"Logging configured with level: {level}")
