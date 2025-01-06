import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_indicator import BaseIndicator


class BollingerBands(BaseIndicator):
    """Bollinger Bands indicator."""

    def __init__(self, params: Dict[str, Any] = None):
        """Initialize Bollinger Bands indicator.

        Args:
            params: Dictionary with parameters:
                - window: Period for moving average (default: 20)
                - num_std: Number of standard deviations (default: 2)
        """
        default_params = {"window": 20, "num_std": 2}
        super().__init__(params or default_params)

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate Bollinger Bands indicator values.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            DataFrame with columns: middle_band, upper_band, lower_band, bandwidth
        """
        self.validate_data(data, ["close"])

        # Calculate middle band (SMA)
        middle_band = data["close"].rolling(window=self.params["window"]).mean()

        # Calculate standard deviation
        std = data["close"].rolling(window=self.params["window"]).std()

        # Calculate bands
        upper_band = middle_band + (std * self.params["num_std"])
        lower_band = middle_band - (std * self.params["num_std"])

        # Calculate bandwidth
        bandwidth = (upper_band - lower_band) / middle_band

        return pd.DataFrame(
            {
                "middle_band": middle_band,
                "upper_band": upper_band,
                "lower_band": lower_band,
                "bandwidth": bandwidth,
            },
            index=data.index,
        )

    def get_signal_thresholds(self) -> Dict[str, float]:
        """Get Bollinger Bands signal thresholds.

        Returns:
            Dictionary of threshold values
        """
        return {
            "bandwidth_threshold": 0.1,
            "price_distance_threshold": 0.02,  # 2% from bands
        }
