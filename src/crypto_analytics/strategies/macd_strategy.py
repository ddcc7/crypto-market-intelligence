"""MACD trading strategy implementation."""

import pandas as pd
from typing import Dict, Optional
from .base_strategy import BaseStrategy
from ..indicators import MACD


class MACDStrategy(BaseStrategy):
    """Trading strategy based on MACD indicator."""

    def __init__(self, params: Optional[Dict] = None):
        """Initialize strategy with MACD indicator.

        Args:
            params: Optional parameters for MACD indicator
        """
        super().__init__([MACD(params)])

    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on MACD.

        Args:
            signals: DataFrame with price and indicator values

        Returns:
            DataFrame with updated signal column
        """
        # Calculate trend direction using MACD line
        signals["trend"] = signals["macd_line"].rolling(window=5).mean()

        # Generate signals based on MACD crossovers
        crossover = signals["macd_line"] - signals["signal_line"]
        prev_crossover = crossover.shift(1)

        # Buy signals: MACD line crosses above signal line
        buy_signals = (
            (crossover > 0)
            & (prev_crossover < 0)
            & (  # Additional conditions for stronger signals
                (signals["histogram"] > 0)  # Positive momentum
                | (signals["trend"] > 0)  # Uptrend
            )
        )
        signals.loc[buy_signals, "signal"] = 1

        # Sell signals: MACD line crosses below signal line
        sell_signals = (
            (crossover < 0)
            & (prev_crossover > 0)
            & (  # Additional conditions for stronger signals
                (signals["histogram"] < 0)  # Negative momentum
                | (signals["trend"] < 0)  # Downtrend
            )
        )
        signals.loc[sell_signals, "signal"] = -1

        # Calculate current position
        signals["position"] = signals["signal"].cumsum()

        # Exit positions on strong trend reversal
        trend_reversal = (signals["position"] > 0) & (  # Long position
            signals["trend"] < -signals["trend"].std()
        ) | (  # Strong downtrend
            signals["position"] < 0
        ) & (  # Short position
            signals["trend"] > signals["trend"].std()
        )  # Strong uptrend
        signals.loc[trend_reversal, "signal"] = -signals.loc[trend_reversal, "position"]

        return signals
