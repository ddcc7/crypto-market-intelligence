"""Tests for Bollinger Bands trading strategy."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.strategies import BollingerStrategy


class TestBollingerStrategy(unittest.TestCase):
    """Test cases for Bollinger Bands strategy."""

    def setUp(self):
        """Set up test data."""
        self.strategy = BollingerStrategy()

        # Create sample data with clear mean reversion patterns
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        n_points = len(dates)

        # Create a mean-reverting price series
        base = 100
        amplitude = 20
        cycles = 6  # Number of cycles in the period
        t = np.linspace(0, cycles * 2 * np.pi, n_points)
        trend = base + amplitude * np.sin(t)

        # Add some noise
        noise = np.random.normal(0, 1, n_points) * 2
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
        self.assertIn("middle_band", latest)
        self.assertIn("upper_band", latest)
        self.assertIn("lower_band", latest)
        self.assertIn("bandwidth", latest)
        self.assertIn("signal", latest)
        self.assertTrue(latest["signal"] in [-1, 0, 1])

    def test_mean_reversion(self):
        """Test mean reversion behavior."""
        # Create mean-reverting data
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")

        # Create base price series with clear trend
        base_price = 100
        prices = np.ones(100) * base_price

        # Create overbought condition (price well above mean)
        prices[10:30] = np.linspace(
            base_price, base_price * 1.3, 20
        )  # Gradual increase
        prices[30:40] = base_price * 1.3  # Stay high

        # Create oversold condition (price well below mean)
        prices[50:70] = np.linspace(
            base_price, base_price * 0.7, 20
        )  # Gradual decrease
        prices[70:80] = base_price * 0.7  # Stay low

        # Add some noise
        prices += np.random.normal(0, 1, 100) * 0.5

        reversion_data = pd.DataFrame({"close": prices}, index=dates)

        # Get the signals
        signals_df = self.strategy.calculate_signals(reversion_data)
        signals_df = self.strategy.generate_signal_rules(signals_df)

        # Check for sell signals in overbought condition (during high price period)
        overbought_signals = signals_df.iloc[30:40]["signal"]
        self.assertTrue(
            any(overbought_signals == -1),
            "Should generate sell signals in overbought condition",
        )

        # Check for buy signals in oversold condition (during low price period)
        oversold_signals = signals_df.iloc[70:80]["signal"]
        self.assertTrue(
            any(oversold_signals == 1),
            "Should generate buy signals in oversold condition",
        )

    def test_parameter_sensitivity(self):
        """Test strategy with different parameters."""
        # Test with narrow bands (more signals)
        narrow_strategy = BollingerStrategy({"window": 20, "num_std": 1.5})
        narrow_results = narrow_strategy.generate_signals(self.test_data)

        # Test with wide bands (fewer signals)
        wide_strategy = BollingerStrategy({"window": 20, "num_std": 2.5})
        wide_results = wide_strategy.generate_signals(self.test_data)

        # Verify both parameter sets produce valid results
        self.assertIsInstance(narrow_results["performance"]["total_return"], float)
        self.assertIsInstance(wide_results["performance"]["total_return"], float)

        # Narrow bands should generate more trades
        self.assertGreater(
            narrow_results["performance"]["num_trades"],
            wide_results["performance"]["num_trades"],
        )

    def test_band_behavior(self):
        """Test Bollinger Bands behavior with different volatility regimes."""
        # Create data with changing volatility
        dates = pd.date_range(start="2023-01-01", periods=200, freq="D")
        base_price = 100

        # Low volatility period
        low_vol = np.random.normal(0, 0.5, 100)
        # High volatility period
        high_vol = np.random.normal(0, 2.0, 100)

        # Combine periods
        prices = np.concatenate(
            [base_price + np.cumsum(low_vol), base_price + np.cumsum(high_vol)]
        )

        vol_data = pd.DataFrame({"close": prices}, index=dates)
        results = self.strategy.generate_signals(vol_data)

        # Get the signals
        signals_df = self.strategy.calculate_signals(vol_data)

        # Verify band properties
        band_width_low = (
            signals_df["upper_band"][:100] - signals_df["lower_band"][:100]
        ).mean()
        band_width_high = (
            signals_df["upper_band"][100:] - signals_df["lower_band"][100:]
        ).mean()

        # Bands should be wider in high volatility period
        self.assertGreater(band_width_high, band_width_low)

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
