"""Market analysis utilities for cryptocurrency analysis."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union


class MarketAnalyzer:
    """Analyzes market conditions and trends."""

    def __init__(self, anomaly_threshold: float = 3.0):
        """Initialize MarketAnalyzer.

        Args:
            anomaly_threshold: Number of standard deviations for anomaly detection
        """
        self.anomaly_threshold = anomaly_threshold

    def calculate_market_stats(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive market statistics.

        Args:
            data: DataFrame with OHLC data

        Returns:
            dict: Market statistics
        """
        if not all(col in data.columns for col in ["close", "high", "low", "volume"]):
            raise ValueError(
                "Data must contain 'close', 'high', 'low', and 'volume' columns"
            )

        # Calculate returns and volatility
        returns = data["close"].pct_change()
        volatility = returns.std() * np.sqrt(252)  # Annualized

        # Calculate trading ranges
        daily_range = (data["high"] - data["low"]) / data["close"]
        avg_range = daily_range.mean()

        # Calculate volume metrics
        avg_volume = data["volume"].mean()
        volume_std = data["volume"].std()

        # Calculate trend metrics
        sma_20 = data["close"].rolling(window=20).mean()
        sma_50 = data["close"].rolling(window=50).mean()
        trend = 1 if sma_20.iloc[-1] > sma_50.iloc[-1] else -1

        # Calculate momentum
        momentum = (data["close"].iloc[-1] / data["close"].iloc[-20] - 1) * 100

        return {
            "returns": {
                "daily_mean": float(returns.mean()),
                "daily_std": float(returns.std()),
                "annualized_return": float(returns.mean() * 252),
                "annualized_volatility": float(volatility),
            },
            "trading_range": {
                "average_range": float(avg_range),
                "range_volatility": float(daily_range.std()),
            },
            "volume": {
                "average_volume": float(avg_volume),
                "volume_volatility": float(volume_std),
                "volume_trend": float(data["volume"].iloc[-5:].mean() / avg_volume),
            },
            "trend": {
                "current_trend": trend,
                "momentum": float(momentum),
                "distance_from_sma20": float(
                    (data["close"].iloc[-1] / sma_20.iloc[-1] - 1) * 100
                ),
                "distance_from_sma50": float(
                    (data["close"].iloc[-1] / sma_50.iloc[-1] - 1) * 100
                ),
            },
        }

    def detect_anomalies(
        self, data: pd.DataFrame, columns: Optional[List[str]] = None
    ) -> Dict[str, pd.Series]:
        """Detect anomalies in market data.

        Args:
            data: DataFrame with market data
            columns: List of columns to check for anomalies

        Returns:
            dict: Dictionary of anomalies by column
        """
        if columns is None:
            columns = ["close", "volume"] if "volume" in data.columns else ["close"]

        anomalies = {}

        # Detect price movement anomalies
        if "close" in data.columns:
            # Calculate multiple metrics for price anomalies
            price = data["close"]
            returns = price.pct_change()
            abs_returns = returns.abs()
            log_returns = np.log(price / price.shift(1))
            price_changes = price.diff()

            # Calculate rolling statistics
            window = 20
            returns_mean = returns.rolling(window=window, min_periods=1).mean()
            returns_std = returns.rolling(window=window, min_periods=1).std()
            abs_returns_mean = abs_returns.rolling(window=window, min_periods=1).mean()
            abs_returns_std = abs_returns.rolling(window=window, min_periods=1).std()
            log_returns_mean = log_returns.rolling(window=window, min_periods=1).mean()
            log_returns_std = log_returns.rolling(window=window, min_periods=1).std()

            # Calculate z-scores for each metric
            returns_z = (returns - returns_mean) / returns_std
            abs_returns_z = (abs_returns - abs_returns_mean) / abs_returns_std
            log_returns_z = (log_returns - log_returns_mean) / log_returns_std

            # Calculate price level anomalies
            price_mean = price.rolling(window=50, min_periods=1).mean()
            price_std = price.rolling(window=50, min_periods=1).std()
            price_z = (price - price_mean) / price_std

            # Calculate momentum anomalies
            momentum = price.pct_change(5)
            momentum_mean = momentum.rolling(window=window, min_periods=1).mean()
            momentum_std = momentum.rolling(window=window, min_periods=1).std()
            momentum_z = (momentum - momentum_mean) / momentum_std

            # Calculate consecutive moves
            up_moves = (returns > 0).astype(int)
            down_moves = (returns < 0).astype(int)
            consecutive_up = up_moves.rolling(window=3, min_periods=3).sum()
            consecutive_down = down_moves.rolling(window=3, min_periods=3).sum()

            # Identify anomalies
            anomalies["price_movements"] = pd.Series(False, index=data.index)
            anomalies["price_movements"][
                (abs(returns_z) > self.anomaly_threshold)
                | (abs(abs_returns_z) > self.anomaly_threshold)
                | (abs(log_returns_z) > self.anomaly_threshold)
                | (abs(price_z) > self.anomaly_threshold)
                | (abs(momentum_z) > self.anomaly_threshold)
                | (consecutive_up == 3)
                | (consecutive_down == 3)
                | (abs(returns) > abs_returns.quantile(0.95))
            ] = True

        # Detect volume anomalies if available
        if "volume" in data.columns:
            # Calculate volume metrics
            volume = data["volume"]
            volume_changes = volume.pct_change()
            log_volume = np.log(volume)
            log_volume_changes = log_volume.diff()

            # Calculate rolling statistics
            window = 20
            volume_mean = volume.rolling(window=window, min_periods=1).mean()
            volume_std = volume.rolling(window=window, min_periods=1).std()
            changes_mean = volume_changes.rolling(window=window, min_periods=1).mean()
            changes_std = volume_changes.rolling(window=window, min_periods=1).std()
            log_changes_mean = log_volume_changes.rolling(
                window=window, min_periods=1
            ).mean()
            log_changes_std = log_volume_changes.rolling(
                window=window, min_periods=1
            ).std()

            # Calculate z-scores
            volume_z = (volume - volume_mean) / volume_std
            changes_z = (volume_changes - changes_mean) / changes_std
            log_changes_z = (log_volume_changes - log_changes_mean) / log_changes_std

            # Calculate volume spikes
            volume_ratio = volume / volume_mean
            volume_ratio_changes = volume_ratio.diff()

            # Identify anomalies
            anomalies["volume"] = pd.Series(False, index=data.index)
            anomalies["volume"][
                (abs(volume_z) > self.anomaly_threshold)
                | (abs(changes_z) > self.anomaly_threshold)
                | (abs(log_changes_z) > self.anomaly_threshold)
                | (volume_ratio > 3)
                | (volume_ratio_changes > 2)
                | (volume > volume.quantile(0.95))
            ] = True

        return anomalies

    def calculate_volatility(self, data: pd.DataFrame, window: int = 20) -> pd.Series:
        """Calculate rolling volatility.

        Args:
            data: DataFrame with 'close' price
            window: Rolling window size

        Returns:
            pd.Series: Rolling volatility
        """
        if "close" not in data.columns:
            raise ValueError("Data must contain 'close' column")

        returns = data["close"].pct_change()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
        return volatility

    def detect_trend(self, data: pd.DataFrame, window: int = 20) -> pd.Series:
        """Detect market trend using moving averages.

        Args:
            data: DataFrame with 'close' price
            window: Moving average window

        Returns:
            pd.Series: Trend direction (1: uptrend, -1: downtrend, 0: sideways)
        """
        if "close" not in data.columns:
            raise ValueError("Data must contain 'close' column")

        ma = data["close"].rolling(window=window).mean()
        trend = pd.Series(0, index=data.index)

        # Uptrend when price is above MA
        trend[data["close"] > ma] = 1

        # Downtrend when price is below MA
        trend[data["close"] < ma] = -1

        return trend

    def calculate_momentum(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate price momentum.

        Args:
            data: DataFrame with 'close' price
            period: Momentum period

        Returns:
            pd.Series: Momentum indicator
        """
        if "close" not in data.columns:
            raise ValueError("Data must contain 'close' column")

        momentum = data["close"].diff(period)
        return momentum

    def analyze_volume_profile(
        self, data: pd.DataFrame, window: int = 20
    ) -> Dict[str, pd.Series]:
        """Analyze volume profile.

        Args:
            data: DataFrame with 'close' and 'volume' data
            window: Rolling window size

        Returns:
            dict: Volume analysis metrics
        """
        if not all(col in data.columns for col in ["close", "volume"]):
            raise ValueError("Data must contain 'close' and 'volume' columns")

        # Calculate volume metrics
        avg_volume = data["volume"].rolling(window=window).mean()
        volume_trend = data["volume"] / avg_volume

        # Calculate price-volume correlation
        returns = data["close"].pct_change()
        volume_returns = data["volume"].pct_change()
        correlation = returns.rolling(window=window).corr(volume_returns)

        return {
            "average_volume": avg_volume,
            "volume_trend": volume_trend,
            "price_volume_correlation": correlation,
        }

    def identify_support_resistance(
        self, data: pd.DataFrame, window: int = 20, num_points: int = 5
    ) -> Tuple[pd.Series, pd.Series]:
        """Identify support and resistance levels.

        Args:
            data: DataFrame with OHLC data
            window: Rolling window size
            num_points: Number of points to confirm level

        Returns:
            tuple: (support_levels, resistance_levels)
        """
        if not all(col in data.columns for col in ["high", "low"]):
            raise ValueError("Data must contain 'high' and 'low' columns")

        # Calculate rolling min/max
        rolling_low = data["low"].rolling(window=window).min()
        rolling_high = data["high"].rolling(window=window).max()

        # Identify support levels (local minima)
        support = pd.Series(np.nan, index=data.index)
        for i in range(num_points, len(data) - num_points):
            if all(rolling_low.iloc[i - num_points : i] >= rolling_low.iloc[i]) and all(
                rolling_low.iloc[i + 1 : i + num_points + 1] > rolling_low.iloc[i]
            ):
                support.iloc[i] = rolling_low.iloc[i]

        # Identify resistance levels (local maxima)
        resistance = pd.Series(np.nan, index=data.index)
        for i in range(num_points, len(data) - num_points):
            if all(
                rolling_high.iloc[i - num_points : i] <= rolling_high.iloc[i]
            ) and all(
                rolling_high.iloc[i + 1 : i + num_points + 1] < rolling_high.iloc[i]
            ):
                resistance.iloc[i] = rolling_high.iloc[i]

        return support, resistance

    def calculate_market_strength(
        self, data: pd.DataFrame, window: int = 14
    ) -> pd.Series:
        """Calculate market strength indicator (ADX).

        Args:
            data: DataFrame with OHLC data
            window: Rolling window size

        Returns:
            pd.Series: Market strength indicator (ADX)
        """
        if not all(col in data.columns for col in ["high", "low", "close"]):
            raise ValueError("Data must contain 'high', 'low', and 'close' columns")

        # Calculate true range
        high_low = data["high"] - data["low"]
        high_close = abs(data["high"] - data["close"].shift(1))
        low_close = abs(data["low"] - data["close"].shift(1))

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=window, min_periods=1).mean()

        # Calculate directional movement
        high_diff = data["high"].diff()
        low_diff = -data["low"].diff()

        # Calculate positive and negative directional movement
        pos_dm = pd.Series(0, index=data.index)
        neg_dm = pd.Series(0, index=data.index)

        pos_dm[(high_diff > 0) & (high_diff > low_diff)] = high_diff
        neg_dm[(low_diff > 0) & (low_diff > high_diff)] = low_diff

        # Calculate smoothed directional movement
        pos_dm_avg = pos_dm.rolling(window=window, min_periods=1).mean()
        neg_dm_avg = neg_dm.rolling(window=window, min_periods=1).mean()

        # Calculate directional indicators
        pdi = 100 * pos_dm_avg / atr
        ndi = 100 * neg_dm_avg / atr

        # Handle division by zero
        pdi = pdi.fillna(0)
        ndi = ndi.fillna(0)

        # Calculate directional index
        di_diff = abs(pdi - ndi)
        di_sum = pdi + ndi

        # Avoid division by zero
        dx = pd.Series(0, index=data.index)
        valid_sum = di_sum > 0
        dx[valid_sum] = 100 * di_diff[valid_sum] / di_sum[valid_sum]

        # Calculate ADX (smoothed DX)
        adx = dx.rolling(window=window, min_periods=1).mean()

        # Ensure non-negative values and cap at 100
        adx = np.clip(adx, 0, 100)

        return adx
