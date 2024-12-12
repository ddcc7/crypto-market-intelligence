"""Tests for SMA trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import SMAStrategy
from crypto_analytics.utils import DataManager


class TestSMAStrategy(unittest.TestCase):
    """Test cases for SMA strategy."""

    def setUp(self):
        """Set up test data."""
        self.data_manager = DataManager()
        self.strategy = SMAStrategy()

        # Create sample data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        self.test_data = pd.DataFrame(
            {"close": np.random.randn(len(dates)).cumsum() + 100}, index=dates
        )

    def test_calculate_sma(self):
        """Test SMA calculation."""
        period = 20
        sma = self.strategy.calculate_sma(self.test_data, period)

        self.assertIsInstance(sma, pd.Series)
        self.assertEqual(len(sma), len(self.test_data))

        # Test that SMA follows price movements
        correlation = sma.corr(self.test_data["close"])
        self.assertGreater(correlation, 0.9)

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

    def test_trend_following(self):
        """Test trend following behavior."""
        # Test with trending data
        trend_data = self.test_data.copy()

        # Create uptrend
        trend_data.iloc[:11]["close"] = np.linspace(100, 120, 11)

        # Create downtrend
        trend_data.iloc[11:21]["close"] = np.linspace(120, 80, 10)

        signals = self.strategy.generate_signals(trend_data)

        # Check for buy signals in uptrend
        self.assertTrue(any(signals.iloc[:11] == 1))

        # Check for sell signals in downtrend
        self.assertTrue(any(signals.iloc[11:21] == -1))


if __name__ == "__main__":
    unittest.main()
