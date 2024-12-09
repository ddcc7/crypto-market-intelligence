from datetime import datetime
import logging
from typing import Dict, Any
import pandas as pd

from .base_strategy import BaseStrategy
from ..indicators.macd import MACD
from ..utils.performance_metrics import PerformanceMetrics
from ..config.config_manager import ConfigManager


class MACDStrategy(BaseStrategy):
    """MACD (Moving Average Convergence Divergence) trading strategy."""

    def __init__(self, output_dir=None):
        super().__init__(output_dir)
        self.indicator = MACD()
        self.metrics = PerformanceMetrics()
        self.config = ConfigManager()

    def generate_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        fast_period: int = None,
        slow_period: int = None,
        signal_period: int = None,
    ) -> Dict[str, Any]:
        """Generate trading signals for a symbol."""
        # Get default parameters if not provided
        params = self.config.get_strategy_params("macd")
        fast_period = fast_period or params.get("default_fast_period", 12)
        slow_period = slow_period or params.get("default_slow_period", 26)
        signal_period = signal_period or params.get("default_signal_period", 9)

        # Generate signals using MACD indicator
        signals = self.indicator.generate_signals(
            df, fast_period, slow_period, signal_period
        )

        # Calculate performance metrics
        performance = self.metrics.calculate_metrics(signals)

        return {
            "symbol": symbol,
            "strategy": self.name,
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "fast_period": fast_period,
                "slow_period": slow_period,
                "signal_period": signal_period,
            },
            "performance": performance,
            "current_position": int(signals["position"].iloc[-1]),
            "latest_signal": {
                "timestamp": signals.index[-1].isoformat(),
                "price": float(signals["price"].iloc[-1]),
                "macd_line": float(signals["macd_line"].iloc[-1]),
                "signal_line": float(signals["signal_line"].iloc[-1]),
                "histogram": float(signals["histogram"].iloc[-1]),
                "signal": int(signals["signal"].iloc[-1]),
            },
        }

    def backtest(
        self,
        historical_data: Dict[str, pd.DataFrame],
        fast_period: int = None,
        slow_period: int = None,
        signal_period: int = None,
    ) -> Dict[str, Any]:
        """Backtest MACD strategy across multiple cryptocurrencies."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "strategy": self.name,
            "parameters": {
                "fast_period": fast_period,
                "slow_period": slow_period,
                "signal_period": signal_period,
            },
            "signals": {},
        }

        # Generate signals for each symbol
        for symbol, df in historical_data.items():
            try:
                symbol_results = self.generate_signals(
                    df, symbol, fast_period, slow_period, signal_period
                )
                results["signals"][symbol] = symbol_results
            except Exception as e:
                logging.error(f"Error generating MACD signals for {symbol}: {str(e)}")
                continue

        # Calculate portfolio-level metrics
        if results["signals"]:
            results["portfolio_metrics"] = self.metrics.calculate_portfolio_metrics(
                results["signals"]
            )

        return results
