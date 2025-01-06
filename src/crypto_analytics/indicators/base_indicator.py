from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, Optional


class BaseIndicator(ABC):
    """Base class for all technical indicators."""

    def __init__(self, params: Optional[Dict[str, Any]] = None):
        """Initialize indicator with optional parameters."""
        self.params = params or {}

    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate the indicator values.

        Args:
            data: DataFrame with required price data

        Returns:
            DataFrame with indicator values
        """
        pass

    @abstractmethod
    def get_signal_thresholds(self) -> Dict[str, float]:
        """Get indicator-specific signal thresholds.

        Returns:
            Dictionary of threshold values for signal generation
        """
        pass

    def validate_data(self, data: pd.DataFrame, required_columns: list) -> None:
        """Validate input data has required columns.

        Args:
            data: Input DataFrame
            required_columns: List of required column names

        Raises:
            ValueError if required columns are missing
        """
        missing = [col for col in required_columns if col not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
