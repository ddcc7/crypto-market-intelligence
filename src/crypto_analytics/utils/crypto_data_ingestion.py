import requests
import pandas as pd
from datetime import datetime
import time
import logging
from pathlib import Path
import json
from crypto_analytics import CryptoAnalytics

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("crypto_ingestion.log"), logging.StreamHandler()],
)


class CryptoDataIngestion:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.output_dir = Path("data")
        self.output_dir.mkdir(exist_ok=True)
        self.analytics = CryptoAnalytics(self.output_dir)

    def _make_request(self, endpoint, params=None, max_retries=3, retry_delay=60):
        """Make API request with retry logic and rate limit handling"""
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/{endpoint}", params=params)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit exceeded
                    wait_time = int(response.headers.get("Retry-After", retry_delay))
                    logging.warning(
                        f"Rate limit reached. Waiting {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    logging.error(
                        f"Request failed with status code: {response.status_code}"
                    )
                    response.raise_for_status()

            except requests.exceptions.RequestException as e:
                logging.error(f"Request attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)

        return None

    def get_market_data(
        self, vs_currency="usd", order="market_cap_desc", per_page=250, page=1
    ):
        """Fetch market data for top cryptocurrencies"""
        endpoint = "coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": False,
        }

        return self._make_request(endpoint, params)

    def save_to_csv(self, data, filename):
        """Save data to CSV file with timestamp"""
        if not data:
            logging.error("No data to save")
            return False

        try:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.output_dir / f"{filename}_{timestamp}.csv"
            df.to_csv(filepath, index=False)
            logging.info(f"Data saved successfully to {filepath}")

            # Validate and analyze the data
            is_valid, messages = self.analytics.validate_data(df)
            for message in messages:
                logging.info(f"Validation: {message}")

            if is_valid:
                # Calculate market statistics
                stats = self.analytics.calculate_market_stats(df)
                logging.info("Market statistics calculated successfully")

                # Detect anomalies
                anomalies = self.analytics.detect_anomalies(df)
                if any(len(v) > 0 for v in anomalies.values() if isinstance(v, list)):
                    logging.warning("Anomalies detected in market data")
                else:
                    logging.info("No significant anomalies detected")

                # Save analytics results
                self.analytics.save_analytics(stats, anomalies)

            return True

        except Exception as e:
            logging.error(f"Error processing data: {str(e)}")
            return False


def main():
    ingestion = CryptoDataIngestion()

    try:
        # Fetch market data
        logging.info("Starting data ingestion...")
        market_data = ingestion.get_market_data()

        if market_data:
            # Save to CSV and perform analytics
            success = ingestion.save_to_csv(market_data, "crypto_market_data")
            if success:
                logging.info("Data ingestion and analysis completed successfully")
            else:
                logging.error("Failed to save and analyze data")
        else:
            logging.error("Failed to fetch market data")

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
