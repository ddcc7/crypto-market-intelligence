"""Tests for Stochastic Oscillator trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import StochasticStrategy
from crypto_analytics.utils import DataManager


class TestStochasticStrategy(unittest.TestCase):
    """Test cases for Stochastic Oscillator strategy."""

    def setUp(self):
        """Set up test data."""
        self.data_manager = DataManager()
        self.strategy = StochasticStrategy()

        # Create sample data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        n_periods = len(dates)

        # Generate OHLC data
        close_prices = np.random.randn(n_periods).cumsum() + 100
        high_prices = close_prices + np.random.rand(n_periods) * 2
        low_prices = close_prices - np.random.rand(n_periods) * 2

        self.test_data = pd.DataFrame(
            {"high": high_prices, "low": low_prices, "close": close_prices}, index=dates
        )

    def test_calculate_stochastic(self):
        """Test Stochastic Oscillator calculation."""
        k_period = 14
        d_period = 3
        k, d = self.strategy.calculate_stochastic(self.test_data, k_period, d_period)

        self.assertIsInstance(k, pd.Series)
        self.assertIsInstance(d, pd.Series)
        self.assertEqual(len(k), len(self.test_data))
        self.assertEqual(len(d), len(self.test_data))

        # Test value ranges
        self.assertTrue(all((k >= 0) & (k <= 100)))
        self.assertTrue(all((d >= 0) & (d <= 100)))

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

    def test_overbought_oversold(self):
        """Test overbought and oversold conditions."""
        # Test with extreme data
        extreme_data = self.test_data.copy()

        # Create overbought condition
        extreme_data.iloc[:11]["close"] = extreme_data.iloc[:11]["high"]

        # Create oversold condition
        extreme_data.iloc[11:21]["close"] = extreme_data.iloc[11:21]["low"]

        signals = self.strategy.generate_signals(extreme_data)

        # Check for sell signals in overbought condition
        self.assertTrue(any(signals.iloc[:11] == -1))

        # Check for buy signals in oversold condition
        self.assertTrue(any(signals.iloc[11:21] == 1))


if __name__ == "__main__":
    unittest.main()
