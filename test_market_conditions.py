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

    # Download 2 years of data to capture different market conditions
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 2 years

    symbols = ["BTC-USD", "ETH-USD", "XRP-USD"]
    historical_data = {}

    for symbol in symbols:
        try:
            logging.info(f"Downloading {symbol} data...")
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            if not df.empty:
                # Rename columns to match expected format
                df = df.rename(
                    columns={
                        "Close": "close",
                        "High": "high",
                        "Low": "low",
                        "Open": "open",
                        "Volume": "volume",
                    }
                )
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


def print_market_condition_results(results: dict):
    """Print market condition analysis results in a readable format."""
    for symbol in results["strategies"]:
        print(f"\n=== {symbol} Analysis ===")

        for strategy in results["strategies"][symbol]:
            print(f"\n{strategy} Strategy:")

            # Print overall performance
            perf = results["strategies"][symbol][strategy]["overall_performance"]
            print("\nOverall Performance:")
            print(f"Total Return: {perf['total_return']*100:.2f}%")
            print(f"Annual Return: {perf['annual_return']*100:.2f}%")
            print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
            print(f"Number of Trades: {perf['num_trades']}")

            # Print performance by market condition
            market_perf = results["strategies"][symbol][strategy][
                "market_condition_performance"
            ]
            print("\nPerformance by Market Condition:")

            for condition in market_perf["market_conditions"]:
                cond_data = market_perf["market_conditions"][condition]
                print(f"\n{condition.replace('_', ' ').title()}:")
                print(f"Number of Periods: {cond_data['periods']}")
                print(f"Average Return: {cond_data['avg_return']*100:.2f}%")
                print(f"Average Sharpe: {cond_data['avg_sharpe']:.2f}")
                print(f"Return Std Dev: {cond_data['return_std']*100:.2f}%")


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

    # Run market condition analysis
    logging.info("Running market condition analysis...")
    results = analyzer.compare_all_strategies(
        historical_data, short_window=20, long_window=50, market_window=20
    )

    # Print results
    print_market_condition_results(results)

    logging.info(f"\nResults saved to {output_dir}/predictions.json")


if __name__ == "__main__":
    main()
