"""Tests for Bollinger Bands trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import BollingerStrategy
from crypto_analytics.utils import DataManager


class TestBollingerStrategy(unittest.TestCase):
    """Test cases for Bollinger Bands strategy."""

    def setUp(self):
        """Set up test data."""
        self.data_manager = DataManager()
        self.strategy = BollingerStrategy()

        # Create sample data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        self.test_data = pd.DataFrame(
            {"close": np.random.randn(len(dates)).cumsum() + 100}, index=dates
        )

    def test_calculate_bollinger_bands(self):
        """Test Bollinger Bands calculation."""
        period = 20
        num_std = 2

        middle_band, upper_band, lower_band = self.strategy.calculate_bollinger_bands(
            self.test_data, period, num_std
        )

        self.assertIsInstance(middle_band, pd.Series)
        self.assertIsInstance(upper_band, pd.Series)
        self.assertIsInstance(lower_band, pd.Series)
        self.assertEqual(len(middle_band), len(self.test_data))

        # Test that bands follow price movements
        correlation = middle_band.corr(self.test_data["close"])
        self.assertGreater(correlation, 0.9)

        # Test band relationships
        self.assertTrue(all(upper_band >= middle_band))
        self.assertTrue(all(lower_band <= middle_band))

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

    def test_mean_reversion(self):
        """Test mean reversion behavior."""
        # Test with mean-reverting data
        reversion_data = self.test_data.copy()

        # Create overbought condition
        reversion_data.iloc[:11]["close"] = 120

        # Create oversold condition
        reversion_data.iloc[11:21]["close"] = 80

        signals = self.strategy.generate_signals(reversion_data)

        # Check for sell signals in overbought condition
        self.assertTrue(any(signals.iloc[:11] == -1))

        # Check for buy signals in oversold condition
        self.assertTrue(any(signals.iloc[11:21] == 1))


if __name__ == "__main__":
    unittest.main()
