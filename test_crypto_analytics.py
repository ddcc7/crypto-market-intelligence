import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import json
from crypto_analytics import CryptoAnalytics


class TestCryptoAnalytics(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test outputs
        self.test_dir = Path(tempfile.mkdtemp())
        self.analytics = CryptoAnalytics(self.test_dir)

        # Create sample test data
        self.sample_data = pd.DataFrame(
            {
                "id": ["bitcoin", "ethereum", "ripple", "dogecoin", "cardano"],
                "symbol": ["btc", "eth", "xrp", "doge", "ada"],
                "name": ["Bitcoin", "Ethereum", "XRP", "Dogecoin", "Cardano"],
                "current_price": [50000.0, 3000.0, 1.0, 0.5, 2.0],
                "market_cap": [1e12, 3e11, 5e10, 1e10, 2e10],
                "total_volume": [5e10, 2e10, 1e9, 5e8, 1e9],
                "price_change_percentage_24h": [5.0, -2.0, 0.5, 1.0, -1.0],
            }
        )

    def test_data_validation_success(self):
        is_valid, messages = self.analytics.validate_data(self.sample_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(messages), 1)
        self.assertIn("All validations passed", messages[0])

    def test_data_validation_missing_columns(self):
        invalid_data = self.sample_data.drop("market_cap", axis=1)
        is_valid, messages = self.analytics.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Missing required columns", messages[0])

    def test_data_validation_negative_values(self):
        invalid_data = self.sample_data.copy()
        invalid_data.loc[0, "current_price"] = -1000
        is_valid, messages = self.analytics.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Found negative values", messages[0])

    def test_market_stats_calculation(self):
        stats = self.analytics.calculate_market_stats(self.sample_data)

        # Test market overview
        self.assertIn("market_overview", stats)
        self.assertEqual(stats["market_overview"]["num_cryptocurrencies"], 5)

        # Test price changes
        self.assertIn("price_changes_24h", stats)
        self.assertAlmostEqual(
            stats["price_changes_24h"]["mean"],
            self.sample_data["price_change_percentage_24h"].mean(),
        )

        # Test market dominance
        self.assertIn("market_dominance", stats)
        self.assertEqual(len(stats["market_dominance"]), 5)  # All coins in sample

        # Test liquidity metrics
        self.assertIn("liquidity_metrics", stats)
        self.assertTrue(stats["liquidity_metrics"]["avg_volume_to_mcap"] > 0)

    def test_anomaly_detection(self):
        # Create data with obvious anomalies
        anomalous_data = self.sample_data.copy()
        # Add extreme outliers (more than 3 standard deviations from mean)
        anomalous_data.loc[0, "price_change_percentage_24h"] = (
            150.0  # Extreme positive change
        )
        anomalous_data.loc[1, "price_change_percentage_24h"] = (
            -75.0
        )  # Extreme negative change

        anomalies = self.analytics.detect_anomalies(
            anomalous_data
        )  # Using default threshold

        # Check structure
        self.assertIn("price_movements", anomalies)
        self.assertIn("volume_spikes", anomalies)

        # Should detect both extreme price changes
        self.assertTrue(len(anomalies["price_movements"]) >= 2)
        detected_symbols = {a["symbol"] for a in anomalies["price_movements"]}
        self.assertTrue({"btc", "eth"}.issubset(detected_symbols))

    def test_analytics_saving(self):
        stats = self.analytics.calculate_market_stats(self.sample_data)
        anomalies = self.analytics.detect_anomalies(self.sample_data)

        # Test saving
        success = self.analytics.save_analytics(stats, anomalies)
        self.assertTrue(success)

        # Verify file exists and is valid JSON
        analytics_file = self.test_dir / "analytics.json"
        self.assertTrue(analytics_file.exists())

        with open(analytics_file) as f:
            saved_data = json.load(f)
            self.assertIn("market_stats", saved_data)
            self.assertIn("anomalies", saved_data)


if __name__ == "__main__":
    unittest.main()
