import pandas as pd
import numpy as np
from pathlib import Path
from crypto_analytics import CryptoAnalytics
import yfinance as yf
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_crypto_data(symbols=["BTC-USD", "ETH-USD"], period="1y"):
    """
    Fetch historical cryptocurrency data from Yahoo Finance.
    """
    historical_data = {}

    for symbol in symbols:
        try:
            logging.info(f"Fetching data for {symbol}")
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)

            if not df.empty:
                # Ensure we have the required 'close' column
                df = df[["Close"]].rename(columns={"Close": "close"})
                historical_data[symbol] = df
                logging.info(f"Successfully fetched {len(df)} data points for {symbol}")
            else:
                logging.warning(f"No data found for {symbol}")

        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
            continue

    return historical_data


def test_sma_strategy():
    # Create output directory
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    # Initialize analytics
    analytics = CryptoAnalytics(output_dir=output_dir)

    # Fetch historical data
    symbols = ["BTC-USD", "ETH-USD", "XRP-USD", "ADA-USD"]
    historical_data = fetch_crypto_data(symbols=symbols, period="2y")

    if not historical_data:
        logging.error("No historical data fetched. Exiting test.")
        return

    logging.info("Running SMA strategy backtest...")

    # Test different SMA window combinations
    window_combinations = [
        (20, 50),  # Standard
        (10, 30),  # Faster
        (50, 200),  # Longer-term
    ]

    for short_window, long_window in window_combinations:
        logging.info(f"\nTesting SMA {short_window}/{long_window} strategy:")

        try:
            results = analytics.backtest_sma_strategy(
                historical_data, short_window=short_window, long_window=long_window
            )

            # Print summary metrics
            if "portfolio_metrics" in results:
                metrics = results["portfolio_metrics"]
                logging.info(f"Mean Return: {metrics['mean_return']:.2%}")
                logging.info(f"Return Std: {metrics['std_return']:.2%}")
                logging.info(f"Best Symbol: {metrics['best_symbol']}")
                logging.info(f"Worst Symbol: {metrics['worst_symbol']}")

                # Print individual symbol performance
                for symbol in results["signals"]:
                    perf = results["signals"][symbol]["performance"]
                    logging.info(f"\n{symbol} Performance:")
                    logging.info(f"Total Return: {perf['total_return']:.2%}")
                    logging.info(f"Annual Return: {perf['annual_return']:.2%}")
                    logging.info(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
                    logging.info(f"Number of Trades: {perf['num_trades']}")

        except Exception as e:
            logging.error(f"Error testing {short_window}/{long_window} strategy: {e}")
            continue


if __name__ == "__main__":
    test_sma_strategy()
