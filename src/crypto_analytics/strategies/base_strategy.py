from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..indicators import BaseIndicator


class BaseStrategy(ABC):
    """Base class for all trading strategies."""

    def __init__(self, indicators: Optional[List[BaseIndicator]] = None):
        """Initialize strategy with optional indicators."""
        self.indicators = indicators or []
        self.current_position = 0

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate signals based on indicators.

        Args:
            data: DataFrame with price data

        Returns:
            DataFrame with signals and indicator values
        """
        # Validate input data
        if "close" not in data.columns:
            raise ValueError("Input data must contain 'close' price column")
        if len(data) == 0:
            raise ValueError("Input data is empty")

        # Initialize signals DataFrame
        signals = pd.DataFrame(index=data.index)
        signals["price"] = data["close"]
        signals["signal"] = 0  # Initialize with no position

        # Calculate indicator values
        for indicator in self.indicators:
            indicator_data = indicator.calculate(data)
            # Add indicator columns to signals DataFrame
            for col in indicator_data.columns:
                signals[col] = indicator_data[col]

        return signals

    @abstractmethod
    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on indicator values.

        Args:
            signals: DataFrame with price and indicator values

        Returns:
            DataFrame with updated signal column
        """
        pass

    def generate_signals(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate trading signals and calculate performance.

        Args:
            data: DataFrame with price data

        Returns:
            Dictionary with signal generation results
        """
        # Calculate signals
        signals = self.calculate_signals(data)
        signals = self.generate_signal_rules(signals)

        # Calculate returns and performance metrics
        signals["position"] = signals["signal"].cumsum()
        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        # Get latest signal information
        latest = signals.iloc[-1].to_dict()
        latest["timestamp"] = signals.index[-1]

        # Calculate performance metrics
        performance = self.calculate_performance_metrics(signals)

        # Get strategy parameters
        parameters = {}
        for indicator in self.indicators:
            parameters[indicator.__class__.__name__] = indicator.params

        return {
            "symbol": "CRYPTO",  # Placeholder for now
            "strategy": self.__class__.__name__,
            "timestamp": datetime.now(),
            "parameters": parameters,
            "performance": performance,
            "current_position": signals["position"].iloc[-1],
            "latest_signal": latest,
        }

    def calculate_performance_metrics(self, signals: pd.DataFrame) -> Dict[str, float]:
        """Calculate strategy performance metrics.

        Args:
            signals: DataFrame with signals and returns

        Returns:
            Dictionary of performance metrics
        """
        # Calculate basic metrics
        total_return = (1 + signals["strategy_returns"]).prod() - 1
        annualized_return = (1 + total_return) ** (252 / len(signals)) - 1
        volatility = signals["strategy_returns"].std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility if volatility != 0 else 0

        # Calculate drawdown
        cumulative_returns = (1 + signals["strategy_returns"]).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns / rolling_max - 1
        max_drawdown = drawdowns.min()

        # Calculate win rate and number of trades
        trades = signals["signal"].fillna(0) != 0
        num_trades = trades.sum()
        winning_trades = ((signals["strategy_returns"] > 0) & trades).sum()
        win_rate = winning_trades / num_trades if num_trades > 0 else 0

        return {
            "total_return": total_return,
            "annualized_return": annualized_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "num_trades": num_trades,
        }
