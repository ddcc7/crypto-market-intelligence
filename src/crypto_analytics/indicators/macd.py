import pandas as pd
from typing import Dict, Any
from .base_indicator import BaseIndicator


class MACD(BaseIndicator):
    """MACD (Moving Average Convergence Divergence) indicator."""

    def __init__(self):
        super().__init__("MACD")

    def calculate(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> pd.DataFrame:
        """
        Calculate MACD indicator values.

        Args:
            df: DataFrame with price data
            fast_period: Period for fast EMA
            slow_period: Period for slow EMA
            signal_period: Period for signal line EMA

        Returns:
            DataFrame with MACD indicators
        """
        df = self.prepare_data(df)

        # Calculate EMAs
        fast_ema = df["close"].ewm(span=fast_period, adjust=False).mean()
        slow_ema = df["close"].ewm(span=slow_period, adjust=False).mean()

        # Calculate MACD components
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        return pd.DataFrame(
            {
                "macd_line": macd_line,
                "signal_line": signal_line,
                "histogram": histogram,
            },
            index=df.index,
        )

    def generate_signals(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> pd.DataFrame:
        """
        Generate trading signals based on MACD crossovers.

        Args:
            df: DataFrame with price data
            fast_period: Period for fast EMA
            slow_period: Period for slow EMA
            signal_period: Period for signal line EMA

        Returns:
            DataFrame with trading signals
        """
        # Calculate MACD indicators
        macd_data = self.calculate(df, fast_period, slow_period, signal_period)

        # Initialize signals DataFrame
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]
        signals = pd.concat([signals, macd_data], axis=1)

        # Generate signals on crossovers
        signals["signal"] = 0

        # Buy signals: MACD line crosses above Signal line
        signals.loc[
            (signals["macd_line"] > signals["signal_line"])
            & (signals["macd_line"].shift(1) <= signals["signal_line"].shift(1)),
            "signal",
        ] = 1

        # Sell signals: MACD line crosses below Signal line
        signals.loc[
            (signals["macd_line"] < signals["signal_line"])
            & (signals["macd_line"].shift(1) >= signals["signal_line"].shift(1)),
            "signal",
        ] = -1

        # Calculate positions
        signals["position"] = signals["signal"].cumsum()

        return signals
