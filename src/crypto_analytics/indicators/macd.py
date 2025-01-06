import pandas as pd
from typing import Dict, Any
from .base_indicator import BaseIndicator


class MACD(BaseIndicator):
    """Moving Average Convergence Divergence (MACD) indicator."""

    def __init__(self, params: Dict[str, Any] = None):
        """Initialize MACD indicator.

        Args:
            params: Dictionary with parameters:
                - fast_period: Period for fast EMA (default: 12)
                - slow_period: Period for slow EMA (default: 26)
                - signal_period: Period for signal line (default: 9)
        """
        default_params = {"fast_period": 12, "slow_period": 26, "signal_period": 9}
        super().__init__(params or default_params)

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicator values.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            DataFrame with columns: macd_line, signal_line, histogram
        """
        self.validate_data(data, ["close"])

        # Calculate EMAs
        fast_ema = (
            data["close"].ewm(span=self.params["fast_period"], adjust=False).mean()
        )
        slow_ema = (
            data["close"].ewm(span=self.params["slow_period"], adjust=False).mean()
        )

        # Calculate MACD line and Signal line
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(
            span=self.params["signal_period"], adjust=False
        ).mean()
        histogram = macd_line - signal_line

        return pd.DataFrame(
            {
                "macd_line": macd_line,
                "signal_line": signal_line,
                "histogram": histogram,
            },
            index=data.index,
        )

    def get_signal_thresholds(self) -> Dict[str, float]:
        """Get MACD signal thresholds.

        Returns:
            Dictionary of threshold values
        """
        return {"zero_line": 0.0, "histogram_threshold": 0.0}
