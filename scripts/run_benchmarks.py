#!/usr/bin/env python3
"""Script to run strategy benchmarks on multiple assets."""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from pathlib import Path
import json
from crypto_analytics.benchmark.strategy_benchmark import StrategyBenchmark
import warnings
import numpy as np
from functools import partial


def ensure_dir(directory):
    """Create directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_cache_path(symbol: str, start_date: str, end_date: str) -> Path:
    """Get path for cached data file."""
    cache_dir = Path("data/cache")
    ensure_dir(cache_dir)
    cache_file = f"{symbol}_{start_date}_{end_date}.parquet"
    return cache_dir / cache_file


def download_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Download historical data from Yahoo Finance with caching and optimization.

    Args:
        symbol: Asset symbol
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        DataFrame with OHLCV data
    """
    cache_path = get_cache_path(symbol, start_date, end_date)

    # Check if cached data exists
    if cache_path.exists():
        # Use fastparquet engine for faster reading
        return pd.read_parquet(cache_path, engine="fastparquet")

    # Download if not cached
    ticker = yf.Ticker(symbol)

    # Download with progress=False to avoid printing progress bars
    data = ticker.history(start=start_date, end=end_date, interval="1h", progress=False)

    # Optimize memory usage by using appropriate dtypes
    float_cols = ["open", "high", "low", "close"]
    data = data.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    # Optimize dtypes
    for col in float_cols:
        data[col] = data[col].astype("float32")
    data["volume"] = data["volume"].astype("int32")

    # Cache the data using fastparquet
    data.to_parquet(cache_path, engine="fastparquet", compression="snappy")
    return data


