"""Adaptive Bollinger Bands strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .adaptive_strategy import (
    AdaptiveStrategy,
    PositionConfig,
    MarketRegime,
    MarketContext,
)


class AdaptiveBollingerStrategy(AdaptiveStrategy):
    """Bollinger Bands strategy with adaptive parameters and position sizing."""

    def __init__(
        self,
        position_config: Optional[PositionConfig] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        """Initialize strategy.

        Args:
            position_config: Position and risk configuration
            params: Strategy parameters including:
                - base_window: Base period for moving average (default: 20)
                - base_num_std: Base number of standard deviations (default: 2)
                - mean_reversion_threshold: Threshold for mean reversion signals
                - trend_following_threshold: Threshold for trend following signals
                - adaptive_bands: Whether to adjust bands for market regime
        """
        default_params = {
            "base_window": 20,
            "base_num_std": 2.0,
            "mean_reversion_threshold": 0.8,
            "trend_following_threshold": 1.2,
            "adaptive_bands": True,
        }
        if params:
            default_params.update(params)
        super().__init__(position_config, default_params)

    def get_adaptive_parameters(
        self, context: Optional[MarketContext] = None
    ) -> Dict[str, float]:
        """Get Bollinger Bands parameters adapted to current market context.

        Args:
            context: Current market context

        Returns:
            Dictionary of adapted indicator parameters
        """
        if not context or not self.params["adaptive_bands"]:
            return {
                "window": self.params["base_window"],
                "num_std": self.params["base_num_std"],
            }

        # Adjust parameters based on volatility and regime
        volatility_factor = 1.0 + (context.volatility - 0.2) * 2

        # Regime-specific adjustments
        regime_factors = {
            MarketRegime.STRONG_BULL: {
                "window": 0.8,  # Faster in strong trends
                "std": 1.2,  # Wider bands
            },
            MarketRegime.WEAK_BULL: {"window": 0.9, "std": 1.1},
            MarketRegime.SIDEWAYS: {"window": 1.0, "std": 1.0},
            MarketRegime.WEAK_BEAR: {"window": 0.9, "std": 1.1},
            MarketRegime.STRONG_BEAR: {"window": 0.8, "std": 1.2},
            MarketRegime.HIGH_VOL: {
                "window": 1.3,  # Slower in high volatility
                "std": 1.5,  # Much wider bands
            },
            MarketRegime.LOW_VOL: {
                "window": 0.7,  # Faster in low volatility
                "std": 0.8,  # Tighter bands
            },
        }

        window_factor = regime_factors[context.regime]["window"]
        std_factor = regime_factors[context.regime]["std"]

        # Calculate adjusted parameters
        window = max(
            10, int(self.params["base_window"] * volatility_factor * window_factor)
        )
        num_std = max(1.0, self.params["base_num_std"] * volatility_factor * std_factor)

        return {"window": window, "num_std": num_std}

    def calculate_raw_signal(self, data: pd.DataFrame) -> float:
        """Calculate raw Bollinger Bands trading signal.

        Args:
            data: Market data

        Returns:
            Signal value between -1 and 1
        """
        # Get adaptive parameters
        params = self.get_adaptive_parameters(self.current_context)

        # Calculate Bollinger Bands
        rolling_mean = data["Close"].rolling(window=params["window"]).mean()
        rolling_std = data["Close"].rolling(window=params["window"]).std()

        upper_band = rolling_mean + (rolling_std * params["num_std"])
        lower_band = rolling_mean - (rolling_std * params["num_std"])

        # Calculate price position within bands
        current_price = data["Close"].iloc[-1]
        band_width = upper_band.iloc[-1] - lower_band.iloc[-1]
        relative_position = (current_price - rolling_mean.iloc[-1]) / (band_width / 2)

        # Calculate trend strength and direction
        price_trend = data["Close"].diff(params["window"]).iloc[-1]
        trend_direction = np.sign(price_trend) if abs(price_trend) > 0 else 0

        # Initialize signal
        signal = 0.0

        if self.current_context:
            if self.current_context.regime in [
                MarketRegime.STRONG_BULL,
                MarketRegime.STRONG_BEAR,
            ]:
                # Trend-following mode in strong trends
                if abs(relative_position) > self.params["trend_following_threshold"]:
                    signal = np.sign(relative_position)
            else:
                # Mean-reversion mode in other regimes
                if abs(relative_position) > self.params["mean_reversion_threshold"]:
                    signal = -np.sign(relative_position)

            # Adjust signal strength based on position within bands
            signal *= min(1.0, abs(relative_position) / 2)

            # Reduce signal in high volatility
            if self.current_context.regime == MarketRegime.HIGH_VOL:
                signal *= 0.5

            # Strengthen signal if trend confirms
            if np.sign(signal) == trend_direction:
                signal *= 1.2

        return signal
