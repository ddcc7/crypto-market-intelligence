"""Adaptive MACD strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .adaptive_strategy import (
    AdaptiveStrategy,
    PositionConfig,
    MarketRegime,
    MarketContext,
)


class AdaptiveMACDStrategy(AdaptiveStrategy):
    """MACD strategy with adaptive parameters and position sizing."""

    def __init__(
        self,
        position_config: Optional[PositionConfig] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        """Initialize strategy.

        Args:
            position_config: Position and risk configuration
            params: Strategy parameters including:
                - base_fast_period: Base fast EMA period (default: 12)
                - base_slow_period: Base slow EMA period (default: 26)
                - base_signal_period: Base signal period (default: 9)
                - volatility_adjustment: Whether to adjust periods for volatility
        """
        default_params = {
            "base_fast_period": 12,
            "base_slow_period": 26,
            "base_signal_period": 9,
            "volatility_adjustment": True,
        }
        if params:
            default_params.update(params)
        super().__init__(position_config, default_params)

    def get_adaptive_periods(
        self, context: Optional[MarketContext] = None
    ) -> Dict[str, int]:
        """Get MACD periods adapted to current market context.

        Args:
            context: Current market context

        Returns:
            Dictionary of adapted indicator periods
        """
        if not context or not self.params["volatility_adjustment"]:
            return {
                "fast": self.params["base_fast_period"],
                "slow": self.params["base_slow_period"],
                "signal": self.params["base_signal_period"],
            }

        # Adjust periods based on volatility and regime
        volatility_factor = 1.0 + (context.volatility - 0.2) * 2

        # Regime-specific adjustments
        regime_factors = {
            MarketRegime.STRONG_BULL: 0.8,  # Faster in strong trends
            MarketRegime.WEAK_BULL: 0.9,
            MarketRegime.SIDEWAYS: 1.2,  # Slower in sideways
            MarketRegime.WEAK_BEAR: 0.9,
            MarketRegime.STRONG_BEAR: 0.8,
            MarketRegime.HIGH_VOL: 1.3,  # Slower in high volatility
            MarketRegime.LOW_VOL: 0.7,  # Faster in low volatility
        }
        regime_factor = regime_factors[context.regime]

        # Calculate adjusted periods
        fast_period = max(
            5, int(self.params["base_fast_period"] * volatility_factor * regime_factor)
        )
        slow_period = max(
            10, int(self.params["base_slow_period"] * volatility_factor * regime_factor)
        )
        signal_period = max(
            3,
            int(self.params["base_signal_period"] * volatility_factor * regime_factor),
        )

        return {"fast": fast_period, "slow": slow_period, "signal": signal_period}

    def calculate_raw_signal(self, data: pd.DataFrame) -> float:
        """Calculate raw MACD trading signal.

        Args:
            data: Market data

        Returns:
            Signal value between -1 and 1
        """
        # Get adaptive periods
        periods = self.get_adaptive_periods(self.current_context)

        # Calculate MACD
        fast_ema = data["Close"].ewm(span=periods["fast"], adjust=False).mean()
        slow_ema = data["Close"].ewm(span=periods["slow"], adjust=False).mean()

        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=periods["signal"], adjust=False).mean()
        histogram = macd_line - signal_line

        # Calculate signal strength
        hist_std = histogram.rolling(20).std()
        if hist_std.iloc[-1] > 0:
            signal_strength = histogram.iloc[-1] / (hist_std.iloc[-1] * 2)
        else:
            signal_strength = 0

        # Clip signal to [-1, 1] range
        signal_strength = np.clip(signal_strength, -1, 1)

        # Adjust signal based on trend confirmation
        if self.current_context:
            # Strengthen signal in trending markets
            if self.current_context.regime in [
                MarketRegime.STRONG_BULL,
                MarketRegime.STRONG_BEAR,
            ]:
                signal_strength *= 1.2
            # Weaken signal in sideways markets
            elif self.current_context.regime == MarketRegime.SIDEWAYS:
                signal_strength *= 0.5

            # Zero out signal in extreme volatility
            if self.current_context.regime == MarketRegime.HIGH_VOL:
                signal_strength = 0

        return signal_strength
