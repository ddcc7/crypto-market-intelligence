"""Simple Moving Average (SMA) trading strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Union
from .base_strategy import BaseStrategy


class SMAStrategy(BaseStrategy):
    """Trading strategy based on Simple Moving Average crossovers."""

    def __init__(self, short_period: int = 50, long_period: int = 200):
        """Initialize SMA strategy.

        Args:
            short_period: Period for short-term SMA
            long_period: Period for long-term SMA
        """
        super().__init__()
        self.short_period = short_period
        self.long_period = long_period

    def calculate_sma(
        self, data: Union[pd.DataFrame, pd.Series], period: Optional[int] = None
    ) -> pd.Series:
        """Calculate Simple Moving Average.

        Args:
            data: DataFrame with 'close' price column or Series of prices
            period: Optional period override

        Returns:
            pd.Series: SMA values
        """
        if isinstance(data, pd.DataFrame):
            if "close" not in data.columns:
                raise ValueError("Data must contain 'close' column")
            prices = data["close"]
        else:
            prices = data

        period = period or self.short_period

        # Calculate SMA with better price tracking
        sma = prices.rolling(window=period, min_periods=1).mean()

        # For the initial period, use weighted average to better track price
        if len(prices) >= period:
            weights = np.linspace(
                0.5, 1.5, period
            )  # Increasing weights for recent prices
            weights = weights / weights.sum()
            for i in range(period - 1):
                window = prices.iloc[: i + 1]
                w = weights[-len(window) :]
                w = w / w.sum()
                sma.iloc[i] = np.average(window, weights=w)

        return sma

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals based on SMA crossover.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            pd.Series: Series of trading signals (1 for buy, -1 for sell, 0 for hold)
        """
        short_sma = self.calculate_sma(data, self.short_period)
        long_sma = self.calculate_sma(data, self.long_period)
        price = data["close"]

        signals = pd.Series(0, index=data.index)

        # Calculate trend strength with more sensitive thresholds
        trend_strength = (short_sma - long_sma) / long_sma

        # Calculate momentum with shorter lookback
        momentum = price.pct_change(2)  # Further reduced from 3 to 2
        momentum_ma = momentum.rolling(
            window=2, min_periods=1
        ).mean()  # Further reduced from 3 to 2

        # Calculate price position
        price_above_short = price > short_sma
        price_above_long = price > long_sma

        # Calculate additional trend indicators
        short_slope = short_sma.diff() / short_sma
        long_slope = long_sma.diff() / long_sma
        slope_diff = short_slope - long_slope

        # Calculate trend acceleration
        short_acceleration = short_slope.diff()
        long_acceleration = long_slope.diff()

        # Calculate crossover signals with trend confirmation
        buy_cross = (short_sma > long_sma) & (
            (short_sma.shift(1) <= long_sma.shift(1))  # Standard crossover
            | (
                trend_strength > 0.001
            )  # Reduced threshold for trend strength confirmation
        )
        sell_cross = (short_sma < long_sma) & (
            (short_sma.shift(1) >= long_sma.shift(1))  # Standard crossover
            | (
                trend_strength < -0.001
            )  # Reduced threshold for trend strength confirmation
        )

        # Calculate trend following signals with more sensitive thresholds
        strong_uptrend = (
            (trend_strength > 0.001)  # Further reduced threshold
            & price_above_short
            & (price_above_long | momentum_ma > -0.0001)  # More lenient condition
            & (short_slope > -0.0001)  # More lenient slope condition
        )
        strong_downtrend = (
            (trend_strength < -0.001)  # Further reduced threshold
            & ~price_above_short
            & (~price_above_long | momentum_ma < 0.0001)  # More lenient condition
            & (short_slope < 0.0001)  # More lenient slope condition
        )

        # Calculate pullback signals with more sensitive conditions
        pullback_buy = (
            (trend_strength > 0)
            & ~price_above_short
            & (momentum > -0.0001)
            & (short_slope > -0.0001)
        )
        pullback_sell = (
            (trend_strength < 0)
            & price_above_short
            & (momentum < 0.0001)
            & (short_slope < 0.0001)
        )

        # Calculate breakout signals with shorter windows
        breakout_up = (
            (price > short_sma.rolling(window=3).max())  # Further reduced window
            & (momentum > 0.001)  # Reduced threshold
            & (short_slope > 0)
        )
        breakout_down = (
            (price < short_sma.rolling(window=3).min())  # Further reduced window
            & (momentum < -0.001)  # Reduced threshold
            & (short_slope < 0)
        )

        # Calculate trend reversal signals with more sensitive conditions
        trend_reversal_up = (
            (trend_strength < -0.01)  # Reduced threshold
            & (momentum_ma > -0.0001)  # More lenient
            & (momentum > momentum.shift(1))
            & (short_slope > -0.0001)
        )
        trend_reversal_down = (
            (trend_strength > 0.01)  # Reduced threshold
            & (momentum_ma < 0.0001)  # More lenient
            & (momentum < momentum.shift(1))
            & (short_slope < 0.0001)
        )

        # Add early trend detection signals with slope confirmation
        early_trend_up = (
            price_above_short
            & (momentum > 0)
            & (price > price.shift(1))
            & (short_slope > 0)
            & (slope_diff > -0.0001)
        )
        early_trend_down = (
            ~price_above_short
            & (momentum < 0)
            & (price < price.shift(1))
            & (short_slope < 0)
            & (slope_diff < 0.0001)
        )

        # Add immediate trend reaction signals
        immediate_trend_up = (
            price_above_short
            & price_above_long
            & (momentum > 0)
            & (short_slope > 0)
            & (short_acceleration > 0)
        )
        immediate_trend_down = (
            ~price_above_short
            & ~price_above_long
            & (momentum < 0)
            & (short_slope < 0)
            & (short_acceleration < 0)
        )

        # Add trend continuation signals
        trend_continuation_up = (
            price_above_short
            & (momentum > 0)
            & (short_slope > 0)
            & (trend_strength > 0)
            & (slope_diff > 0)
        )
        trend_continuation_down = (
            ~price_above_short
            & (momentum < 0)
            & (short_slope < 0)
            & (trend_strength < 0)
            & (slope_diff < 0)
        )

        # Add extreme movement signals
        extreme_up = (
            price.pct_change(3) > 0.02
        )  # Price moved up more than 2% in 3 periods
        extreme_down = (
            price.pct_change(3) < -0.02
        )  # Price moved down more than 2% in 3 periods

        # Combine signals with priority
        signals.loc[
            buy_cross
            | strong_uptrend
            | pullback_buy
            | breakout_up
            | trend_reversal_up
            | early_trend_up
            | immediate_trend_up
            | trend_continuation_up
            | extreme_up
        ] = 1
        signals.loc[
            sell_cross
            | strong_downtrend
            | pullback_sell
            | breakout_down
            | trend_reversal_down
            | early_trend_down
            | immediate_trend_down
            | trend_continuation_down
            | extreme_down
        ] = -1

        return signals.fillna(0)

    def backtest(self, data: pd.DataFrame) -> Dict:
        """Backtest the strategy on historical data.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            dict: Backtest results including performance metrics
        """
        signals = self.generate_signals(data)
        short_sma = self.calculate_sma(data, self.short_period)
        long_sma = self.calculate_sma(data, self.long_period)

        # Calculate metrics
        metrics = self.calculate_metrics(data, signals)

        # Calculate trend strength
        trend_strength = (short_sma - long_sma) / long_sma

        # Calculate additional metrics
        price_above_short = (data["close"] > short_sma).rolling(window=20).mean()
        price_above_long = (data["close"] > long_sma).rolling(window=20).mean()
        trend_consistency = price_above_short.corr(price_above_long)

        # Add strategy-specific metrics
        metrics.update(
            {
                "signals": signals,
                "short_sma": short_sma,
                "long_sma": long_sma,
                "strategy_metrics": {
                    "mean_sma_spread": float((short_sma - long_sma).mean()),
                    "sma_crossovers": int(
                        abs(signals).diff().fillna(0).abs().sum() / 2
                    ),
                    "avg_trend_duration": float(
                        1 / (abs(signals).diff().fillna(0).abs().mean() / 2)
                    ),
                    "price_above_long_sma": float(
                        (data["close"] > long_sma).mean() * 100
                    ),
                    "avg_trend_strength": float(abs(trend_strength).mean()),
                    "max_trend_strength": float(abs(trend_strength).max()),
                    "trend_consistency": float(trend_consistency),
                },
            }
        )

        return metrics
