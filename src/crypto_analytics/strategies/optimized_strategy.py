"""Optimized trading strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from .base_strategy import BaseStrategy
from ..indicators import MACD, BollingerBands


class OptimizedStrategy(BaseStrategy):
    """Optimized trading strategy based on genetic algorithm optimization."""

    def __init__(self, params: Optional[Dict] = None):
        """Initialize strategy with optimized parameters."""
        super().__init__()
        self.name = "Optimized"

        # Use the successful parameters from SOL-USD optimization
        self.params = params or {
            "indicator_weights": {"macd": 0.6, "bollinger": 0.4},
            "entry_thresholds": {"oversold": -0.8, "overbought": 0.8},
            "exit_thresholds": {"profit": 0.03, "loss": -0.02},
            "position_size": 0.8,
            "stop_loss": 0.05,
            "take_profit": 0.1,
            "lookback_period": 20,
        }

        # Initialize indicators
        self.macd = MACD()
        self.bollinger = BollingerBands()

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on optimized parameters.

        Args:
            data: Market data DataFrame

        Returns:
            DataFrame with trading signals
        """
        signals = data.copy()
        signals["signal"] = 0
        signals["position"] = 0

        # Ensure we have price data
        if "close" in signals.columns:
            signals["price"] = signals["close"]
        elif "Close" in signals.columns:
            signals["price"] = signals["Close"]
            signals["close"] = signals["Close"]

        # Calculate indicators
        macd_data = self.macd.calculate(signals)
        bb_data = self.bollinger.calculate(signals)

        lookback = self.params["lookback_period"]

        for i in range(lookback, len(signals)):
            # Calculate combined signal
            macd_signal = (
                macd_data["macd_line"].iloc[i]
                * self.params["indicator_weights"]["macd"]
            )
            bb_signal = (
                bb_data["bandwidth"].iloc[i]
                * self.params["indicator_weights"]["bollinger"]
            )
            combined_signal = macd_signal + bb_signal

            # Generate entry signals
            if combined_signal < self.params["entry_thresholds"]["oversold"]:
                signals.iloc[i, signals.columns.get_loc("signal")] = 1
            elif combined_signal > self.params["entry_thresholds"]["overbought"]:
                signals.iloc[i, signals.columns.get_loc("signal")] = -1

            # Update position
            new_position = signals.iloc[i - 1]["position"] + signals.iloc[i]["signal"]
            signals.iloc[i, signals.columns.get_loc("position")] = np.clip(
                new_position,
                -self.params["position_size"],
                self.params["position_size"],
            )

            # Check for stop loss and take profit
            if signals.iloc[i - 1]["position"] != 0:
                returns = (
                    signals.iloc[i]["price"] - signals.iloc[i - 1]["price"]
                ) / signals.iloc[i - 1]["price"]

                if (
                    returns * signals.iloc[i - 1]["position"]
                    <= -self.params["stop_loss"]
                ):
                    # Stop loss hit
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0
                elif (
                    returns * signals.iloc[i - 1]["position"]
                    >= self.params["take_profit"]
                ):
                    # Take profit hit
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0

        # Calculate returns
        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        return signals

    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on indicator rules.

        This method is already handled in calculate_signals, so we just return the signals.
        """
        return signals
