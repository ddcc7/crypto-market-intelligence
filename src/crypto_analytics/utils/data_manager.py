"""Data management utilities for cryptocurrency analysis."""

import pandas as pd
import numpy as np
from typing import Optional, Union, Dict


class DataManager:
    """Manages data operations for cryptocurrency analysis."""

    def __init__(self):
        """Initialize DataManager."""
        self.data = None

    def load_data(self, data: Union[pd.DataFrame, str]) -> pd.DataFrame:
        """Load data from a DataFrame or file path.

        Args:
            data: DataFrame or path to data file

        Returns:
            pd.DataFrame: Loaded data
        """
        if isinstance(data, pd.DataFrame):
            self.data = data.copy()
        elif isinstance(data, str):
            # Attempt to load from file
            try:
                if data.endswith(".csv"):
                    self.data = pd.read_csv(data, parse_dates=True, index_col=0)
                elif data.endswith(".parquet"):
                    self.data = pd.read_parquet(data)
                else:
                    raise ValueError("Unsupported file format")
            except Exception as e:
                raise ValueError(f"Failed to load data: {str(e)}")
        else:
            raise ValueError("Data must be a DataFrame or file path")

        return self.data

    def validate_data(self) -> bool:
        """Validate the loaded data.

        Returns:
            bool: True if data is valid
        """
        if self.data is None:
            raise ValueError("No data loaded")

        required_columns = ["close"]
        missing_columns = [
            col for col in required_columns if col not in self.data.columns
        ]

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        return True

    def prepare_data(self, columns: Optional[list] = None) -> pd.DataFrame:
        """Prepare data for analysis.

        Args:
            columns: List of columns to include

        Returns:
            pd.DataFrame: Prepared data
        """
        if not self.validate_data():
            raise ValueError("Invalid data")

        if columns is None:
            columns = ["close"]

        missing_columns = [col for col in columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        prepared_data = self.data[columns].copy()
        prepared_data = prepared_data.dropna()

        return prepared_data

    def get_returns(self, period: int = 1) -> pd.Series:
        """Calculate returns for the specified period.

        Args:
            period: Number of periods for return calculation

        Returns:
            pd.Series: Returns
        """
        if not self.validate_data():
            raise ValueError("Invalid data")

        returns = self.data["close"].pct_change(period)
        return returns.dropna()

    def get_volatility(self, window: int = 20) -> pd.Series:
        """Calculate rolling volatility.

        Args:
            window: Rolling window size

        Returns:
            pd.Series: Volatility
        """
        if not self.validate_data():
            raise ValueError("Invalid data")

        returns = self.get_returns()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
        return volatility.dropna()

    def resample_data(self, rule: str) -> pd.DataFrame:
        """Resample data to a different frequency.

        Args:
            rule: Resampling rule (e.g., '1H', '1D')

        Returns:
            pd.DataFrame: Resampled data
        """
        if not self.validate_data():
            raise ValueError("Invalid data")

        resampled = (
            self.data.resample(rule)
            .agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
            .dropna()
        )

        return resampled
