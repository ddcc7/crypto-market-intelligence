from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any


class BaseIndicator(ABC):
    """Base class for all technical indicators."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Calculate the indicator values."""
        pass

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Generate trading signals based on indicator values."""
        pass

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate input data has required columns."""
        required_columns = ["close"]
        return all(col in df.columns for col in required_columns)

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for indicator calculation."""
        if not self.validate_data(df):
            raise ValueError("DataFrame missing required columns: close")
        return df.copy()
