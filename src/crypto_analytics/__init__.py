"""Cryptocurrency market analytics package."""

from .indicators import BaseIndicator, MACD, BollingerBands
from .strategies import (
    BaseStrategy,
    MACDStrategy,
    BollingerStrategy,
    AdaptiveStrategy,
    AdaptiveMACDStrategy,
    AdaptiveBollingerStrategy,
    PositionConfig,
    MarketRegime,
    MarketContext,
)

__version__ = "0.1.0"

__all__ = [
    "BaseIndicator",
    "MACD",
    "BollingerBands",
    "BaseStrategy",
    "MACDStrategy",
    "BollingerStrategy",
    "AdaptiveStrategy",
    "AdaptiveMACDStrategy",
    "AdaptiveBollingerStrategy",
    "PositionConfig",
    "MarketRegime",
    "MarketContext",
]
