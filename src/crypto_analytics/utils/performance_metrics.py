import numpy as np
import pandas as pd
from typing import Dict, Any
from ..config.config_manager import ConfigManager


class PerformanceMetrics:
    """Calculates trading strategy performance metrics."""

    def __init__(self, config: ConfigManager = None):
        self.config = config or ConfigManager()
        self.annualization_factor = self.config.get(
            "performance.annualization_factor", 252
        )
        self.risk_free_rate = self.config.get("performance.risk_free_rate", 0.02)

    def calculate_returns(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Calculate strategy returns."""
        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]
        return signals

    def calculate_metrics(self, signals: pd.DataFrame) -> Dict[str, float]:
        """Calculate comprehensive performance metrics."""
        if "strategy_returns" not in signals.columns:
            signals = self.calculate_returns(signals)

        strategy_returns = signals["strategy_returns"].dropna()

        # Basic metrics
        total_return = (1 + strategy_returns).prod() - 1
        annual_return = (1 + total_return) ** (
            self.annualization_factor / len(signals)
        ) - 1

        # Risk metrics
        volatility = strategy_returns.std() * np.sqrt(self.annualization_factor)
        sharpe_ratio = (
            (annual_return - self.risk_free_rate) / volatility if volatility != 0 else 0
        )
        max_drawdown = self.calculate_max_drawdown(strategy_returns)

        # Trading metrics
        num_trades = int(abs(signals["signal"]).sum())
        win_rate = self.calculate_win_rate(strategy_returns)

        return {
            "total_return": float(total_return),
            "annual_return": float(annual_return),
            "volatility": float(volatility),
            "sharpe_ratio": float(sharpe_ratio),
            "max_drawdown": float(max_drawdown),
            "num_trades": num_trades,
            "win_rate": float(win_rate),
        }

    def calculate_portfolio_metrics(
        self, signals_dict: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """Calculate portfolio-level performance metrics."""
        returns = []
        sharpe_ratios = []
        symbols = []

        for symbol, data in signals_dict.items():
            perf = data["performance"]
            returns.append(perf["total_return"])
            sharpe_ratios.append(perf["sharpe_ratio"])
            symbols.append(symbol)

        returns_array = np.array(returns)

        return {
            "mean_return": float(np.mean(returns_array)),
            "std_return": float(np.std(returns_array)),
            "mean_sharpe": float(np.mean(sharpe_ratios)),
            "portfolio_sharpe": (
                float(np.mean(returns_array) / np.std(returns_array))
                if np.std(returns_array) != 0
                else 0
            ),
            "best_symbol": symbols[np.argmax(returns_array)],
            "worst_symbol": symbols[np.argmin(returns_array)],
            "correlation_matrix": self.calculate_correlation_matrix(signals_dict),
        }

    def calculate_max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown."""
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdowns = cumulative / rolling_max - 1
        return float(drawdowns.min())

    def calculate_win_rate(self, returns: pd.Series) -> float:
        """Calculate strategy win rate."""
        winning_trades = (returns > 0).sum()
        total_trades = len(returns[returns != 0])
        return winning_trades / total_trades if total_trades > 0 else 0

    def calculate_correlation_matrix(
        self, signals_dict: Dict[str, Dict]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate correlation matrix between symbols."""
        returns_dict = {}
        for symbol, data in signals_dict.items():
            if "signals" in data and "strategy_returns" in data["signals"]:
                returns_dict[symbol] = data["signals"]["strategy_returns"]

        if returns_dict:
            returns_df = pd.DataFrame(returns_dict)
            corr_matrix = returns_df.corr().round(3)
            return corr_matrix.to_dict()
        return {}
