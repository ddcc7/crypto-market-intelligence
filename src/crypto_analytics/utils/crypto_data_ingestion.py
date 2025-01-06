import requests
import pandas as pd
from datetime import datetime
import time
import logging
from pathlib import Path
import json
import hmac
import hashlib
import os
from typing import Optional, Dict, Any
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("crypto_ingestion.log"), logging.StreamHandler()],
)


class CryptoDataIngestion:
    def __init__(self):
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.mexc_base_url = "https://api.mexc.com"
        self.output_dir = Path("data")
        self.output_dir.mkdir(exist_ok=True)

        # Load MEXC API credentials from environment variables
        self.mexc_api_key = os.getenv("mexc_id")
        self.mexc_api_secret = os.getenv("mexc_secret")

        if not self.mexc_api_key or not self.mexc_api_secret:
            logging.warning("MEXC API credentials not found in environment variables")

    def _generate_mexc_signature(self, params: Dict[str, Any]) -> str:
        """Generate signature for MEXC API authentication"""
        if not self.mexc_api_secret:
            raise ValueError("MEXC API secret is required for authenticated endpoints")

        query_string = urlencode(params)
        return hmac.new(
            self.mexc_api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _make_mexc_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Dict[str, Any] = None,
        auth_required: bool = False,
        max_retries: int = 3,
        retry_delay: int = 5,
    ):
        """Make MEXC API request with retry logic and authentication"""
        url = f"{self.mexc_base_url}/{endpoint}"
        headers = {}

        if auth_required:
            if not self.mexc_api_key:
                raise ValueError("MEXC API key is required for authenticated endpoints")

            params = params or {}
            params["timestamp"] = int(time.time() * 1000)
            params["api_key"] = self.mexc_api_key
            params["signature"] = self._generate_mexc_signature(params)
            headers["X-MEXC-APIKEY"] = self.mexc_api_key

        for attempt in range(max_retries):
            try:
                if method == "GET":
                    response = requests.get(url, params=params, headers=headers)
                elif method == "POST":
                    response = requests.post(url, json=params, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit exceeded
                    logging.warning(
                        f"Rate limit reached. Waiting {retry_delay} seconds..."
                    )
                    time.sleep(retry_delay)
                else:
                    logging.error(
                        f"MEXC API request failed with status code: {response.status_code}"
                    )
                    response.raise_for_status()

            except requests.exceptions.RequestException as e:
                logging.error(
                    f"MEXC API request attempt {attempt + 1} failed: {str(e)}"
                )
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)

        return None

    def get_mexc_historical_data(
        self, symbol: str, interval: str = "1d", limit: int = 1000
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical kline/candlestick data from MEXC

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            interval: Kline interval ('1m','5m','15m','30m','1h','4h','1d','1w','1M')
            limit: Number of records to fetch (max 1000)

        Returns:
            DataFrame with historical data or None if request fails
        """
        try:
            endpoint = "api/v3/klines"
            params = {"symbol": symbol, "interval": interval, "limit": limit}

            response = self._make_mexc_request(endpoint, params=params)

            if response:
                # Convert response to DataFrame with correct MEXC API columns
                df = pd.DataFrame(
                    response,
                    columns=[
                        "timestamp",  # Open time
                        "open",  # Open price
                        "high",  # High price
                        "low",  # Low price
                        "close",  # Close price
                        "volume",  # Volume
                        "close_time",  # Close time
                        "quote_volume",  # Quote asset volume
                    ],
                )

                # Convert timestamp to datetime
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

                # Convert numeric columns
                numeric_columns = [
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "quote_volume",
                ]
                df[numeric_columns] = df[numeric_columns].astype(float)

                return df

            return None

        except Exception as e:
            logging.error(f"Error fetching MEXC historical data: {str(e)}")
            return None

    def save_to_csv(self, data, filename):
        """Save data to CSV file with timestamp"""
        if isinstance(data, pd.DataFrame):
            try:
                filepath = self.output_dir / f"{filename}.csv"
                data.to_csv(filepath, index=False)
                logging.info(f"Data saved successfully to {filepath}")
                return True
            except Exception as e:
                logging.error(f"Error saving data to CSV: {str(e)}")
                return False
        else:
            logging.error("Data must be a pandas DataFrame")
            return False
