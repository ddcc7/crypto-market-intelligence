from crypto_analytics import CryptoAnalytics
import pandas as pd
import os
from pathlib import Path
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np


def prepare_historical_data():
    # Create historical data directory if it doesn't exist
    data_dir = Path("data/historical")
    os.makedirs(data_dir, exist_ok=True)

    data_path = data_dir / "XRP_historical.csv"

    if not data_path.exists():
        # Download data if it doesn't exist
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Get 1 year of data

        xrp = yf.download("XRP-USD", start=start_date, end=end_date)
        # Save with datetime index
        xrp.index = xrp.index.strftime("%Y-%m-%d %H:%M:%S")
        xrp.to_csv(data_path)
        df = xrp[["Close"]].rename(columns={"Close": "close"})
        df.index = pd.to_datetime(df.index)
        print(f"Downloaded data shape: {df.shape}")
        print(f"Data types: {df.dtypes}")
        print(f"Sample data:\n{df.head()}")
        return {"XRP": df}

    # Load existing data
    df = pd.read_csv(data_path)
    print(f"Initial columns: {df.columns.tolist()}")

    # Clean up the data
    df = df[df["Price"].str.match(r"\d{4}-\d{2}-\d{2}.*").fillna(False)]
    df = df.rename(columns={"Price": "timestamp", "Close": "close"})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df["close"] = pd.to_numeric(df["close"])
    df = pd.DataFrame(df["close"])  # Ensure we have only the close column

    print(f"Loaded data shape: {df.shape}")
    print(f"Data types: {df.dtypes}")
    print(f"Sample data:\n{df.head()}")
    return {"XRP": df}


def print_strategy_results(name: str, results: dict, window_pair: tuple):
    """Helper function to print strategy results in a consistent format."""
    short_window, long_window = window_pair
    perf = results["performance"]
    print(f"\n{name} {short_window}/{long_window}:")
    print(f"Total Returns: {perf['total_return']: .2f}%")
    print(f"Annual Returns: {perf['annual_return']: .2f}%")
    print(f"Sharpe Ratio: {perf['sharpe_ratio']: .2f}")
    print(f"Number of Trades: {perf['num_trades']}")


def main():
    # Create output directory if it doesn't exist
    output_dir = Path("data/analysis_results")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize analyzer
    analyzer = CryptoAnalytics(output_dir=output_dir)

    # Load or download historical data
    print("Preparing historical data...")
    historical_data = prepare_historical_data()
    print("Data ready!")

    # Test both strategies with different window combinations
    window_pairs = [(10, 30), (20, 50), (50, 200)]

    print("\nTesting both SMA and WMA strategies...")
    for short_window, long_window in window_pairs:
        try:
            # Compare both strategies
            comparison = analyzer.compare_strategies(
                historical_data, short_window=short_window, long_window=long_window
            )

            # Print SMA results
            sma_results = comparison["strategies"]["SMA"]["signals"]["XRP"]
            print_strategy_results("SMA", sma_results, (short_window, long_window))

            # Print WMA results
            wma_results = comparison["strategies"]["WMA"]["signals"]["XRP"]
            print_strategy_results("WMA", wma_results, (short_window, long_window))

            # Print comparison metrics
            print("\nStrategy Comparison:")
            for strategy in ["SMA", "WMA"]:
                metrics = comparison["strategies"][strategy]["metrics"]
                print(f"\n{strategy} Overall Metrics:")
                print(f"Mean Return: {metrics['mean_return']:.2f}%")
                print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")

            print("\n" + "=" * 50)  # Separator between window pairs

        except Exception as e:
            print(
                f"Error comparing strategies for {short_window}/{long_window}: {str(e)}"
            )


if __name__ == "__main__":
    main()
