"""Tests for base trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import BaseStrategy
from crypto_analytics.utils import DataManager


class MockStrategy(BaseStrategy):
    """Mock strategy for testing BaseStrategy."""

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate mock signals.

        Args:
            data: DataFrame with price data

        Returns:
            pd.Series: Mock signals
        """
        signals = pd.Series(0, index=data.index)
        signals.iloc[::2] = 1  # Buy every other period
        signals.iloc[1::2] = -1  # Sell in between
        return signals

    def backtest(self, data: pd.DataFrame) -> dict:
        """Run mock backtest.

        Args:
            data: DataFrame with price data

        Returns:
            dict: Mock backtest results
        """
        signals = self.generate_signals(data)
        metrics = self.calculate_metrics(data, signals)

        metrics.update({"signals": signals, "strategy_metrics": {"test_metric": 1.0}})

        return metrics


class TestBaseStrategy(unittest.TestCase):
    """Test cases for base strategy."""

    def setUp(self):
        """Set up test data."""
        self.data_manager = DataManager()
        self.strategy = MockStrategy()

        # Create sample data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        self.test_data = pd.DataFrame(
            {"close": np.random.randn(len(dates)).cumsum() + 100}, index=dates
        )

    def test_calculate_returns(self):
        """Test returns calculation."""
        returns = self.strategy.calculate_returns(self.test_data)

        self.assertIsInstance(returns, pd.Series)
        self.assertEqual(len(returns), len(self.test_data))
        self.assertTrue(pd.notnull(returns).all())

    def test_calculate_metrics(self):
        """Test metrics calculation."""
        signals = self.strategy.generate_signals(self.test_data)
        metrics = self.strategy.calculate_metrics(self.test_data, signals)

        self.assertIsInstance(metrics, dict)
        self.assertIn("performance", metrics)

        perf = metrics["performance"]
        self.assertIn("total_return", perf)
        self.assertIn("annualized_return", perf)
        self.assertIn("volatility", perf)
        self.assertIn("sharpe_ratio", perf)
        self.assertIn("max_drawdown", perf)
        self.assertIn("win_rate", perf)
        self.assertIn("num_trades", perf)

    def test_generate_signals(self):
        """Test signal generation."""
        signals = self.strategy.generate_signals(self.test_data)

        self.assertIsInstance(signals, pd.Series)
        self.assertEqual(len(signals), len(self.test_data))
        self.assertTrue(all(signals.isin([-1, 0, 1])))

    def test_backtest(self):
        """Test backtesting functionality."""
        results = self.strategy.backtest(self.test_data)

        self.assertIsInstance(results, dict)
        self.assertIn("signals", results)
        self.assertIn("performance", results)
        self.assertIn("strategy_metrics", results)


if __name__ == "__main__":
    unittest.main()
