from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any
from datetime import datetime
import numpy as np
import logging


class BaseStrategy(ABC):
    """Base class for all trading strategies."""

    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        self.name = self.__class__.__name__

    @abstractmethod
    def generate_signals(
        self, df: pd.DataFrame, symbol: str, **kwargs
    ) -> Dict[str, Any]:
        """Generate trading signals for a given symbol."""
        pass

    @abstractmethod
    def backtest(
        self, historical_data: Dict[str, pd.DataFrame], **kwargs
    ) -> Dict[str, Any]:
        """Run backtest for the strategy."""
        pass

    def calculate_performance_metrics(self, signals: pd.DataFrame) -> Dict[str, float]:
        """Calculate standard performance metrics."""
        total_return = (1 + signals["strategy_returns"]).prod() - 1
        annual_return = (1 + total_return) ** (252 / len(signals)) - 1
        sharpe_ratio = (
            np.sqrt(252)
            * signals["strategy_returns"].mean()
            / signals["strategy_returns"].std()
        )

        return {
            "total_return": float(total_return),
            "annual_return": float(annual_return),
            "sharpe_ratio": float(sharpe_ratio),
            "num_trades": int(abs(signals["signal"]).sum()),
        }

    def calculate_portfolio_metrics(
        self, signals_dict: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """Calculate portfolio-level metrics."""
        returns = [s["performance"]["total_return"] for s in signals_dict.values()]
        sharpe_ratios = [
            s["performance"]["sharpe_ratio"] for s in signals_dict.values()
        ]

        return {
            "mean_return": float(np.mean(returns)),
            "std_return": float(np.std(returns)),
            "mean_sharpe": float(np.mean(sharpe_ratios)),
            "best_symbol": max(
                signals_dict.items(),
                key=lambda x: x[1]["performance"]["total_return"],
            )[0],
            "worst_symbol": min(
                signals_dict.items(),
                key=lambda x: x[1]["performance"]["total_return"],
            )[0],
        }
