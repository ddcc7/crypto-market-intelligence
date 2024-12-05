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
        xrp.to_csv(data_path)
        df = xrp[["Close"]].rename(columns={"Close": "close"})
        print(f"Downloaded data shape: {df.shape}")
        print(f"Data types: {df.dtypes}")
        print(f"Sample data:\n{df.head()}")
        return {"XRP": df}

    # Load existing data
    df = pd.read_csv(data_path, skiprows=[1, 2])  # Skip Ticker and timestamp rows
    df = df.rename(columns={"Price": "timestamp", "Close": "close"})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df = df[["close"]].astype(float)

    print(f"Loaded data shape: {df.shape}")
    print(f"Data types: {df.dtypes}")
    print(f"Sample data:\n{df.head()}")
    return {"XRP": df}


def print_strategy_results(name: str, results: dict, window_pair: tuple):
    """Helper function to print strategy results in a consistent format."""
    short_window, long_window = window_pair
    perf = results["performance"]
    print(f"\n{name} {short_window}/{long_window}:")
    print(f"Total Returns: {perf['total_return']*100:.2f}%")
    print(f"Annual Returns: {perf['annual_return']*100:.2f}%")
    print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
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

    # Test EMA strategy with different parameters
    window_pairs = [
        (10, 30),  # Short-term crossover
        (20, 50),  # Medium-term crossover
        (50, 200),  # Long-term crossover
    ]

    print("\nTesting EMA strategy...")
    for short_window, long_window in window_pairs:
        try:
            # Run EMA backtest
            results = analyzer.backtest_ema_strategy(
                historical_data, short_window=short_window, long_window=long_window
            )

            # Print results for XRP
            if "XRP" in results["signals"]:
                print_strategy_results(
                    "EMA", results["signals"]["XRP"], (short_window, long_window)
                )

                print("\nPortfolio Metrics:")
                metrics = results["portfolio_metrics"]
                print(f"Mean Return: {metrics['mean_return']*100:.2f}%")
                print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")

            print("\n" + "=" * 50)  # Separator between parameter pairs

        except Exception as e:
            print(f"Error testing EMA for {short_window}/{long_window}: {str(e)}")

    # Compare all strategies
    print("\nComparing all strategies...")
    try:
        comparison = analyzer.compare_all_strategies(
            historical_data,
            short_window=20,  # Using medium-term settings
            long_window=50,
        )

        # Print comparison results
        print("\nStrategy Comparison (20/50):")
        for strategy in ["SMA", "WMA", "EMA"]:
            metrics = comparison["strategies"][strategy]["metrics"]
            signals = comparison["strategies"][strategy]["signals"]["XRP"]

            print(f"\n{strategy} Strategy:")
            print(f"Mean Return: {metrics['mean_return']*100:.2f}%")
            print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")
            print(f"Total Return: {signals['performance']['total_return']*100:.2f}%")
            print(f"Number of Trades: {signals['performance']['num_trades']}")

    except Exception as e:
        print(f"Error comparing strategies: {str(e)}")


if __name__ == "__main__":
    main()
