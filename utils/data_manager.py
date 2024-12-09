import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
from typing import Dict, Optional


class DataManager:
    """Handles data operations for crypto analytics."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("data")
        self.historical_dir = self.output_dir / "historical"
        self.results_dir = self.output_dir / "analysis_results"
        self._setup_directories()

    def _setup_directories(self):
        """Create necessary directories if they don't exist."""
        self.historical_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def fetch_historical_data(
        self, symbols: list, period: str = "2y", interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical cryptocurrency data from Yahoo Finance.

        Args:
            symbols: List of cryptocurrency symbols
            period: Time period to download (e.g., "2y" for 2 years)
            interval: Data interval (e.g., "1d" for daily)

        Returns:
            Dict of DataFrames with historical price data
        """
        historical_data = {}

        for symbol in symbols:
            try:
                logging.info(f"Fetching data for {symbol}")
                ticker = yf.Ticker(symbol)
                df = ticker.history(period=period, interval=interval)

                if not df.empty:
                    df = df[["Close"]].rename(columns={"Close": "close"})
                    historical_data[symbol] = df
                    logging.info(
                        f"Successfully fetched {len(df)} data points for {symbol}"
                    )
                else:
                    logging.warning(f"No data found for {symbol}")

            except Exception as e:
                logging.error(f"Error fetching data for {symbol}: {e}")
                continue

        return historical_data

    def save_results(self, results: Dict, strategy_name: str):
        """Save strategy results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.results_dir / f"{strategy_name}_{timestamp}.json"

        try:
            with open(filename, "w") as f:
                json.dump(results, f, indent=4)
            logging.info(f"Results saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving results: {e}")

    def load_results(self, strategy_name: str) -> Optional[Dict]:
        """Load most recent results for a strategy."""
        try:
            files = list(self.results_dir.glob(f"{strategy_name}_*.json"))
            if not files:
                return None

            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            with open(latest_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading results: {e}")
            return None
