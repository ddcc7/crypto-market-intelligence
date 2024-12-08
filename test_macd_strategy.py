from crypto_analytics import CryptoAnalytics
import pandas as pd
import os
from pathlib import Path
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def prepare_historical_data():
    """Prepare historical data for testing."""
    data_dir = Path("data/historical")
    os.makedirs(data_dir, exist_ok=True)

    # Download 2 years of data for comprehensive testing
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    symbols = ["BTC-USD", "ETH-USD", "XRP-USD"]
    historical_data = {}

    for symbol in symbols:
        try:
            logging.info(f"Downloading {symbol} data...")
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            if not df.empty:
                df = df[["Close"]].rename(columns={"Close": "close"})
                historical_data[symbol] = df
                logging.info(
                    f"Successfully downloaded {len(df)} data points for {symbol}"
                )
            else:
                logging.warning(f"No data found for {symbol}")

        except Exception as e:
            logging.error(f"Error downloading {symbol} data: {str(e)}")
            continue

    return historical_data


def print_macd_results(results: dict, period_desc: str):
    """Print MACD strategy results in a readable format."""
    print(f"\nMACD Strategy Results - {period_desc}")
    print("=" * 50)

    for symbol in results["signals"]:
        perf = results["signals"][symbol]["performance"]
        latest = results["signals"][symbol]["latest_signal"]

        print(f"\n{symbol}:")
        print(f"Total Return: {perf['total_return']*100:.2f}%")
        print(f"Annual Return: {perf['annual_return']*100:.2f}%")
        print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
        print(f"Number of Trades: {perf['num_trades']}")

        print("\nLatest Signal:")
        print(f"Price: ${latest['price']:.2f}")
        print(f"MACD Line: {latest['macd_line']:.4f}")
        print(f"Signal Line: {latest['signal_line']:.4f}")
        print(f"Histogram: {latest['histogram']:.4f}")
        print(f"Signal: {latest['signal']} (1: Buy, -1: Sell, 0: Hold)")

    if "portfolio_metrics" in results:
        print("\nPortfolio Metrics:")
        metrics = results["portfolio_metrics"]
        print(f"Mean Return: {metrics['mean_return']*100:.2f}%")
        print(f"Return Std Dev: {metrics['std_return']*100:.2f}%")
        print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")
        print(f"Best Symbol: {metrics['best_symbol']}")
        print(f"Worst Symbol: {metrics['worst_symbol']}")


def main():
    # Create output directory
    output_dir = Path("data/analysis_results")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize analyzer
    analyzer = CryptoAnalytics(output_dir=output_dir)

    # Prepare historical data
    logging.info("Preparing historical data...")
    historical_data = prepare_historical_data()

    if not historical_data:
        logging.error("No historical data available. Exiting...")
        return

    # Test different MACD parameter combinations
    parameter_sets = [
        # Standard settings
        {"fast": 12, "slow": 26, "signal": 9, "desc": "Standard (12/26/9)"},
        # Faster response
        {"fast": 8, "slow": 17, "signal": 9, "desc": "Fast (8/17/9)"},
        # Slower, more stable
        {"fast": 19, "slow": 39, "signal": 9, "desc": "Slow (19/39/9)"},
    ]

    # Run backtests with different parameters
    for params in parameter_sets:
        logging.info(f"\nTesting MACD strategy with {params['desc']} parameters...")
        try:
            results = analyzer.backtest_macd_strategy(
                historical_data,
                fast_period=params["fast"],
                slow_period=params["slow"],
                signal_period=params["signal"],
            )
            print_macd_results(results, params["desc"])
        except Exception as e:
            logging.error(f"Error testing MACD strategy: {str(e)}")
            continue

    logging.info(f"\nResults saved to {output_dir}/predictions.json")


if __name__ == "__main__":
    main()
