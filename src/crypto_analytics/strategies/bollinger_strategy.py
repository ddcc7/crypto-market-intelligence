"""Bollinger Bands trading strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from .base_strategy import BaseStrategy
from ..indicators import BollingerBands


class BollingerStrategy(BaseStrategy):
    """Trading strategy based on Bollinger Bands."""

    def __init__(self, params: Optional[Dict] = None):
        """Initialize strategy with Bollinger Bands indicator.

        Args:
            params: Optional parameters for Bollinger Bands indicator
        """
        super().__init__([BollingerBands(params)])
        self.max_position = 1.0  # Maximum allowed position size

    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on Bollinger Bands.

        Args:
            signals: DataFrame with price and indicator values

        Returns:
            DataFrame with updated signal column
        """
        # Calculate percentage B (position of price within the bands)
        signals["percent_b"] = (signals["price"] - signals["lower_band"]) / (
            signals["upper_band"] - signals["lower_band"]
        )

        # Calculate price distance from middle band as percentage
        signals["price_deviation"] = (
            signals["price"] - signals["middle_band"]
        ) / signals["middle_band"]

        # Initialize signals
        signals["signal"] = 0
        signals["position"] = 0

        for i in range(1, len(signals)):
            prev_position = signals.iloc[i - 1]["position"]

            # Check oversold conditions
            oversold = (signals.iloc[i]["percent_b"] < 0) or (
                (signals.iloc[i]["percent_b"] < 0.2)
                and (signals.iloc[i]["price_deviation"] < -0.02)
            )

            # Check overbought conditions
            overbought = (signals.iloc[i]["percent_b"] > 1) or (
                (signals.iloc[i]["percent_b"] > 0.8)
                and (signals.iloc[i]["price_deviation"] > 0.02)
            )

            # Check middle band reversion
            middle_band_threshold = 0.05
            middle_band_reversion = (
                (signals.iloc[i]["percent_b"] > 0.5 - middle_band_threshold)
                and (signals.iloc[i]["percent_b"] < 0.5 + middle_band_threshold)
                and (abs(prev_position) > 0)
            )

            # Generate signals with position limits
            if oversold and prev_position < self.max_position:
                signals.iloc[i, signals.columns.get_loc("signal")] = 1
            elif overbought and prev_position > -self.max_position:
                signals.iloc[i, signals.columns.get_loc("signal")] = -1
            elif middle_band_reversion:
                signals.iloc[i, signals.columns.get_loc("signal")] = -prev_position

            # Update position with limits
            new_position = prev_position + signals.iloc[i]["signal"]
            signals.iloc[i, signals.columns.get_loc("position")] = np.clip(
                new_position, -self.max_position, self.max_position
            )

        return signals
