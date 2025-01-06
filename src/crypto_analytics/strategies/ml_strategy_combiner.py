"""ML-based strategy combiner using gradient boosting."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import json
from datetime import datetime
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from .base_strategy import BaseStrategy
from .macd_strategy import MACDStrategy
from .bollinger_strategy import BollingerStrategy
from ..indicators import MACD, BollingerBands


class MLStrategyCombiner(BaseStrategy):
    """ML-based strategy combiner using gradient boosting."""

    def __init__(
        self,
        lookback_period: int = 30,
        prediction_threshold: float = 0.65,
        position_size: float = 1.0,
        stop_loss: float = 0.015,
        take_profit: float = 0.035,
    ):
        """Initialize ML strategy combiner.

        Args:
            lookback_period: Period for feature engineering
            prediction_threshold: Threshold for signal generation
            position_size: Maximum position size
            stop_loss: Stop loss percentage
            take_profit: Take profit percentage
        """
        super().__init__()
        self.lookback_period = lookback_period
        self.prediction_threshold = prediction_threshold
        self.position_size = position_size
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        # Initialize strategies
        self.strategies = {
            "macd": MACDStrategy(),
            "bollinger": BollingerStrategy(),
        }

        # Initialize indicators with optimized parameters
        self.indicators = [
            MACD(
                {
                    "fast_period": 8,  # Faster response to price changes
                    "slow_period": 21,  # Better trend capture
                    "signal_period": 5,  # Quicker signal generation
                }
            ),
            BollingerBands(
                {"window": 20, "num_std": 2.5}  # Wider bands for stronger signals
            ),
        ]

        # Initialize ML model with optimized parameters
        self.model = GradientBoostingClassifier(
            n_estimators=200,  # More trees for better accuracy
            learning_rate=0.05,  # Slower learning rate for better generalization
            max_depth=4,  # Slightly deeper trees
            subsample=0.8,  # Random sampling of training data
            min_samples_split=20,  # Prevent overfitting
            min_samples_leaf=10,  # Prevent overfitting
            random_state=42,
        )
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for ML model.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with features
        """
        features = pd.DataFrame(index=data.index)

        # Add technical indicator features
        signals = data.copy()
        signals["price"] = signals["close"]

        # Calculate indicator features
        for indicator in self.indicators:
            indicator_data = indicator.calculate(data)
            if isinstance(indicator_data, pd.DataFrame):
                for col in indicator_data.columns:
                    signals[col] = indicator_data[col]
                    features[f"{indicator.__class__.__name__}_{col}"] = indicator_data[
                        col
                    ]
            else:
                signals[indicator.__class__.__name__] = indicator_data
                features[indicator.__class__.__name__] = indicator_data

        # Add strategy signals
        for name, strategy in self.strategies.items():
            strategy_signals = strategy.generate_signal_rules(signals)
            features[f"{name}_signal"] = strategy_signals["signal"]

        # Enhanced price-based features
        features["returns"] = data["close"].pct_change(fill_method=None)
        features["log_returns"] = np.log1p(data["close"]).diff()

        # Volatility features
        returns = features["returns"]
        features["volatility"] = returns.rolling(self.lookback_period).std()
        features["volatility_long"] = returns.rolling(self.lookback_period * 2).std()
        features["volatility_ratio"] = (
            features["volatility"] / features["volatility_long"]
        )

        # Momentum features
        for period in [5, 10, 20, 30]:
            features[f"momentum_{period}"] = data["close"].pct_change(
                period, fill_method=None
            )
            features[f"volume_momentum_{period}"] = data["volume"].pct_change(
                period, fill_method=None
            )

        # Trend features
        features["trend"] = np.where(data["close"] > data["close"].shift(1), 1, -1)
        features["trend_strength"] = (
            features["trend"].rolling(self.lookback_period).mean()
        )
        features["trend_consistency"] = abs(features["trend_strength"])

        # Price level features
        for period in [5, 10, 20]:
            features[f"price_distance_ma_{period}"] = (
                data["close"] - data["close"].rolling(period).mean()
            ) / data["close"].rolling(period).mean()

        # Volume features
        features["volume_trend"] = data["volume"].pct_change(fill_method=None)
        features["volume_ma"] = data["volume"].rolling(self.lookback_period).mean()
        features["relative_volume"] = data["volume"] / features["volume_ma"]
        features["volume_trend_strength"] = (
            features["volume_trend"].rolling(self.lookback_period).mean()
        )

        # Candlestick features
        features["body_size"] = abs(data["close"] - data["open"]) / data["open"]
        features["upper_shadow"] = (
            data["high"] - data[["open", "close"]].max(axis=1)
        ) / data["open"]
        features["lower_shadow"] = (
            data[["open", "close"]].min(axis=1) - data["low"]
        ) / data["open"]
        features["body_upper_ratio"] = features["body_size"] / features[
            "upper_shadow"
        ].replace(0, np.nan)
        features["body_lower_ratio"] = features["body_size"] / features[
            "lower_shadow"
        ].replace(0, np.nan)

        # Range features
        features["daily_range"] = (data["high"] - data["low"]) / data["open"]
        features["range_ma"] = (
            features["daily_range"].rolling(self.lookback_period).mean()
        )
        features["relative_range"] = features["daily_range"] / features["range_ma"]

        # Handle NaN values with forward fill then zero
        features = features.ffill().fillna(0)

        return features

    def prepare_labels(self, data: pd.DataFrame) -> pd.Series:
        """Prepare labels for ML model training with enhanced logic.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Series with labels (1 for up, -1 for down, 0 for hold)
        """
        # Calculate forward returns for multiple periods
        future_returns = pd.Series(0, index=data.index)

        # Weight different time horizons
        weights = {1: 0.4, 2: 0.3, 3: 0.2, 5: 0.1}

        for period, weight in weights.items():
            period_returns = (
                data["close"]
                .shift(-period)
                .pct_change(period, fill_method=None)
                .shift(period)
            )
            future_returns += period_returns * weight

        labels = pd.Series(0, index=data.index)

        # Dynamic thresholds based on volatility
        volatility = data["close"].pct_change(fill_method=None).rolling(20).std()
        up_threshold = self.prediction_threshold / 100 + volatility
        down_threshold = -self.prediction_threshold / 100 - volatility

        # Generate labels with dynamic thresholds
        labels[future_returns > up_threshold] = 1
        labels[future_returns < down_threshold] = -1

        return labels

    def train(self, data: pd.DataFrame) -> None:
        """Train the ML model.

        Args:
            data: DataFrame with OHLCV data
        """
        features = self.prepare_features(data)
        labels = self.prepare_labels(data)

        # Remove NaN values
        valid_idx = ~(features.isna().any(axis=1) | labels.isna())
        features = features[valid_idx]
        labels = labels[valid_idx]

        # Scale features
        self.scaler.fit(features)
        scaled_features = self.scaler.transform(features)

        # Train model
        self.model.fit(scaled_features, labels)
        self.is_trained = True

    def generate_signal_rules(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on ML model predictions.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with signals and positions
        """
        if not self.is_trained:
            self.train(data)

        # Prepare features and generate predictions
        features = self.prepare_features(data)
        scaled_features = self.scaler.transform(features)
        predictions = self.model.predict(scaled_features)
        probabilities = self.model.predict_proba(scaled_features)

        # Initialize signals DataFrame
        signals = pd.DataFrame(index=data.index)
        signals["signal"] = pd.Series(0, index=data.index)
        signals["position"] = pd.Series(0, index=data.index)

        # Generate signals based on predictions and confidence
        for i in range(len(signals)):
            if i < self.lookback_period:
                continue

            max_prob = np.max(probabilities[i])
            if max_prob > self.prediction_threshold:
                signals.iloc[i, signals.columns.get_loc("signal")] = predictions[i]

            # Update position
            if i > 0:
                new_position = (
                    signals.iloc[i - 1]["position"] + signals.iloc[i]["signal"]
                )
                signals.iloc[i, signals.columns.get_loc("position")] = np.clip(
                    new_position, -self.position_size, self.position_size
                )

        return signals

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate trading signals using ML model.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with signals and positions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before generating signals")

        # Copy input data to preserve original
        signals = data.copy()

        # Add technical indicators
        for indicator in self.indicators:
            indicator_data = indicator.calculate(data)
            if isinstance(indicator_data, pd.DataFrame):
                for col in indicator_data.columns:
                    signals[col] = indicator_data[col]
            else:
                signals[indicator.__class__.__name__] = indicator_data

        # Generate predictions
        features = self.prepare_features(data)
        scaled_features = self.scaler.transform(features)
        predictions = self.model.predict(scaled_features)
        probabilities = self.model.predict_proba(scaled_features)

        # Initialize signal and position columns
        signals["signal"] = pd.Series(0, index=signals.index)
        signals["position"] = pd.Series(0, index=signals.index)

        # Generate signals based on predictions and confidence
        for i in range(len(signals)):
            if i < self.lookback_period:
                continue

            max_prob = np.max(probabilities[i])
            if max_prob > self.prediction_threshold:
                signals.iloc[i, signals.columns.get_loc("signal")] = predictions[i]

            # Update position
            if i > 0:
                new_position = (
                    signals.iloc[i - 1]["position"] + signals.iloc[i]["signal"]
                )
                signals.iloc[i, signals.columns.get_loc("position")] = np.clip(
                    new_position, -self.position_size, self.position_size
                )

        # Calculate returns
        signals["returns"] = signals["close"].pct_change(fill_method=None)
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        # Apply stop loss and take profit
        for i in range(1, len(signals)):
            if signals.iloc[i - 1]["position"] != 0:
                returns = (
                    signals.iloc[i]["close"] - signals.iloc[i - 1]["close"]
                ) / signals.iloc[i - 1]["close"]

                if returns * signals.iloc[i - 1]["position"] <= -self.stop_loss:
                    # Stop loss hit
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0
                    signals.iloc[i, signals.columns.get_loc("strategy_returns")] = (
                        -self.stop_loss
                    )
                elif returns * signals.iloc[i - 1]["position"] >= self.take_profit:
                    # Take profit hit
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0
                    signals.iloc[i, signals.columns.get_loc("strategy_returns")] = (
                        self.take_profit
                    )

        return signals

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals for the strategy.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with signals and positions
        """
        if not self.is_trained:
            self.train(data)

        return self.calculate_signals(data)

    def backtest(self, data: pd.DataFrame) -> Dict:
        """Backtest the ML strategy.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Dict with performance metrics
        """
        signals = self.generate_signals(data)

        # Calculate metrics
        returns = signals["strategy_returns"].dropna()

        if len(returns) == 0:
            return {
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0,
                "max_drawdown": 0.0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "total_return": 0.0,
                "volatility": 0.0,
                "trades": 0,
            }

        # Calculate performance metrics
        total_return = (1 + returns).prod() - 1
        volatility = returns.std() * np.sqrt(252)
        sharpe = (
            returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0
        )

        downside_returns = returns[returns < 0]
        sortino = (
            returns.mean() * np.sqrt(252) / downside_returns.std()
            if len(downside_returns) > 0 and downside_returns.std() != 0
            else 0
        )

        cum_returns = (1 + returns).cumprod()
        rolling_max = cum_returns.expanding().max()
        drawdowns = (cum_returns - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()

        win_rate = (returns > 0).mean()
        profit_factor = (
            abs(returns[returns > 0].sum()) / abs(returns[returns < 0].sum())
            if len(returns[returns < 0]) > 0
            else float("inf")
        )
        profit_factor = min(profit_factor, 1000.0)

        trades = len(signals[signals["signal"] != 0])

        metrics = {
            "sharpe_ratio": float(sharpe),
            "sortino_ratio": float(sortino),
            "max_drawdown": float(max_drawdown),
            "win_rate": float(win_rate),
            "profit_factor": float(profit_factor),
            "total_return": float(total_return),
            "volatility": float(volatility),
            "trades": trades,
        }

        # Save results to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"results/ml_strategy_results_{timestamp}.json"

        with open(results_file, "w") as f:
            json.dump(metrics, f, indent=4)

        return metrics
