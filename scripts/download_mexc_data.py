#!/usr/bin/env python3

from crypto_analytics.utils.crypto_data_ingestion import CryptoDataIngestion
import logging
from datetime import datetime
import time


def main():
    # Initialize data ingestion
    ingestion = CryptoDataIngestion()

    # Define trading pairs to download (MEXC format without underscore)
    trading_pairs = [
        "BTCUSDT",  # Bitcoin
        "ETHUSDT",  # Ethereum
        "SOLUSDT",  # Solana
        "AVAXUSDT",  # Avalanche
        "POLYUSDT",  # Polygon (MATIC)
    ]

    # Define timeframes to download
    timeframes = ["4h"]  # 4-hour candles

    for symbol in trading_pairs:
        for interval in timeframes:
            logging.info(f"Downloading {symbol} data for {interval} timeframe...")

            try:
                # Get historical data
                df = ingestion.get_mexc_historical_data(
                    symbol=symbol,
                    interval=interval,
                    limit=1000,  # Maximum allowed limit
                )

                if df is not None and not df.empty:
                    # Generate filename with symbol, interval and timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"mexc_{symbol.lower()}_{interval}_{timestamp}"

                    # Save to CSV
                    ingestion.save_to_csv(df, filename)
                    logging.info(f"Successfully saved {symbol} {interval} data to CSV")
                else:
                    logging.error(f"No data received for {symbol} {interval}")

            except Exception as e:
                logging.error(f"Error downloading {symbol} {interval} data: {str(e)}")

            # Add a small delay between requests to avoid rate limits
            time.sleep(1)


if __name__ == "__main__":
    main()
