"""Exponential Moving Average (EMA) trading strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Union
from .base_strategy import BaseStrategy


class EMAStrategy(BaseStrategy):
    """Trading strategy based on Exponential Moving Average crossovers."""

    def __init__(self, short_period: int = 12, long_period: int = 26):
        """Initialize EMA strategy.

        Args:
            short_period: Period for short-term EMA
            long_period: Period for long-term EMA
        """
        super().__init__()
        self.short_period = short_period
        self.long_period = long_period

    def calculate_ema(
        self, data: Union[pd.DataFrame, pd.Series], period: Optional[int] = None
    ) -> pd.Series:
        """Calculate Exponential Moving Average.

        Args:
            data: DataFrame with 'close' price column or Series of prices
            period: Optional period override

        Returns:
            pd.Series: EMA values
        """
        if isinstance(data, pd.DataFrame):
            if "close" not in data.columns:
                raise ValueError("Data must contain 'close' column")
            prices = data["close"]
        else:
            prices = data

        period = period or self.short_period

        # Use pandas built-in EMA with adjusted smoothing factor for better price tracking
        alpha = 2.0 / (period + 1)  # Standard smoothing factor
        ema = prices.ewm(alpha=alpha, adjust=False, min_periods=1).mean()

        return ema

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals based on EMA crossover.

        Args:
            data: DataFrame with 'close' price column

        Returns:
            pd.Series: Series of trading signals (1 for buy, -1 for sell, 0 for hold)
        """
        short_ema = self.calculate_ema(data, self.short_period)
        long_ema = self.calculate_ema(data, self.long_period)
        price = data["close"]

        signals = pd.Series(0, index=data.index)

        # Calculate trend strength with more sensitive thresholds
        trend_strength = (short_ema - long_ema) / long_ema

        # Calculate momentum with shorter lookback
        momentum = price.pct_change(2)  # Further reduced from 3 to 2
        momentum_ma = momentum.rolling(
            window=2, min_periods=1
        ).mean()  # Further reduced from 3 to 2

        # Calculate price position
        price_above_short = price > short_ema
        price_above_long = price > long_ema

        # Calculate additional trend indicators
        short_slope = short_ema.diff() / short_ema
        long_slope = long_ema.diff() / long_ema
        slope_diff = short_slope - long_slope

        # Calculate trend acceleration
        short_acceleration = short_slope.diff()
        long_acceleration = long_slope.diff()

        # Calculate crossover signals with trend confirmation
        buy_cross = (short_ema > long_ema) & (
            (short_ema.shift(1) <= long_ema.shift(1))  # Standard crossover
            | (
                trend_strength > 0.001
            )  # Reduced threshold for trend strength confirmation
        )
        sell_cross = (short_ema < long_ema) & (
            (short_ema.shift(1) >= long_ema.shift(1))  # Standard crossover
            | (
                trend_strength < -0.001
            )  # Reduced threshold for trend strength confirmation
        )

        # Calculate trend following signals with more sensitive thresholds
        strong_uptrend = (
            (trend_strength >= 0)  # Any positive trend strength
            & (price > price.shift(1))  # Price is rising
            & (
                (price_above_short & price_above_long)  # Price above both EMAs
                | (momentum_ma > -0.001)  # Or positive momentum
                | (short_slope > -0.001)  # Or positive slope
            )
        )
        strong_downtrend = (
            (trend_strength < 0)  # Negative trend strength
            & (price < price.shift(1))  # Price is falling
            & (
                (~price_above_short & ~price_above_long)  # Price below both EMAs
                | (momentum_ma < 0.001)  # Or negative momentum
                | (short_slope < 0.001)  # Or negative slope
            )
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
            (price > short_ema.rolling(window=3).max())  # Further reduced window
            & (momentum > 0.001)  # Reduced threshold
            & (short_slope > 0)
        )
        breakout_down = (
            (price < short_ema.rolling(window=3).min())  # Further reduced window
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

        # Add immediate price level signals
        price_level_up = (
            price > price.rolling(window=5).max()
        )  # Price above recent highs
        price_level_down = (
            price < price.rolling(window=5).min()
        )  # Price below recent lows

        # Add trend strength confirmation signals
        trend_strength_up = (
            (trend_strength > 0)
            & (trend_strength > trend_strength.shift(1))
            & (short_slope > 0)
            & (long_slope > 0)
        )
        trend_strength_down = (
            (trend_strength < 0)
            & (trend_strength < trend_strength.shift(1))
            & (short_slope < 0)
            & (long_slope < 0)
        )

        # Add momentum divergence signals
        momentum_divergence_up = (
            (price < price.shift(1))
            & (momentum > momentum.shift(1))
            & (short_slope > short_slope.shift(1))
        )
        momentum_divergence_down = (
            (price > price.shift(1))
            & (momentum < momentum.shift(1))
            & (short_slope < short_slope.shift(1))
        )

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
            | price_level_up
            | trend_strength_up
            | momentum_divergence_up
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
            | price_level_down
            | trend_strength_down
            | momentum_divergence_down
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
        short_ema = self.calculate_ema(data, self.short_period)
        long_ema = self.calculate_ema(data, self.long_period)

        # Calculate metrics
        metrics = self.calculate_metrics(data, signals)

        # Calculate trend strength
        trend_strength = (short_ema - long_ema) / long_ema

        # Calculate additional metrics
        price_above_short = (data["close"] > short_ema).rolling(window=20).mean()
        price_above_long = (data["close"] > long_ema).rolling(window=20).mean()
        trend_consistency = price_above_short.corr(price_above_long)

        # Add strategy-specific metrics
        metrics.update(
            {
                "signals": signals,
                "short_ema": short_ema,
                "long_ema": long_ema,
                "strategy_metrics": {
                    "mean_ema_spread": float((short_ema - long_ema).mean()),
                    "ema_crossovers": int(
                        abs(signals).diff().fillna(0).abs().sum() / 2
                    ),
                    "avg_trend_duration": float(
                        1 / (abs(signals).diff().fillna(0).abs().mean() / 2)
                    ),
                    "avg_trend_strength": float(abs(trend_strength).mean()),
                    "max_trend_strength": float(abs(trend_strength).max()),
                    "trend_consistency": float(trend_consistency),
                },
            }
        )

        return metrics
