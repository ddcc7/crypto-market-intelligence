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


def print_bollinger_results(results: dict, window: int, num_std: float):
    """Helper function to print Bollinger Bands strategy results."""
    perf = results["performance"]
    print(f"\nBollinger Bands (Window: {window}, StdDev: {num_std}):")
    print(f"Total Returns: {perf['total_return']*100:.2f}%")
    print(f"Annual Returns: {perf['annual_return']*100:.2f}%")
    print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
    print(f"Number of Trades: {perf['num_trades']}")

    # Print latest signal details
    latest = results["latest_signal"]
    print("\nLatest Signal:")
    print(f"Price: ${latest['price']:.4f}")
    print(f"Upper Band: ${latest['upper_band']:.4f}")
    print(f"Middle Band: ${latest['middle_band']:.4f}")
    print(f"Lower Band: ${latest['lower_band']:.4f}")
    print(f"Signal: {latest['signal']} (1: Buy, -1: Sell, 0: Hold)")


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

    # Test Bollinger Bands strategy with different parameters
    window_std_pairs = [
        (20, 2.0),  # Standard settings
        (10, 1.5),  # Faster, tighter bands
        (50, 2.5),  # Slower, wider bands
    ]

    print("\nTesting Bollinger Bands strategy...")
    for window, num_std in window_std_pairs:
        try:
            # Run Bollinger Bands backtest
            results = analyzer.backtest_bollinger_strategy(
                historical_data, window=window, num_std=num_std
            )

            # Print results for XRP
            if "XRP" in results["signals"]:
                print_bollinger_results(results["signals"]["XRP"], window, num_std)

                print("\nPortfolio Metrics:")
                metrics = results["portfolio_metrics"]
                print(f"Mean Return: {metrics['mean_return']*100:.2f}%")
                print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")

            print("\n" + "=" * 50)  # Separator between parameter pairs

        except Exception as e:
            print(
                f"Error testing Bollinger Bands for window={window}, std={num_std}: {str(e)}"
            )


if __name__ == "__main__":
    main()
