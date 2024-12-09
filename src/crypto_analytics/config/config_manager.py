from pathlib import Path
import json
import logging
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration settings for crypto analytics."""

    DEFAULT_CONFIG = {
        "data": {
            "historical_dir": "data/historical",
            "results_dir": "data/results",
            "default_period": "2y",
            "default_interval": "1d",
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
        "strategies": {
            "macd": {
                "default_fast_period": 12,
                "default_slow_period": 26,
                "default_signal_period": 9,
            },
            "sma": {"default_short_window": 20, "default_long_window": 50},
        },
        "performance": {
            "annualization_factor": 252,  # Trading days in a year
            "risk_free_rate": 0.02,  # 2% annual risk-free rate
        },
    }

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("config.json")
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    return {**self.DEFAULT_CONFIG, **config}  # Merge with defaults
            else:
                self.save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG

    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split(".")
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def update(self, key: str, value: Any):
        """Update configuration value."""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save_config(self.config)

    def get_strategy_params(self, strategy_name: str) -> Dict[str, Any]:
        """Get default parameters for a strategy."""
        return self.get(f"strategies.{strategy_name}", {})
