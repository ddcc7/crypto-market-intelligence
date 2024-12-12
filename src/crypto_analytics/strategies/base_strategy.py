from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Union


class BaseStrategy(ABC):
    """Abstract base class for trading strategies."""

    def __init__(self):
        """Initialize strategy."""
        pass

    @staticmethod
    def initialize_ma(prices: pd.Series, period: int) -> pd.Series:
        """Initialize moving average with high correlation to price.

        Args:
            prices: Series of prices
            period: Moving average period

        Returns:
            pd.Series: Initialized moving average
        """
        # Calculate regular MA
        ma = prices.rolling(window=period, min_periods=1).mean()

        # For the initial period, use exponentially weighted values
        if len(prices) > period:
            # Calculate weights with stronger emphasis on recent prices
            weights = np.exp(np.linspace(-2, 0, period))
            weights = weights / weights.sum()

            # Calculate initial values using exponential weights
            for i in range(period):
                if i == 0:
                    ma.iloc[i] = prices.iloc[i]
                else:
                    window = prices.iloc[: i + 1]
                    w = weights[-(i + 1) :]
                    w = w / w.sum()
                    ma.iloc[i] = np.sum(window * w)

            # Smooth the transition between initialization and regular MA
            alpha = np.linspace(0, 1, period)
            regular_ma = prices.rolling(window=period).mean()
            for i in range(period, period * 2):
                if i < len(ma):
                    blend = alpha[i - period]
                    ma.iloc[i] = (1 - blend) * ma.iloc[i - 1] + blend * regular_ma.iloc[
                        i
                    ]

        return ma

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals.

        Args:
            data: DataFrame with price data

        Returns:
            pd.Series: Trading signals (1: buy, -1: sell, 0: hold)
        """
        pass

    @abstractmethod
    def backtest(self, data: pd.DataFrame) -> Dict:
        """Backtest the strategy.

        Args:
            data: DataFrame with price data

        Returns:
            dict: Backtest results
        """
        pass

    def calculate_returns(self, data: pd.DataFrame) -> pd.Series:
        """Calculate returns from price data.

        Args:
            data: DataFrame with 'close' price

        Returns:
            pd.Series: Returns
        """
        if "close" not in data.columns:
            raise ValueError("Data must contain 'close' column")

        # Calculate returns and handle first value
        returns = data["close"].pct_change()
        returns.iloc[0] = 0  # Set first return to 0 instead of NaN

        return returns

    def calculate_metrics(self, data: pd.DataFrame, signals: pd.Series) -> Dict:
        """Calculate performance metrics.

        Args:
            data: DataFrame with price data
            signals: Series of trading signals

        Returns:
            dict: Performance metrics
        """
        returns = self.calculate_returns(data)
        strategy_returns = returns * signals.shift(1).fillna(
            0
        )  # Fill first signal with 0

        # Calculate metrics
        total_return = (1 + strategy_returns).prod() - 1
        annualized_return = (1 + total_return) ** (252 / len(data)) - 1
        volatility = strategy_returns.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility if volatility != 0 else 0

        # Calculate drawdown
        cumulative = (1 + strategy_returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdowns = cumulative / rolling_max - 1
        max_drawdown = drawdowns.min()

        # Calculate win rate
        winning_trades = (strategy_returns > 0).sum()
        total_trades = (signals != 0).sum()
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        return {
            "performance": {
                "total_return": float(total_return),
                "annualized_return": float(annualized_return),
                "volatility": float(volatility),
                "sharpe_ratio": float(sharpe_ratio),
                "max_drawdown": float(max_drawdown),
                "win_rate": float(win_rate),
                "num_trades": int(total_trades),
            }
        }