def prepare_data_for_timeframe(data: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Optimized data preparation for a specific timeframe."""
    offset_map = {
        "1m": "1T",
        "5m": "5T",
        "15m": "15T",
        "30m": "30T",
        "1h": "1H",
        "4h": "4H",
        "1d": "1D",
        "1w": "1W",
    }
    offset = offset_map.get(timeframe, "1D")

    # Use numpy operations for faster calculations
    grouped = data.groupby(pd.Grouper(freq=offset))
    resampled = pd.DataFrame(
        {
            "open": grouped["open"].first(),
            "high": grouped["high"].max(),
            "low": grouped["low"].min(),
            "close": grouped["close"].last(),
            "volume": grouped["volume"].sum(),
        }
    )

    return resampled.dropna()


def process_strategy(
    strategy_class, data: pd.DataFrame, timeframes: list, transaction_costs: float
):
    """Process a single strategy across all timeframes."""
    strategy_results = {}
    strategy = strategy_class() if strategy_class else None

    for timeframe in timeframes:
        try:
            # Prepare data for timeframe
            tf_data = prepare_data_for_timeframe(data.copy(), timeframe)

            if strategy_class:
                # Generate signals for strategy
                signals = strategy.generate_signals(tf_data)
            else:
                # Buy and hold strategy (always invested)
                signals = pd.Series(1, index=tf_data.index)

            # Calculate returns and costs
            returns = tf_data["close"].pct_change()

            if strategy_class:
                # Apply transaction costs for active strategies
                signal_changes = signals.diff().fillna(0).abs()
                transaction_costs_returns = -signal_changes * transaction_costs
            else:
                # Buy and hold only pays transaction costs once at the start
                transaction_costs_returns = pd.Series(
                    0.0, index=returns.index, dtype="float64"
                )
                transaction_costs_returns.iloc[0] = -float(transaction_costs)

            # Calculate metrics
            strategy_returns = returns * signals.shift(1)
            adjusted_returns = strategy_returns + transaction_costs_returns

            metrics = calculate_metrics(adjusted_returns)
            strategy_name = (
                strategy.__class__.__name__ if strategy_class else "BuyAndHold"
            )
            strategy_results[f"{strategy_name}_{timeframe}"] = metrics

        except Exception as e:
            strategy_name = (
                strategy.__class__.__name__ if strategy_class else "BuyAndHold"
            )
            print(f"Error in {strategy_name} for {timeframe}: {str(e)}")
            continue

    return strategy_results


def calculate_metrics(returns: pd.Series) -> dict:
    """Vectorized calculation of performance metrics."""
    # Basic metrics
    total_return = (1 + returns).prod() - 1
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)

    # Use numpy for faster calculations
    neg_returns = returns[returns < 0]
    downside_vol = neg_returns.std() * np.sqrt(252) if len(neg_returns) > 0 else 1e-6

    # Calculate drawdown using numpy operations
    cum_returns = (1 + returns).cumprod()
    rolling_max = np.maximum.accumulate(cum_returns)
    drawdowns = (cum_returns - rolling_max) / rolling_max
    max_drawdown = drawdowns.min()

    # Trading metrics
    trades = returns.diff().fillna(0).abs()
    num_trades = (trades != 0).sum()
    win_rate = (returns > 0).mean() if num_trades > 0 else 0

    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "volatility": volatility,
        "sharpe_ratio": annual_return / volatility if volatility != 0 else 0,
        "sortino_ratio": annual_return / downside_vol if downside_vol != 0 else 0,
        "calmar_ratio": abs(annual_return / max_drawdown) if max_drawdown != 0 else 0,
        "max_drawdown": max_drawdown,
        "num_trades": num_trades,
        "win_rate": win_rate,
    }


def process_asset(args):
    """Process a single asset with optimized strategy processing."""
    symbol, start_date, end_date, timeframes, transaction_costs = args
    try:
        print(f"Downloading data for {symbol}...")
        data = download_data(symbol, start_date, end_date)

        print(f"Running benchmark for {symbol}...")
        benchmark = StrategyBenchmark(timeframes=timeframes)

        # Process strategies in parallel
        with ThreadPoolExecutor() as executor:
            strategy_futures = []

            # Add buy and hold strategy
            future = executor.submit(
                process_strategy,
                None,  # None represents buy and hold
                data,
                timeframes,
                transaction_costs,
            )
            strategy_futures.append(future)

            # Add active strategies
            for strategy_class in benchmark.strategies:
                future = executor.submit(
                    process_strategy,
                    strategy_class,
                    data,
                    timeframes,
                    transaction_costs,
                )
                strategy_futures.append(future)

            # Combine results
            all_results = {}
            for future in as_completed(strategy_futures):
                all_results.update(future.result())

        # Convert results to DataFrame
        results_df = pd.DataFrame(
            [
                {"asset": symbol, "strategy": strategy_name, **metrics}
                for strategy_name, metrics in all_results.items()
            ]
        )

        # Store results in benchmark object for plotting
        benchmark.results = {symbol: all_results}

        return {
            "symbol": symbol,
            "success": True,
            "results": results_df,
            "benchmark": benchmark,
        }
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")
        return {"symbol": symbol, "success": False, "error": str(e)}


def main():
    # Suppress warnings
    warnings.filterwarnings("ignore")

    start_time = time.time()

    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create output directory
    output_dir = Path(f"benchmarks/run_{timestamp}")
    ensure_dir(output_dir)

    # Define test assets
    assets = [
        "BTC-USD",  # Bitcoin
        "ETH-USD",  # Ethereum
        "BNB-USD",  # Binance Coin
        "SOL-USD",  # Solana
        "ADA-USD",  # Cardano
    ]

    # Define parameters
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    timeframes = ["1h", "4h", "1d"]
    transaction_costs = 0.001  # 0.1% transaction cost

    # Prepare arguments for parallel processing
    process_args = [
        (symbol, start_date, end_date, timeframes, transaction_costs)
        for symbol in assets
    ]

    # Process assets in parallel using ProcessPoolExecutor
    results = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_asset, args) for args in process_args]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            if result["success"]:
                symbol = result["symbol"]
                benchmark = result["benchmark"]
                # Save plots with optimized settings
                benchmark.plot_results(
                    symbol, save_path=str(output_dir / f"{symbol}_results.png")
                )

    # Combine all successful results
    successful_results = [r for r in results if r["success"]]
    if successful_results:
        # Generate and save report
        combined_report = pd.concat([r["results"] for r in successful_results])

        # Add timeframe column for better analysis
        combined_report["timeframe"] = combined_report["strategy"].apply(
            lambda x: x.split("_")[-1]
        )
        combined_report["strategy_name"] = combined_report["strategy"].apply(
            lambda x: "_".join(x.split("_")[:-1])
        )

        # Sort by asset and timeframe for better readability
        combined_report = combined_report.sort_values(
            ["asset", "timeframe", "sharpe_ratio"], ascending=[True, True, False]
        )

        # Save full report
        report_path = output_dir / "benchmark_results.csv"
        combined_report.to_csv(report_path, index=False)

        # Print summary statistics
        print("\nTop 5 Strategy-Timeframe Combinations by Sharpe Ratio:")
        top_5 = combined_report.nlargest(5, "sharpe_ratio")[
            [
                "asset",
                "strategy_name",
                "timeframe",
                "total_return",
                "annual_return",
                "sharpe_ratio",
                "max_drawdown",
                "num_trades",
                "win_rate",
            ]
        ]
        print(top_5.to_string())
        top_5.to_csv(output_dir / "top_5_sharpe.csv", index=False)

        print("\nWorst 5 Strategy-Timeframe Combinations by Maximum Drawdown:")
        worst_5 = combined_report.nlargest(5, "max_drawdown")[
            [
                "asset",
                "strategy_name",
                "timeframe",
                "total_return",
                "annual_return",
                "sharpe_ratio",
                "max_drawdown",
                "num_trades",
                "win_rate",
            ]
        ]
        print(worst_5.to_string())
        worst_5.to_csv(output_dir / "worst_5_drawdown.csv", index=False)

        # Print buy and hold comparison
        print("\nBuy and Hold Performance by Asset (1d timeframe):")
        buy_hold = combined_report[
            (combined_report["strategy_name"] == "BuyAndHold")
            & (combined_report["timeframe"] == "1d")
        ][["asset", "total_return", "annual_return", "sharpe_ratio", "max_drawdown"]]
        print(buy_hold.to_string())
        buy_hold.to_csv(output_dir / "buy_hold_performance.csv", index=False)

    # Save run metadata
    run_time = time.time() - start_time
    metadata = {
        "timestamp": timestamp,
        "run_time_seconds": run_time,
        "assets_processed": len(assets),
        "successful_assets": len(successful_results),
        "failed_assets": len([r for r in results if not r["success"]]),
        "timeframes_tested": timeframes,
        "date_range": f"{start_date} to {end_date}",
    }

    with open(output_dir / "run_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nBenchmark completed in {run_time:.2f} seconds")
    print(f"Results saved in: {output_dir}")


if __name__ == "__main__":
    main()
