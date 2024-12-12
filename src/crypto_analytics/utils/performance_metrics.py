"""Performance metrics calculation utilities."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Union


class PerformanceMetrics:
    """Calculates trading strategy performance metrics."""

    @staticmethod
    def calculate_returns(data: pd.DataFrame) -> pd.Series:
        """Calculate returns from price data.

        Args:
            data: DataFrame with 'close' price

        Returns:
            pd.Series: Returns
        """
        if "close" not in data.columns:
            raise ValueError("Data must contain 'close' column")

        return data["close"].pct_change()

    @staticmethod
    def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:
        """Calculate cumulative returns.

        Args:
            returns: Series of returns

        Returns:
            pd.Series: Cumulative returns
        """
        return (1 + returns).cumprod() - 1

    @staticmethod
    def calculate_sharpe_ratio(
        returns: pd.Series, risk_free_rate: float = 0.0
    ) -> float:
        """Calculate Sharpe ratio.

        Args:
            returns: Series of returns
            risk_free_rate: Risk-free rate (annualized)

        Returns:
            float: Sharpe ratio
        """
        excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
        return np.sqrt(252) * (excess_returns.mean() / excess_returns.std())

    @staticmethod
    def calculate_sortino_ratio(
        returns: pd.Series, risk_free_rate: float = 0.0
    ) -> float:
        """Calculate Sortino ratio.

        Args:
            returns: Series of returns
            risk_free_rate: Risk-free rate (annualized)

        Returns:
            float: Sortino ratio
        """
        excess_returns = returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]
        downside_std = np.sqrt(np.mean(downside_returns**2))

        return (
            np.sqrt(252) * (excess_returns.mean() / downside_std)
            if downside_std != 0
            else np.inf
        )

    @staticmethod
    def calculate_max_drawdown(returns: pd.Series) -> float:
        """Calculate maximum drawdown.

        Args:
            returns: Series of returns

        Returns:
            float: Maximum drawdown
        """
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns / rolling_max - 1
        return drawdowns.min()

    @staticmethod
    def calculate_win_rate(signals: pd.Series, returns: pd.Series) -> float:
        """Calculate win rate.

        Args:
            signals: Series of trading signals
            returns: Series of returns

        Returns:
            float: Win rate
        """
        trade_returns = returns * signals.shift(1)
        winning_trades = (trade_returns > 0).sum()
        total_trades = (signals != 0).sum()

        return winning_trades / total_trades if total_trades > 0 else 0

    def calculate_all_metrics(
        self, data: pd.DataFrame, signals: pd.Series, risk_free_rate: float = 0.0
    ) -> Dict[str, float]:
        """Calculate all performance metrics.

        Args:
            data: DataFrame with 'close' price
            signals: Series of trading signals
            risk_free_rate: Risk-free rate (annualized)

        Returns:
            dict: All performance metrics
        """
        returns = self.calculate_returns(data)
        strategy_returns = returns * signals.shift(1)

        metrics = {
            "total_return": self.calculate_cumulative_returns(strategy_returns).iloc[
                -1
            ],
            "sharpe_ratio": self.calculate_sharpe_ratio(
                strategy_returns, risk_free_rate
            ),
            "sortino_ratio": self.calculate_sortino_ratio(
                strategy_returns, risk_free_rate
            ),
            "max_drawdown": self.calculate_max_drawdown(strategy_returns),
            "win_rate": self.calculate_win_rate(signals, returns),
            "volatility": strategy_returns.std() * np.sqrt(252),  # Annualized
            "avg_return": strategy_returns.mean() * 252,  # Annualized
            "num_trades": (signals != 0).sum(),
        }

        return metrics
