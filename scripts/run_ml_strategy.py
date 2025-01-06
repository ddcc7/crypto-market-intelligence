#!/usr/bin/env python3
"""Script to run the ML strategy combiner."""

import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import logging
from datetime import datetime
from crypto_analytics.strategies import MLStrategyCombiner

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_data(data_path: str) -> pd.DataFrame:
    """Load and prepare OHLCV data."""
    df = pd.read_csv(data_path)

    # Ensure required columns exist
    required_columns = ["timestamp", "open", "high", "low", "close", "volume"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Data must contain columns: {required_columns}")

    # Convert timestamp to datetime if needed
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Set timestamp as index
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)

    return df


def main():
    """Run ML strategy combiner."""
    try:
        # Load configuration
        config = load_config("config/trading_params.yaml")

        # Load data
        data_dir = Path("data")
        latest_file = max(data_dir.glob("*.csv"), key=lambda x: x.stat().st_mtime)
        logger.info(f"Loading data from {latest_file}")
        data = load_data(latest_file)

        # Create results directory if it doesn't exist
        Path("results").mkdir(exist_ok=True)

        # Initialize strategy
        strategy = MLStrategyCombiner(
            lookback_period=config.get("lookback_period", 20),
            prediction_threshold=config.get("prediction_threshold", 0.55),
            position_size=config.get("position_size", 1.0),
            stop_loss=config.get("stop_loss", 0.02),
            take_profit=config.get("take_profit", 0.04),
        )

        # Split data into training and testing sets
        train_size = int(len(data) * 0.7)
        train_data = data[:train_size]
        test_data = data[train_size:]

        # Train the model
        logger.info("Training ML strategy combiner...")
        strategy.train(train_data)

        # Backtest on test data
        logger.info("Running backtest on test data...")
        metrics = strategy.backtest(test_data)

        # Log performance metrics
        logger.info("\nPerformance Metrics:")
        for metric, value in metrics.items():
            logger.info(f"{metric}: {value:.4f}")

        # Generate signals for the most recent data
        recent_data = data.tail(100)
        signals = strategy.calculate_signals(recent_data)

        # Log recent signals
        logger.info("\nRecent Trading Signals:")
        recent_signals = signals[signals["signal"] != 0].tail()
        if not recent_signals.empty:
            for idx, row in recent_signals.iterrows():
                signal_type = "BUY" if row["signal"] > 0 else "SELL"
                logger.info(f"{idx}: {signal_type} - Position: {row['position']:.2f}")
        else:
            logger.info("No recent signals generated")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
