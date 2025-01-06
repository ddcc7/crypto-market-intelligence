"""Tests for MACD trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import MACDStrategy


class TestMACDStrategy(unittest.TestCase):
    """Test cases for MACD strategy."""

    def setUp(self):
        """Set up test data."""
        self.strategy = MACDStrategy()

        # Create sample data with a clear trend for testing
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        n_points = len(dates)

        # Create a price series with clear trends
        trend = np.concatenate(
            [
                np.linspace(100, 120, n_points // 3),  # Uptrend
                np.linspace(120, 90, n_points // 3),  # Downtrend
                np.linspace(90, 110, n_points - 2 * (n_points // 3)),  # Recovery
            ]
        )

        # Add some noise to make it more realistic
        noise = np.random.normal(0, 1, n_points) * 0.5
        prices = trend + noise

        self.test_data = pd.DataFrame({"close": prices}, index=dates)

    def test_signal_generation(self):
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

        # Check performance metrics
        perf = results["performance"]
        self.assertIn("total_return", perf)
        self.assertIn("annualized_return", perf)
        self.assertIn("volatility", perf)
        self.assertIn("sharpe_ratio", perf)
        self.assertIn("max_drawdown", perf)
        self.assertIn("win_rate", perf)
        self.assertIn("num_trades", perf)

        # Check latest signal
        latest = results["latest_signal"]
        self.assertIn("timestamp", latest)
        self.assertIn("price", latest)
        self.assertIn("macd_line", latest)
        self.assertIn("signal_line", latest)
        self.assertIn("histogram", latest)
        self.assertIn("signal", latest)
        self.assertTrue(latest["signal"] in [-1, 0, 1])

    def test_trend_following(self):
        """Test trend following behavior."""
        # Create trending data
        trend_data = pd.DataFrame(
            index=pd.date_range(start="2023-01-01", periods=100, freq="D")
        )

        # Strong uptrend
        trend_data["close"] = (
            np.linspace(100, 200, 100) + np.random.normal(0, 1, 100) * 0.5
        )
        up_results = self.strategy.generate_signals(trend_data)

        # Strong downtrend
        trend_data["close"] = (
            np.linspace(200, 100, 100) + np.random.normal(0, 1, 100) * 0.5
        )
        down_results = self.strategy.generate_signals(trend_data)

        # Verify trend following behavior
        self.assertGreaterEqual(
            up_results["current_position"], 0
        )  # Should be long or flat in uptrend
        self.assertLessEqual(
            down_results["current_position"], 0
        )  # Should be short or flat in downtrend

    def test_parameter_sensitivity(self):
        """Test strategy with different parameters."""
        # Test with faster parameters
        fast_strategy = MACDStrategy(
            {"fast_period": 8, "slow_period": 17, "signal_period": 9}
        )
        fast_results = fast_strategy.generate_signals(self.test_data)

        # Test with slower parameters
        slow_strategy = MACDStrategy(
            {"fast_period": 19, "slow_period": 39, "signal_period": 9}
        )
        slow_results = slow_strategy.generate_signals(self.test_data)

        # Verify both parameter sets produce valid results
        self.assertIsInstance(fast_results["performance"]["total_return"], float)
        self.assertIsInstance(slow_results["performance"]["total_return"], float)

        # Fast strategy should generate more trades
        self.assertGreater(
            fast_results["performance"]["num_trades"],
            slow_results["performance"]["num_trades"],
        )

    def test_crossover_signals(self):
        """Test MACD crossover signal generation."""
        # Create data with clear crossover points
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")

        # Create price series with multiple trends to generate crossovers
        prices = []
        base = 100

        # Uptrend
        prices.extend(np.linspace(base, base * 1.2, 20))
        # Consolidation
        prices.extend([base * 1.2] * 10)
        # Sharp downtrend
        prices.extend(np.linspace(base * 1.2, base * 0.8, 20))
        # Consolidation
        prices.extend([base * 0.8] * 10)
        # Recovery
        prices.extend(np.linspace(base * 0.8, base * 1.1, 20))
        # Final consolidation
        prices.extend([base * 1.1] * 20)

        # Add some noise
        prices = np.array(prices) + np.random.normal(0, 1, len(prices)) * 0.5

        crossover_data = pd.DataFrame({"close": prices}, index=dates)
        results = self.strategy.generate_signals(crossover_data)

        # Get the signals
        signals_df = self.strategy.calculate_signals(crossover_data)
        signals_df = self.strategy.generate_signal_rules(signals_df)

        # Verify signal properties
        self.assertTrue(any(signals_df["signal"] == 1), "Should have buy signals")
        self.assertTrue(any(signals_df["signal"] == -1), "Should have sell signals")
        self.assertTrue(
            all(signals_df["signal"].isin([-1, 0, 1])), "All signals should be valid"
        )

        # Verify that signals are generated
        self.assertGreater(
            results["performance"]["num_trades"], 0, "Should generate trades"
        )

    def test_error_handling(self):
        """Test error handling."""
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
