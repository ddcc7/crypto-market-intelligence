"""Stochastic Oscillator trading strategy implementation."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple, Union
from .base_strategy import BaseStrategy


class StochasticStrategy(BaseStrategy):
    """Trading strategy based on Stochastic Oscillator."""

    def __init__(
        self,
        k_period: int = 14,
        d_period: int = 3,
        overbought: float = 80,
        oversold: float = 20,
    ):
        """Initialize Stochastic strategy.

        Args:
            k_period: Period for %K line
            d_period: Period for %D line (signal line)
            overbought: Overbought threshold
            oversold: Oversold threshold
        """
        super().__init__()
        self.k_period = k_period
        self.d_period = d_period
        self.overbought = overbought
        self.oversold = oversold

    def calculate_stochastic(
        self,
        data: pd.DataFrame,
        k_period: Optional[int] = None,
        d_period: Optional[int] = None,
    ) -> Tuple[pd.Series, pd.Series]:
        """Calculate Stochastic Oscillator.

        Args:
            data: DataFrame with OHLC data
            k_period: Optional period override for %K
            d_period: Optional period override for %D

        Returns:
            tuple: (%K, %D) values
        """
        if not all(col in data.columns for col in ["high", "low", "close"]):
            raise ValueError("Data must contain 'high', 'low', and 'close' columns")

        k_period = k_period or self.k_period
        d_period = d_period or self.d_period

        # Calculate %K with minimum periods and weighted windows
        k = pd.Series(index=data.index, dtype=float)

        for i in range(len(data)):
            if i < k_period:
                window = slice(0, i + 1)
            else:
                window = slice(i - k_period + 1, i + 1)

            window_data = data.iloc[window]
            window_high = window_data["high"]
            window_low = window_data["low"]

            # Use exponential weights for recent prices
            weights = np.exp(np.linspace(-1, 0, len(window_data)))
            weights = weights / weights.sum()

            # Calculate weighted high and low
            high = np.average(window_high, weights=weights)
            low = np.average(window_low, weights=weights)

            if high == low:
                k.iloc[i] = 50  # Middle value when range is zero
            else:
                # Calculate %K with current close and clip to 0-100 range
                k.iloc[i] = np.clip(
                    100 * (data["close"].iloc[i] - low) / (high - low), 0, 100
                )

        # Calculate %D with weighted moving average
        d = pd.Series(index=data.index, dtype=float)

        for i in range(len(data)):
            if i < d_period:
                window = slice(0, i + 1)
            else:
                window = slice(i - d_period + 1, i + 1)

            window_k = k.iloc[window]

            # Use exponential weights for smoothing
            weights = np.exp(np.linspace(-1, 0, len(window_k)))
            weights = weights / weights.sum()

            # Calculate weighted average and clip to 0-100 range
            d.iloc[i] = np.clip(np.average(window_k, weights=weights), 0, 100)

        return k, d

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals based on Stochastic Oscillator.

        Args:
            data: DataFrame with OHLC data

        Returns:
            pd.Series: Series of trading signals (1 for buy, -1 for sell, 0 for hold)
        """
        k, d = self.calculate_stochastic(data)
        signals = pd.Series(0, index=data.index)

        # Calculate trend and momentum
        price = data["close"]
        price_sma = price.rolling(window=20, min_periods=1).mean()
        momentum = price.pct_change(3)
        momentum_ma = momentum.rolling(window=3, min_periods=1).mean()

        # Calculate trend direction
        trend_up = price > price_sma
        momentum_up = momentum_ma > 0

        # Generate signals with more sensitive conditions
        oversold = (k < self.oversold) | (d < self.oversold)
        overbought = (k > self.overbought) | (d > self.overbought)

        # Buy signals: Oversold + (Upward momentum or price above SMA)
        buy_signals = oversold & (momentum_up | trend_up)

        # Sell signals: Overbought + (Downward momentum or price below SMA)
        sell_signals = overbought & (~momentum_up | ~trend_up)

        # Add early reversal signals
        early_buy = (k.shift(1) < self.oversold) & (k > k.shift(1)) & (momentum > 0)
        early_sell = (k.shift(1) > self.overbought) & (k < k.shift(1)) & (momentum < 0)

        # Add momentum confirmation signals
        momentum_buy = (k < 30) & (k > k.shift(1)) & (momentum > 0)
        momentum_sell = (k > 70) & (k < k.shift(1)) & (momentum < 0)

        # Combine signals
        signals[buy_signals | early_buy | momentum_buy] = 1
        signals[sell_signals | early_sell | momentum_sell] = -1

        return signals

    def backtest(self, data: pd.DataFrame) -> Dict:
        """Backtest the strategy on historical data.

        Args:
            data: DataFrame with OHLC data

        Returns:
            dict: Backtest results including performance metrics
        """
        signals = self.generate_signals(data)
        k, d = self.calculate_stochastic(data)

        # Calculate metrics
        metrics = self.calculate_metrics(data, signals)

        # Calculate additional stochastic metrics
        overbought_periods = (k > self.overbought) & (d > self.overbought)
        oversold_periods = (k < self.oversold) & (d < self.oversold)

        # Calculate divergence metrics
        price_momentum = data["close"].pct_change(self.k_period)
        stoch_momentum = k - k.shift(self.k_period)
        divergence = (
            (price_momentum > 0) & (stoch_momentum < 0)
        ) | (  # Bearish divergence
            (price_momentum < 0) & (stoch_momentum > 0)
        )  # Bullish divergence

        # Calculate trend metrics
        trend = data["close"].rolling(window=20).mean()
        trend_direction = (trend > trend.shift(1)).astype(int)
        trend_alignment = ((k > 50) == (trend_direction > 0)).mean()

        # Add strategy-specific metrics
        metrics.update(
            {
                "signals": signals,
                "stoch_k": k,
                "stoch_d": d,
                "strategy_metrics": {
                    "overbought_count": int(overbought_periods.sum()),
                    "oversold_count": int(oversold_periods.sum()),
                    "avg_k_value": float(k.mean()),
                    "avg_d_value": float(d.mean()),
                    "k_d_crossovers": int(((k > d) != (k > d).shift(1)).sum()),
                    "time_in_extreme": float(
                        (overbought_periods | oversold_periods).mean() * 100
                    ),
                    "avg_k_volatility": float(k.std()),
                    "avg_d_volatility": float(d.std()),
                    "divergence_count": int(divergence.sum()),
                    "trend_alignment": float(trend_alignment * 100),
                    "signal_effectiveness": float(
                        abs(signals * data["close"].pct_change().shift(-1)).mean() * 100
                    ),
                },
            }
        )

        return metrics
