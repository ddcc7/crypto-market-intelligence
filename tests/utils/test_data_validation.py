"""Tests for data validation utilities."""

import unittest
import pandas as pd
import numpy as np
from crypto_analytics.utils import DataValidator


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation."""

    def setUp(self):
        """Set up test data."""
        self.validator = DataValidator()

        # Create sample data with required columns
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        n_periods = len(dates)

        # Generate valid OHLC data
        close_prices = np.random.randn(n_periods).cumsum() + 100
        high_prices = close_prices + np.abs(np.random.rand(n_periods))
        low_prices = close_prices - np.abs(np.random.rand(n_periods))
        volume = np.random.randint(1000, 10000, n_periods)

        self.sample_data = pd.DataFrame(
            {
                "close": close_prices,
                "high": high_prices,
                "low": low_prices,
                "volume": volume,
            },
            index=dates,
        )

    def test_data_validation_success(self):
        """Test successful data validation."""
        is_valid, messages = self.validator.validate_data(self.sample_data)
        self.assertTrue(is_valid)
        self.assertEqual(messages[-1], "Data validation successful")

    def test_data_validation_missing_columns(self):
        """Test data validation with missing columns."""
        invalid_data = self.sample_data.drop(["high", "low"], axis=1)
        is_valid, messages = self.validator.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Missing required columns", messages[0])

    def test_data_validation_negative_values(self):
        """Test data validation with negative values."""
        invalid_data = self.sample_data.copy()
        invalid_data.loc[invalid_data.index[0], "close"] = -100
        is_valid, messages = self.validator.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Negative values found", messages[0])

    def test_data_validation_null_values(self):
        """Test data validation with null values."""
        invalid_data = self.sample_data.copy()
        invalid_data.loc[invalid_data.index[0], "close"] = np.nan
        is_valid, messages = self.validator.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Null values found", messages[0])

    def test_data_validation_invalid_price_relationships(self):
        """Test data validation with invalid price relationships."""
        invalid_data = self.sample_data.copy()
        invalid_data.loc[invalid_data.index[0], "high"] = 90
        invalid_data.loc[invalid_data.index[0], "low"] = 110
        is_valid, messages = self.validator.validate_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Invalid price relationships found", messages[0])

    def test_data_validation_empty_data(self):
        """Test data validation with empty data."""
        empty_data = pd.DataFrame()
        is_valid, messages = self.validator.validate_data(empty_data)
        self.assertFalse(is_valid)
        self.assertEqual(messages[0], "Data is empty")


if __name__ == "__main__":
    unittest.main()
