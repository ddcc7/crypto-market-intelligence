"""Strategy benchmarking system for evaluating trading strategies."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Type
from datetime import datetime, timedelta
from ..strategies.base_strategy import BaseStrategy
from ..strategies.bollinger_strategy import BollingerStrategy
from ..strategies.ema_strategy import EMAStrategy
from ..strategies.sma_strategy import SMAStrategy
from ..strategies.stochastic_strategy import StochasticStrategy


class StrategyBenchmark:
    """Benchmark trading strategies across multiple assets and timeframes."""

    def __init__(
        self,
        strategies: Optional[List[Type[BaseStrategy]]] = None,
        timeframes: Optional[List[str]] = None,
    ):
        """Initialize benchmark system.

        Args:
            strategies: List of strategy classes to benchmark
            timeframes: List of timeframes to test (e.g., ["1h", "4h", "1d"])
        """
        self.strategies = strategies or [
            BollingerStrategy,
            EMAStrategy,
            SMAStrategy,
            StochasticStrategy,
        ]
        self.timeframes = timeframes or ["1h", "4h", "1d"]
        self.results: Dict = {}

    def prepare_data(self, data: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Prepare data for the given timeframe.

        Args:
            data: Raw OHLCV data
            timeframe: Target timeframe

        Returns:
            Resampled data
        """
        # Convert timeframe to pandas offset
        offset_map = {
            "1m": "1T",
            "5m": "5T",
            "15m": "15T",
            "30m": "30T",
            "1h": "1H",
            "4h": "4H",
            "1d": "1D",
            "1w": "1W",
        }
        offset = offset_map.get(timeframe, "1D")

        # Resample OHLCV data
        resampled = (
            data.resample(offset)
            .agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
            .dropna()
        )

        return resampled

    def calculate_metrics(
        self, returns: pd.Series, signals: pd.Series
    ) -> Dict[str, float]:
        """Calculate comprehensive performance metrics.

        Args:
            returns: Asset returns
            signals: Strategy signals

        Returns:
            Dictionary of metrics
        """
        # Calculate strategy returns
        strategy_returns = returns * signals.shift(1)

        # Basic metrics
        total_return = (1 + strategy_returns).prod() - 1
        annual_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = strategy_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility != 0 else 0

        # Drawdown analysis
        cum_returns = (1 + strategy_returns).cumprod()
        rolling_max = cum_returns.expanding().max()
        drawdowns = (cum_returns - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()

        # Trading metrics
        trades = signals.diff().fillna(0).abs() / 2
        num_trades = trades.sum()
        win_rate = (strategy_returns > 0).mean() if num_trades > 0 else 0

        # Risk metrics
        sortino_ratio = (
            annual_return
            / (strategy_returns[strategy_returns < 0].std() * np.sqrt(252))
            if len(strategy_returns[strategy_returns < 0]) > 0
            else 0
        )

        calmar_ratio = abs(annual_return / max_drawdown) if max_drawdown != 0 else 0

        return {
            "total_return": total_return,
            "annual_return": annual_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "calmar_ratio": calmar_ratio,
            "max_drawdown": max_drawdown,
            "num_trades": num_trades,
            "win_rate": win_rate,
        }

    def run_benchmark(
        self,
        data: pd.DataFrame,
        asset_name: str,
        initial_capital: float = 10000,
        transaction_costs: float = 0.001,
    ) -> Dict:
        """Run benchmark tests for all strategies and timeframes.

        Args:
            data: OHLCV data
            asset_name: Name of the asset
            initial_capital: Initial capital for portfolio calculation
            transaction_costs: Transaction costs per trade (as fraction)

        Returns:
            Dictionary of benchmark results
        """
        results = {}

        # Calculate buy-hold baseline
        returns = data["close"].pct_change()
        buy_hold_metrics = self.calculate_metrics(
            returns, pd.Series(1, index=returns.index)
        )
        results["buy_hold"] = buy_hold_metrics

        # Test each strategy on each timeframe
        for timeframe in self.timeframes:
            # Prepare data for timeframe
            tf_data = self.prepare_data(data, timeframe)
            tf_returns = tf_data["close"].pct_change()

            for strategy_class in self.strategies:
                # Initialize strategy
                strategy = strategy_class()
                strategy_name = strategy.__class__.__name__

                try:
                    # Generate signals
                    signals = strategy.generate_signals(tf_data)

                    # Apply transaction costs
                    signal_changes = signals.diff().fillna(0).abs()
                    transaction_costs_returns = -signal_changes * transaction_costs

                    # Calculate metrics
                    metrics = self.calculate_metrics(
                        tf_returns + transaction_costs_returns, signals
                    )

                    # Store results
                    key = f"{strategy_name}_{timeframe}"
                    results[key] = metrics

                except Exception as e:
                    print(f"Error running {strategy_name} on {timeframe}: {str(e)}")
                    continue

        # Store results
        self.results[asset_name] = results
        return results

    def generate_report(self) -> pd.DataFrame:
        """Generate a comprehensive benchmark report.

        Returns:
            DataFrame with benchmark results
        """
        # Prepare data for report
        report_data = []

        for asset_name, asset_results in self.results.items():
            for strategy_name, metrics in asset_results.items():
                row = {"asset": asset_name, "strategy": strategy_name, **metrics}
                report_data.append(row)

        # Create DataFrame
        report = pd.DataFrame(report_data)

        # Sort by Sharpe ratio
        report = report.sort_values("sharpe_ratio", ascending=False)

        # Round numeric columns
        numeric_cols = [
            "total_return",
            "annual_return",
            "volatility",
            "sharpe_ratio",
            "sortino_ratio",
            "calmar_ratio",
            "max_drawdown",
            "win_rate",
        ]
        report[numeric_cols] = report[numeric_cols].round(4)

        return report

    def plot_results(self, asset_name: str, save_path: Optional[str] = None) -> None:
        """Plot benchmark results for an asset.

        Args:
            asset_name: Name of the asset to plot
            save_path: Optional path to save the plot
        """
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            import pandas as pd
            import numpy as np
        except ImportError:
            print("matplotlib and seaborn are required for plotting")
            return

        results = self.results.get(asset_name)
        if not results:
            print(f"No results found for {asset_name}")
            return

        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

        # Prepare data for plotting
        plot_data = []
        for strategy_name, metrics in results.items():
            plot_data.append(
                {
                    "Strategy": strategy_name,
                    "Total Return": metrics.get("total_return", np.nan),
                    "Sharpe Ratio": metrics.get("sharpe_ratio", np.nan),
                    "Max Drawdown": metrics.get("max_drawdown", np.nan),
                }
            )

        plot_df = pd.DataFrame(plot_data)

        # Plot returns
        sns.barplot(data=plot_df, x="Strategy", y="Total Return", ax=ax1)
        ax1.set_title(f"Total Returns by Strategy - {asset_name}")
        ax1.tick_params(axis="x", rotation=45)

        # Plot Sharpe ratios
        sns.barplot(data=plot_df, x="Strategy", y="Sharpe Ratio", ax=ax2)
        ax2.set_title(f"Sharpe Ratios by Strategy - {asset_name}")
        ax2.tick_params(axis="x", rotation=45)

        # Plot maximum drawdowns
        sns.barplot(data=plot_df, x="Strategy", y="Max Drawdown", ax=ax3)
        ax3.set_title(f"Maximum Drawdowns by Strategy - {asset_name}")
        ax3.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
        else:
            plt.show()
