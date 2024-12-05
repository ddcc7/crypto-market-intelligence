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
        df = xrp[["High", "Low", "Close"]].rename(
            columns={"High": "high", "Low": "low", "Close": "close"}
        )
        print(f"Downloaded data shape: {df.shape}")
        print(f"Data types: {df.dtypes}")
        print(f"Sample data:\n{df.head()}")
        return {"XRP": df}

    # Load existing data
    df = pd.read_csv(data_path, skiprows=[1, 2])  # Skip Ticker and timestamp rows
    df = df.rename(
        columns={
            "Price": "timestamp",
            "High": "high",
            "Low": "low",
            "Close": "close",
        }
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df = df[["high", "low", "close"]].astype(float)

    print(f"Loaded data shape: {df.shape}")
    print(f"Data types: {df.dtypes}")
    print(f"Sample data:\n{df.head()}")
    return {"XRP": df}


def print_stochastic_results(results: dict, params: tuple):
    """Helper function to print Stochastic Oscillator results."""
    k_period, d_period = params
    perf = results["performance"]
    print(f"\nStochastic (%K: {k_period}, %D: {d_period}):")
    print(f"Total Returns: {perf['total_return']*100:.2f}%")
    print(f"Annual Returns: {perf['annual_return']*100:.2f}%")
    print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
    print(f"Number of Trades: {perf['num_trades']}")

    # Print latest signal details
    latest = results["latest_signal"]
    print("\nLatest Signal:")
    print(f"Price: ${latest['price']:.4f}")
    print(f"%K: {latest['k_line']:.2f}")
    print(f"%D: {latest['d_line']:.2f}")
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

    # Test Stochastic Oscillator with different parameters
    parameter_sets = [
        (14, 3),  # Standard settings
        (5, 3),  # Fast stochastic
        (21, 7),  # Slow stochastic
    ]

    print("\nTesting Stochastic Oscillator strategy...")
    for k_period, d_period in parameter_sets:
        try:
            # Run Stochastic backtest
            results = analyzer.backtest_stochastic_strategy(
                historical_data, k_period=k_period, d_period=d_period
            )

            # Print results for XRP
            if "XRP" in results["signals"]:
                print_stochastic_results(
                    results["signals"]["XRP"], (k_period, d_period)
                )

                print("\nPortfolio Metrics:")
                metrics = results["portfolio_metrics"]
                print(f"Mean Return: {metrics['mean_return']*100:.2f}%")
                print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")

            print("\n" + "=" * 50)  # Separator between parameter sets

        except Exception as e:
            print(
                f"Error testing Stochastic for %K={k_period}, %D={d_period}: {str(e)}"
            )

    # Compare all strategies
    print("\nComparing all strategies...")
    try:
        comparison = analyzer.compare_all_strategies(
            historical_data,
            short_window=20,  # For MA strategies
            long_window=50,
            k_period=14,  # For Stochastic
            d_period=3,
        )

        # Print comparison results
        print("\nStrategy Comparison:")
        for strategy in ["SMA", "WMA", "EMA", "Stochastic"]:
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
