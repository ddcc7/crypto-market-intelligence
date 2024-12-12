"""Tests for market analysis utilities."""

import unittest
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
from crypto_analytics.utils import MarketAnalyzer


class TestMarketAnalysis(unittest.TestCase):
    """Test cases for market analysis."""

    def setUp(self):
        """Set up test data."""
        self.analyzer = MarketAnalyzer()

        # Create sample OHLCV data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        self.sample_data = pd.DataFrame(
            {
                "close": np.random.randn(len(dates)).cumsum() + 100,
                "high": np.random.randn(len(dates)).cumsum() + 102,
                "low": np.random.randn(len(dates)).cumsum() + 98,
                "volume": np.random.randint(1000, 10000, len(dates)),
            },
            index=dates,
        )

    def test_market_stats_calculation(self):
        """Test market statistics calculation."""
        stats = self.analyzer.calculate_market_stats(self.sample_data)

        self.assertIsInstance(stats, dict)
        self.assertIn("returns", stats)
        self.assertIn("trading_range", stats)
        self.assertIn("volume", stats)
        self.assertIn("trend", stats)

        # Check returns metrics
        returns = stats["returns"]
        self.assertIn("daily_mean", returns)
        self.assertIn("daily_std", returns)
        self.assertIn("annualized_return", returns)
        self.assertIn("annualized_volatility", returns)

        # Check volume metrics
        volume = stats["volume"]
        self.assertIn("average_volume", volume)
        self.assertIn("volume_volatility", volume)
        self.assertIn("volume_trend", volume)

    def test_anomaly_detection(self):
        """Test anomaly detection."""
        # Create data with obvious anomalies
        anomalous_data = self.sample_data.copy()

        # Add extreme price movements
        anomalous_data.loc[anomalous_data.index[10], "close"] = anomalous_data[
            "close"
        ].mean() + (anomalous_data["close"].std() * 4)
        anomalous_data.loc[anomalous_data.index[20], "close"] = anomalous_data[
            "close"
        ].mean() - (anomalous_data["close"].std() * 4)

        # Add extreme volume
        anomalous_data.loc[anomalous_data.index[30], "volume"] = (
            anomalous_data["volume"].mean() * 5
        )

        anomalies = self.analyzer.detect_anomalies(anomalous_data)

        # Check structure
        self.assertIsInstance(anomalies, dict)
        self.assertIn("price_movements", anomalies)
        self.assertIn("volume", anomalies)

        # Check anomaly detection
        price_anomalies = anomalies["price_movements"]
        self.assertTrue(price_anomalies[anomalous_data.index[10]])
        self.assertTrue(price_anomalies[anomalous_data.index[20]])

        volume_anomalies = anomalies["volume"]
        self.assertTrue(volume_anomalies[anomalous_data.index[30]])

    def test_trend_detection(self):
        """Test trend detection."""
        trend = self.analyzer.detect_trend(self.sample_data)

        self.assertIsInstance(trend, pd.Series)
        self.assertEqual(len(trend), len(self.sample_data))
        self.assertTrue(all(trend.isin([-1, 0, 1])))

    def test_volume_profile(self):
        """Test volume profile analysis."""
        profile = self.analyzer.analyze_volume_profile(self.sample_data)

        self.assertIsInstance(profile, dict)
        self.assertIn("average_volume", profile)
        self.assertIn("volume_trend", profile)
        self.assertIn("price_volume_correlation", profile)

    def test_support_resistance(self):
        """Test support and resistance level identification."""
        support, resistance = self.analyzer.identify_support_resistance(
            self.sample_data
        )

        self.assertIsInstance(support, pd.Series)
        self.assertIsInstance(resistance, pd.Series)
        self.assertEqual(len(support), len(self.sample_data))
        self.assertEqual(len(resistance), len(self.sample_data))

    def test_market_strength(self):
        """Test market strength calculation."""
        strength = self.analyzer.calculate_market_strength(self.sample_data)

        self.assertIsInstance(strength, pd.Series)
        self.assertEqual(len(strength), len(self.sample_data))
        self.assertTrue((strength >= 0).all())


if __name__ == "__main__":
    unittest.main()
