"""Data validation utilities for cryptocurrency analysis."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union


class DataValidator:
    """Validates data for cryptocurrency analysis."""

    def __init__(self, required_columns: Optional[List[str]] = None):
        """Initialize DataValidator.

        Args:
            required_columns: List of required columns
        """
        self.required_columns = required_columns or ["close", "high", "low", "volume"]

    def validate_data(self, data: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate data for analysis.

        Args:
            data: DataFrame to validate

        Returns:
            tuple: (is_valid, list of validation messages)
        """
        messages = []

        # Check if DataFrame is empty
        if data.empty:
            messages.append("Data is empty")
            return False, messages

        # Check required columns
        missing_columns = [
            col for col in self.required_columns if col not in data.columns
        ]
        if missing_columns:
            messages.append(f"Missing required columns: {missing_columns}")
            return False, messages

        # Check for null values
        null_columns = (
            data[self.required_columns]
            .columns[data[self.required_columns].isnull().any()]
            .tolist()
        )
        if null_columns:
            messages.append(f"Null values found in columns: {null_columns}")
            return False, messages

        # Check for negative values in volume if present
        if "volume" in self.required_columns and "volume" in data.columns:
            if (data["volume"] < 0).any():
                messages.append("Negative values found in volume column")
                return False, messages

        # Check for negative prices
        price_columns = [
            col
            for col in ["close", "high", "low", "open"]
            if col in self.required_columns
        ]
        for col in price_columns:
            if (data[col] < 0).any():
                messages.append(f"Negative values found in {col} column")
                return False, messages

        # Check price relationships if OHLC data is present
        if all(col in data.columns for col in ["high", "low", "close"]):
            invalid_prices = (
                (data["high"] < data["low"])
                | (data["close"] > data["high"])
                | (data["close"] < data["low"])
            )
            if invalid_prices.any():
                messages.append("Invalid price relationships found")
                return False, messages

        # All validations passed
        messages.append("Data validation successful")
        return True, messages

    def validate_ohlcv_data(self, data: pd.DataFrame) -> bool:
        """Validate OHLCV (Open, High, Low, Close, Volume) data.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            bool: True if data is valid

        Raises:
            ValueError: If data is invalid
        """
        required_columns = ["open", "high", "low", "close", "volume"]

        # Check if DataFrame is empty
        if data.empty:
            raise ValueError("Data is empty")

        # Check required columns
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Check for null values
        null_columns = (
            data[required_columns]
            .columns[data[required_columns].isnull().any()]
            .tolist()
        )
        if null_columns:
            raise ValueError(f"Null values found in columns: {null_columns}")

        # Validate price relationships
        invalid_prices = (
            (data["high"] < data["low"])
            | (data["close"] > data["high"])
            | (data["close"] < data["low"])
            | (data["open"] > data["high"])
            | (data["open"] < data["low"])
        )

        if invalid_prices.any():
            invalid_dates = data.index[invalid_prices].tolist()
            raise ValueError(
                f"Invalid price relationships found at dates: {invalid_dates}"
            )

        # Validate volume
        if (data["volume"] < 0).any():
            invalid_dates = data.index[data["volume"] < 0].tolist()
            raise ValueError(f"Negative volume found at dates: {invalid_dates}")

        return True

    def validate_timeframe(self, data: pd.DataFrame, expected_freq: str) -> bool:
        """Validate time series frequency.

        Args:
            data: DataFrame with time series data
            expected_freq: Expected frequency (e.g., '1D', '1H')

        Returns:
            bool: True if frequency is valid

        Raises:
            ValueError: If frequency is invalid
        """
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("Index must be DatetimeIndex")

        inferred_freq = pd.infer_freq(data.index)
        if inferred_freq != expected_freq:
            raise ValueError(
                f"Invalid frequency. Expected {expected_freq}, got {inferred_freq}"
            )

        return True

    def validate_indicators(
        self, data: pd.DataFrame, required_indicators: List[str]
    ) -> bool:
        """Validate technical indicators in data.

        Args:
            data: DataFrame with indicator data
            required_indicators: List of required indicator column names

        Returns:
            bool: True if indicators are valid

        Raises:
            ValueError: If indicators are invalid
        """
        # Check required columns
        missing_indicators = [
            ind for ind in required_indicators if ind not in data.columns
        ]
        if missing_indicators:
            raise ValueError(f"Missing required indicators: {missing_indicators}")

        # Check for null values
        null_indicators = (
            data[required_indicators]
            .columns[data[required_indicators].isnull().any()]
            .tolist()
        )
        if null_indicators:
            raise ValueError(f"Null values found in indicators: {null_indicators}")

        return True

    def validate_returns(self, returns: Union[pd.Series, pd.DataFrame]) -> bool:
        """Validate return calculations.

        Args:
            returns: Series or DataFrame of returns

        Returns:
            bool: True if returns are valid

        Raises:
            ValueError: If returns are invalid
        """
        if isinstance(returns, pd.DataFrame):
            returns = returns.iloc[:, 0]  # Take first column if DataFrame

        # Check for null values
        if returns.isnull().any():
            null_dates = returns.index[returns.isnull()].tolist()
            raise ValueError(f"Null values found in returns at dates: {null_dates}")

        # Check for infinite values
        if np.isinf(returns).any():
            inf_dates = returns.index[np.isinf(returns)].tolist()
            raise ValueError(f"Infinite values found in returns at dates: {inf_dates}")

        return True
