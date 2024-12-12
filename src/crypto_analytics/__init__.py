"""Cryptocurrency market analysis package."""

import pandas as pd
from typing import Dict, List, Optional, Union

from .strategies import (
    BaseStrategy,
    MACDStrategy,
    BollingerStrategy,
    EMAStrategy,
    SMAStrategy,
    StochasticStrategy,
)
from .utils import DataManager, DataValidator, MarketAnalyzer, PerformanceMetrics


class CryptoAnalytics:
    """Main class for cryptocurrency market analysis."""

    def __init__(self):
        """Initialize CryptoAnalytics."""
        self.data_manager = DataManager()
        self.data_validator = DataValidator()
        self.market_analyzer = MarketAnalyzer()
        self.performance_metrics = PerformanceMetrics()

        # Initialize available strategies
        self.strategies = {
            "macd": MACDStrategy(),
            "bollinger": BollingerStrategy(),
            "ema": EMAStrategy(),
            "sma": SMAStrategy(),
            "stochastic": StochasticStrategy(),
        }

    def load_data(self, data: Union[pd.DataFrame, str]) -> pd.DataFrame:
        """Load and validate data.

        Args:
            data: DataFrame or path to data file

        Returns:
            pd.DataFrame: Validated data
        """
        data = self.data_manager.load_data(data)
        self.data_validator.validate_ohlcv_data(data)
        return data

    def analyze_market(self, data: pd.DataFrame) -> Dict:
        """Perform market analysis.

        Args:
            data: DataFrame with OHLC data

        Returns:
            dict: Market analysis results
        """
        results = {}

        # Calculate market metrics
        results["volatility"] = self.market_analyzer.calculate_volatility(data)
        results["trend"] = self.market_analyzer.detect_trend(data)
        results["momentum"] = self.market_analyzer.calculate_momentum(data)
        results["volume_profile"] = self.market_analyzer.analyze_volume_profile(data)
        results["support_resistance"] = (
            self.market_analyzer.identify_support_resistance(data)
        )
        results["market_strength"] = self.market_analyzer.calculate_market_strength(
            data
        )

        return results

    def backtest_strategy(
        self, data: pd.DataFrame, strategy_name: str, **strategy_params
    ) -> pd.DataFrame:
        """Backtest a trading strategy.

        Args:
            data: DataFrame with OHLC data
            strategy_name: Name of the strategy to use
            **strategy_params: Strategy-specific parameters

        Returns:
            pd.DataFrame: Backtest results
        """
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy = self.strategies[strategy_name]

        # Update strategy parameters if provided
        for param, value in strategy_params.items():
            if hasattr(strategy, param):
                setattr(strategy, param, value)

        return strategy.backtest(data)

    def run_all_strategies(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Run all available strategies.

        Args:
            data: DataFrame with OHLC data

        Returns:
            dict: Results for each strategy
        """
        results = {}
        for name, strategy in self.strategies.items():
            results[name] = strategy.backtest(data)
        return results


__all__ = ["CryptoAnalytics"]
