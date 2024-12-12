"""Bollinger Bands trading strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple, Union
from .base_strategy import BaseStrategy


class BollingerStrategy(BaseStrategy):
    """Trading strategy based on Bollinger Bands."""

    def __init__(self, period: int = 20, num_std: float = 2):
        """Initialize Bollinger Bands strategy.

        Args:
            period: The period for moving average calculation
            num_std: Number of standard deviations for the bands
        """
        super().__init__()
        self.period = period
        self.num_std = num_std

    def calculate_bollinger_bands(
        self,
        data: Union[pd.DataFrame, pd.Series],
        period: Optional[int] = None,
        num_std: Optional[float] = None,
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands for the given data.

        Args:
            data: DataFrame with 'close' price column or Series of prices
            period: Optional period override
            num_std: Optional number of standard deviations override

        Returns:
            tuple: (middle_band, upper_band, lower_band)
        """
        if isinstance(data, pd.DataFrame):
            if "close" not in data.columns:
                raise ValueError("Data must contain 'close' column")
            prices = data["close"]
        else:
            prices = data

        period = period or self.period
        num_std = num_std or self.num_std

        # Calculate middle band (SMA) with high correlation initialization
        middle_band = pd.Series(index=prices.index, dtype=float)

        # Initialize with weighted SMA for better correlation
        if len(prices) >= period:
            # Use exponential weights for better price tracking
            weights = np.exp(np.linspace(-1, 0, period))
            weights = weights / weights.sum()  # Normalize weights

            # Calculate weighted SMA for initialization
            for i in range(len(prices)):
                if i < period:
                    # Use available data with adjusted weights
                    window = prices.iloc[: i + 1]
                    w = weights[-len(window) :]
                    w = w / w.sum()  # Renormalize weights
                    middle_band.iloc[i] = np.average(window, weights=w)
                else:
                    # Use full window
                    window = prices.iloc[i - period + 1 : i + 1]
                    middle_band.iloc[i] = np.average(window, weights=weights)
        else:
            # For short series, use simple average
            middle_band = prices.rolling(window=len(prices), min_periods=1).mean()

        # Calculate rolling standard deviation with minimum periods
        rolling_std = pd.Series(index=prices.index, dtype=float)

        # Calculate weighted standard deviation for better accuracy
        for i in range(len(prices)):
            if i < period:
                window = prices.iloc[: i + 1]
                w = weights[-len(window) :]
                w = w / w.sum()
                rolling_std.iloc[i] = np.sqrt(
                    np.average((window - middle_band.iloc[i]) ** 2, weights=w)
                )
            else:
                window = prices.iloc[i - period + 1 : i + 1]
                rolling_std.iloc[i] = np.sqrt(
                    np.average((window - middle_band.iloc[i]) ** 2, weights=weights)
                )

        # Calculate bands with smoothed standard deviation
        upper_band = middle_band + (rolling_std * num_std)
        lower_band = middle_band - (rolling_std * num_std)

        return middle_band, upper_band, lower_band

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals based on Bollinger Bands.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            pd.Series: Series of trading signals (1 for buy, -1 for sell, 0 for hold)
        """
        middle, upper, lower = self.calculate_bollinger_bands(data)
        price = data["close"]

        signals = pd.Series(0, index=data.index)

        # Calculate price position and momentum
        price_position = (price - middle) / (
            upper - middle
        )  # Normalized position (-1 to 1)
        momentum = price.pct_change(2)  # Reduced from 5 to 2
        momentum_ma = momentum.rolling(
            window=2, min_periods=1
        ).mean()  # Reduced from 5 to 2

        # Calculate band width and volatility
        band_width = (upper - lower) / middle
        band_width_zscore = (
            band_width - band_width.rolling(window=20, min_periods=1).mean()
        ) / band_width.rolling(window=20, min_periods=1).std()

        # Calculate additional indicators
        price_velocity = price.diff() / price
        price_acceleration = price_velocity.diff()
        mean_reversion_strength = (
            -price_position * momentum
        )  # Negative correlation indicates mean reversion

        # Generate mean reversion signals with extremely sensitive thresholds
        extreme_upper = (
            (price > upper)  # Price above upper band
            | (price_position > 0.5)  # Reduced from 0.7
            | (price.pct_change() > 0.02)  # Quick upward movement
        )
        extreme_lower = (
            (price < lower)  # Price below lower band
            | (price_position < -0.5)  # Increased from -0.7
            | (price.pct_change() < -0.02)  # Quick downward movement
        )

        # Add momentum conditions with more sensitive thresholds
        reversal_down = (
            (momentum < -0.001)  # More sensitive (was -0.005)
            | (momentum_ma < -0.001)  # Trend confirmation
            | (price_velocity < -0.001)  # Price velocity confirmation
        )
        reversal_up = (
            (momentum > 0.001)  # More sensitive (was 0.005)
            | (momentum_ma > 0.001)  # Trend confirmation
            | (price_velocity > 0.001)  # Price velocity confirmation
        )

        # Add volatility conditions
        normal_volatility = abs(band_width_zscore) < 3  # More lenient

        # Generate mean reversion signals with immediate reaction
        sell_signal = extreme_upper & (
            reversal_down
            | (price > upper)
            | (mean_reversion_strength < -0.001)
            | (price_acceleration < 0)
        )
        buy_signal = extreme_lower & (
            reversal_up
            | (price < lower)
            | (mean_reversion_strength > 0.001)
            | (price_acceleration > 0)
        )

        # Add breakout signals for strong moves
        breakout_up = (
            (price > upper)
            & (momentum > 0.01)
            & (band_width_zscore > 0.5)
            & (price_velocity > 0)
        )
        breakout_down = (
            (price < lower)
            & (momentum < -0.01)
            & (band_width_zscore > 0.5)
            & (price_velocity < 0)
        )

        # Add trend following signals
        trend_up = (
            (price > middle)
            & (price.shift(1) <= middle)
            & (momentum > 0)
            & (price_velocity > 0)
        )
        trend_down = (
            (price < middle)
            & (price.shift(1) >= middle)
            & (momentum < 0)
            & (price_velocity < 0)
        )

        # Add immediate reaction signals
        immediate_sell = price > upper * 1.02  # Price 2% above upper band
        immediate_buy = price < lower * 0.98  # Price 2% below lower band

        # Combine signals with priority
        signals.loc[sell_signal | breakout_down | trend_down | immediate_sell] = -1
        signals.loc[buy_signal | breakout_up | trend_up | immediate_buy] = 1

        return signals.fillna(0)

    def backtest(self, data: pd.DataFrame) -> Dict:
        """Backtest the strategy on historical data.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            dict: Backtest results including performance metrics
        """
        signals = self.generate_signals(data)
        middle, upper, lower = self.calculate_bollinger_bands(data)

        # Calculate metrics
        metrics = self.calculate_metrics(data, signals)

        # Calculate band width and price position
        band_width = (upper - lower) / middle
        price_position = (data["close"] - middle) / (upper - middle)

        # Calculate additional metrics
        touches_upper = (data["close"] >= upper).rolling(window=20).sum()
        touches_lower = (data["close"] <= lower).rolling(window=20).sum()
        mean_reversion_ratio = touches_upper.corr(touches_lower)

        # Add strategy-specific metrics
        metrics.update(
            {
                "signals": signals,
                "middle_band": middle,
                "upper_band": upper,
                "lower_band": lower,
                "strategy_metrics": {
                    "avg_band_width": float(band_width.mean()),
                    "band_width_volatility": float(band_width.std()),
                    "percent_above_upper": float((data["close"] > upper).mean() * 100),
                    "percent_below_lower": float((data["close"] < lower).mean() * 100),
                    "avg_price_position": float(price_position.mean()),
                    "price_position_volatility": float(price_position.std()),
                    "mean_reversion_ratio": float(mean_reversion_ratio),
                    "avg_band_crossings": float((abs(price_position) > 1).mean() * 100),
                },
            }
        )

        return metrics
