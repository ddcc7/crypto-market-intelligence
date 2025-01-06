"""Trading strategies for cryptocurrency market analysis."""

from .base_strategy import BaseStrategy
from .breakout_strategy import BreakoutStrategy
from .macd_strategy import MACDStrategy
from .bollinger_strategy import BollingerStrategy
from .adaptive_strategy import (
    AdaptiveStrategy,
    PositionConfig,
    MarketRegime,
    MarketContext,
)
from .adaptive_macd import AdaptiveMACDStrategy
from .adaptive_bollinger import AdaptiveBollingerStrategy
from .optimized_strategy import OptimizedStrategy
from .ml_strategy_combiner import MLStrategyCombiner

__all__ = [
    "BaseStrategy",
    "BreakoutStrategy",
    "MACDStrategy",
    "BollingerStrategy",
    "AdaptiveStrategy",
    "AdaptiveMACDStrategy",
    "AdaptiveBollingerStrategy",
    "OptimizedStrategy",
    "MLStrategyCombiner",
    "PositionConfig",
    "MarketRegime",
    "MarketContext",
]
