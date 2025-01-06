"""Tests for base trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import BaseStrategy
from crypto_analytics.indicators import MACD, BollingerBands


class MockIndicator(MACD):
    """Mock indicator for testing."""

    def __init__(self):
        super().__init__({"fast_period": 12, "slow_period": 26, "signal_period": 9})


class MockStrategy(BaseStrategy):
    """Mock strategy for testing BaseStrategy."""

    def __init__(self):
        super().__init__([MockIndicator()])

    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate mock signals.

        Args:
            signals: DataFrame with price and indicator values

        Returns:
            DataFrame with updated signal column
        """
        # Simple alternating signals using iloc for positional indexing
        signals.iloc[::2, signals.columns.get_loc("signal")] = (
            1  # Buy every other period
        )
        signals.iloc[1::2, signals.columns.get_loc("signal")] = -1  # Sell in between
        return signals


class TestBaseStrategy(unittest.TestCase):
    """Test cases for base strategy."""

    def setUp(self):
        """Set up test data."""
        self.strategy = MockStrategy()

        # Create sample data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        self.test_data = pd.DataFrame(
            {"close": np.random.randn(len(dates)).cumsum() + 100}, index=dates
        )

    def test_calculate_signals(self):
        """Test signal calculation."""
        signals = self.strategy.calculate_signals(self.test_data)

        self.assertIsInstance(signals, pd.DataFrame)
        self.assertEqual(len(signals), len(self.test_data))
        self.assertIn("price", signals.columns)
        self.assertIn("signal", signals.columns)
        self.assertTrue(all(signals["signal"] == 0))  # Initial signals should be 0

        # Check indicator columns
        self.assertIn("macd_line", signals.columns)
        self.assertIn("signal_line", signals.columns)
        self.assertIn("histogram", signals.columns)

    def test_generate_signals(self):
        """Test signal generation."""
        results = self.strategy.generate_signals(self.test_data)

        self.assertIsInstance(results, dict)
        self.assertIn("symbol", results)
        self.assertIn("strategy", results)
        self.assertIn("timestamp", results)
        self.assertIn("parameters", results)
        self.assertIn("performance", results)
        self.assertIn("current_position", results)
        self.assertIn("latest_signal", results)

        # Check that parameters contain indicator parameters
        self.assertIn("MockIndicator", results["parameters"])

        # Check that latest signal contains indicator values
        latest = results["latest_signal"]
        self.assertIn("macd_line", latest)
        self.assertIn("signal_line", latest)
        self.assertIn("histogram", latest)

    def test_performance_metrics(self):
        """Test performance metrics calculation."""
        # Create signals DataFrame with different scenarios
        signals = pd.DataFrame(index=self.test_data.index)
        signals["price"] = 100  # Constant price

        # Test buy and hold
        signals["signal"] = 0  # Initialize with no position
        signals.iloc[0, signals.columns.get_loc("signal")] = (
            1  # Single buy signal at start
        )
        signals["position"] = signals["signal"].cumsum()
        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        metrics = self.strategy.calculate_performance_metrics(signals)

        self.assertEqual(metrics["total_return"], 0.0)  # No return with constant price
        self.assertEqual(
            metrics["volatility"], 0.0
        )  # No volatility with constant price
        self.assertEqual(metrics["num_trades"], 1)  # One trade (initial buy)

        # Test alternating signals
        signals["signal"] = 0  # Reset signals
        signals.iloc[::2, signals.columns.get_loc("signal")] = (
            1  # Buy every other period
        )
        signals.iloc[1::2, signals.columns.get_loc("signal")] = -1  # Sell in between
        signals["position"] = signals["signal"].cumsum()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        metrics = self.strategy.calculate_performance_metrics(signals)
        self.assertEqual(metrics["num_trades"], len(signals))  # Trade every period

    def test_multiple_indicators(self):
        """Test strategy with multiple indicators."""
        # Create strategy with both MACD and Bollinger Bands
        multi_strategy = MockStrategy()
        multi_strategy.indicators.append(BollingerBands())

        results = multi_strategy.generate_signals(self.test_data)

        # Check that indicator values from both indicators are present
        latest = results["latest_signal"]

        # MACD values
        self.assertIn("macd_line", latest)
        self.assertIn("signal_line", latest)
        self.assertIn("histogram", latest)

        # Bollinger Bands values
        self.assertIn("middle_band", latest)
        self.assertIn("upper_band", latest)
        self.assertIn("lower_band", latest)
        self.assertIn("bandwidth", latest)

    def test_error_handling(self):
        """Test error handling in base strategy."""
        # Test with missing close price
        bad_data = pd.DataFrame({"open": [1, 2, 3]})
        with self.assertRaises(ValueError):
            self.strategy.generate_signals(bad_data)

        # Test with empty DataFrame
        empty_data = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.strategy.generate_signals(empty_data)

        # Test with NaN values
        nan_data = self.test_data.copy()
        nan_data.loc[nan_data.index[0], "close"] = np.nan
        results = self.strategy.generate_signals(nan_data)
        self.assertIsInstance(results["performance"]["total_return"], float)


if __name__ == "__main__":
    unittest.main()
