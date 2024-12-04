import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path
import logging
from datetime import datetime


class CryptoAnalytics:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.required_columns = {
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
        }

    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the cryptocurrency market data for completeness and accuracy.

        Returns:
            Tuple[bool, List[str]]: (is_valid, list of validation messages)
        """
        messages = []

        # Check required columns
        missing_cols = self.required_columns - set(df.columns)
        if missing_cols:
            messages.append(f"Missing required columns: {missing_cols}")
            return False, messages

        # Check for null values in critical columns
        null_counts = df[list(self.required_columns)].isnull().sum()
        if null_counts.any():
            for col, count in null_counts[null_counts > 0].items():
                messages.append(f"Found {count} null values in {col}")

        # Check for data type consistency
        numeric_columns = [
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
        ]
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                messages.append(f"Column {col} is not numeric")
                return False, messages

        # Check for negative values where inappropriate
        for col in ["current_price", "market_cap", "total_volume"]:
            if (df[col] < 0).any():
                messages.append(f"Found negative values in {col}")
                return False, messages

        is_valid = len(messages) == 0
        if is_valid:
            messages.append("All validations passed successfully")

        return is_valid, messages

    def calculate_market_stats(self, df: pd.DataFrame) -> Dict:
        """
        Calculate key market statistics.
        """
        stats = {
            "timestamp": datetime.now().isoformat(),
            "market_overview": {
                "total_market_cap": float(df["market_cap"].sum()),
                "total_volume_24h": float(df["total_volume"].sum()),
                "num_cryptocurrencies": len(df),
            },
            "price_changes_24h": {
                "mean": float(df["price_change_percentage_24h"].mean()),
                "median": float(df["price_change_percentage_24h"].median()),
                "std": float(df["price_change_percentage_24h"].std()),
                "min": float(df["price_change_percentage_24h"].min()),
                "max": float(df["price_change_percentage_24h"].max()),
            },
        }

        # Calculate market dominance (top 5)
        total_market_cap = df["market_cap"].sum()
        dominance = df.nlargest(5, "market_cap")[["symbol", "market_cap"]]
        stats["market_dominance"] = {
            row["symbol"]: float(row["market_cap"] / total_market_cap * 100)
            for _, row in dominance.iterrows()
        }

        # Volume/Market Cap ratios (liquidity indicator)
        df["volume_to_mcap"] = df["total_volume"] / df["market_cap"]
        stats["liquidity_metrics"] = {
            "avg_volume_to_mcap": float(df["volume_to_mcap"].mean()),
            "median_volume_to_mcap": float(df["volume_to_mcap"].median()),
        }

        return stats

    def detect_anomalies(
        self, df: pd.DataFrame, z_score_threshold: float = 2.0
    ) -> Dict:
        """
        Detect unusual market movements using statistical methods.
        Uses a modified Z-score approach that's more sensitive to extreme values.
        """
        anomalies = {
            "timestamp": datetime.now().isoformat(),
            "price_movements": [],
            "volume_spikes": [],
            "market_cap_changes": [],
        }

        def get_outliers(series: pd.Series, threshold: float) -> List[Dict]:
            if len(series) < 2:
                return []

            # Use median and MAD for more robust outlier detection
            median = series.median()
            mad = np.median(np.abs(series - median))

            if mad == 0:  # If MAD is 0, use standard deviation instead
                std = series.std()
                if std == 0:
                    return []
                z_scores = np.abs((series - series.mean()) / std)
            else:
                # Modified Z-score using MAD
                z_scores = 0.6745 * np.abs(series - median) / mad

            outliers_idx = z_scores > threshold

            if not outliers_idx.any():
                return []

            return [
                {
                    "symbol": df.loc[idx, "symbol"],
                    "value": float(series[idx]),
                    "z_score": float(z_scores[idx]),
                }
                for idx in series[outliers_idx].index
            ]

        # Detect price change anomalies
        price_outliers = get_outliers(
            df["price_change_percentage_24h"], z_score_threshold
        )
        if price_outliers:
            anomalies["price_movements"].extend(price_outliers)

        # Detect volume spikes
        df["volume_to_mcap"] = df["total_volume"] / df["market_cap"]
        volume_outliers = get_outliers(df["volume_to_mcap"], z_score_threshold)
        if volume_outliers:
            anomalies["volume_spikes"].extend(volume_outliers)

        return anomalies

    def save_analytics(self, stats: Dict, anomalies: Dict) -> bool:
        """
        Save analytics results to JSON file.
        """
        try:
            analytics = {
                "timestamp": datetime.now().isoformat(),
                "market_stats": stats,
                "anomalies": anomalies,
            }

            filepath = self.output_dir / "analytics.json"
            with open(filepath, "w") as f:
                json.dump(analytics, f, indent=4)

            logging.info(f"Analytics saved successfully to {filepath}")
            return True

        except Exception as e:
            logging.error(f"Error saving analytics: {str(e)}")
            return False
