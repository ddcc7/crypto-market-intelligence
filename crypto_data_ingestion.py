import requests
import pandas as pd
from datetime import datetime
import time
import logging
from pathlib import Path
import json

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

            # Save latest data stats with proper type conversion
            stats = {
                "timestamp": timestamp,
                "num_records": int(len(df)),
                "currencies": df["symbol"].tolist(),
                "total_market_cap": float(df["market_cap"].sum()),
            }

            with open(self.output_dir / "latest_stats.json", "w") as f:
                json.dump(stats, f, indent=4)
            logging.info("Stats saved successfully")

            return True

        except Exception as e:
            logging.error(f"Error saving data to CSV: {str(e)}")
            return False


def main():
    ingestion = CryptoDataIngestion()

    try:
        # Fetch market data
        logging.info("Starting data ingestion...")
        market_data = ingestion.get_market_data()

        if market_data:
            # Save to CSV
            success = ingestion.save_to_csv(market_data, "crypto_market_data")
            if success:
                logging.info("Data ingestion completed successfully")
            else:
                logging.error("Failed to save data")
        else:
            logging.error("Failed to fetch market data")

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
