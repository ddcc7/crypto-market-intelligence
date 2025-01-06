"""Benchmark script for evaluating trading strategies."""

import sys
import os
import time
import json
import glob
import memory_profiler
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import itertools

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crypto_analytics.strategies import BreakoutStrategy, MLStrategyCombiner


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""

    def default(self, obj):
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.bool_)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def ensure_dir(directory: str) -> None:
    """Create directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def load_mexc_data(symbol: str) -> pd.DataFrame:
    """Load historical crypto data from MEXC CSV files.

    Args:
        symbol: Cryptocurrency symbol (e.g., 'AVAX_USDT')

    Returns:
        DataFrame with OHLCV data
    """
    # Construct the file path using the new naming pattern
    symbol_lower = symbol.lower().replace("_", "")
    file_pattern = f"data/mexc_{symbol_lower}_4h_*.csv"

    # Find the most recent file matching the pattern
    matching_files = glob.glob(file_pattern)
    if not matching_files:
        raise FileNotFoundError(f"No data files found matching pattern: {file_pattern}")

    # Use the most recent file if multiple exist
    file_path = sorted(matching_files)[-1]

    try:
        # Read CSV file
        data = pd.read_csv(file_path)

        # Convert timestamp to datetime (already in datetime string format)
        data["timestamp"] = pd.to_datetime(data["timestamp"])
        data.set_index("timestamp", inplace=True)

        # Ensure all required columns exist and are properly named
        required_columns = {
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "volume": "volume",
        }

        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Add price column for compatibility
        data["price"] = data["close"]

        # Sort index to ensure chronological order
        data.sort_index(inplace=True)

        return data

    except Exception as e:
        raise Exception(f"Error loading data for {symbol}: {str(e)}")


def run_strategy_benchmark(
    strategy: Any, data: pd.DataFrame, symbol: str
) -> Dict[str, Any]:
    """Run performance benchmark for a strategy."""
    try:
        # Measure execution time
        start_time = time.time()

        # Split data for ML strategy
        if isinstance(strategy, MLStrategyCombiner):
            train_size = int(len(data) * 0.7)
            train_data = data[:train_size]
            test_data = data[train_size:]

            print(f"\nTraining data shape: {train_data.shape}")
            print(f"Test data shape: {test_data.shape}")
            print(f"Columns: {test_data.columns.tolist()}")

            # Train the model
            strategy.train(train_data)

            # Generate signals on test data
            signals = strategy.calculate_signals(test_data)
            print(f"\nSignals shape: {signals.shape}")
            print(f"Signals columns: {signals.columns.tolist()}")

            signals["symbol"] = symbol
            data = test_data
        else:
            # Generate signals for non-ML strategies
            signals = strategy.generate_signals(data)
            signals["symbol"] = symbol

        # Add execution metrics
        execution_time = time.time() - start_time
        memory_usage = memory_profiler.memory_usage(
            (strategy.generate_signals, (data,), {}), max_usage=True
        )

        # Calculate performance metrics
        if "strategy_returns" not in signals.columns:
            print(
                f"\nMissing strategy_returns column. Available columns: {signals.columns.tolist()}"
            )
            return None

        returns = signals["strategy_returns"].dropna()
        print(f"\nNumber of returns: {len(returns)}")
        print(f"Number of non-zero returns: {len(returns[returns != 0])}")

        if len(returns) == 0:
            performance = {
                "total_return": 0.0,
                "annualized_return": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "win_rate": 0.0,
                "num_trades": 0,
                "avg_trade_return": 0.0,
                "max_consecutive_losses": 0,
            }
        else:
            # Calculate metrics
            total_return = (1 + returns).prod() - 1
            annualized_return = (1 + total_return) ** (252 / len(returns)) - 1

            sharpe = (
                returns.mean() / returns.std() * np.sqrt(252)
                if returns.std() != 0
                else 0
            )

            cum_returns = (1 + returns).cumprod()
            rolling_max = cum_returns.expanding().max()
            drawdowns = (cum_returns - rolling_max) / rolling_max
            max_drawdown = drawdowns.min()

            win_rate = (returns > 0).mean()
            num_trades = len(signals[signals["signal"] != 0])

            # Calculate average trade return
            trade_returns = returns[signals["signal"] != 0]
            avg_trade_return = trade_returns.mean() if len(trade_returns) > 0 else 0

            # Calculate maximum consecutive losses
            trade_results = (trade_returns > 0).astype(int)
            loss_streaks = (trade_results != 1).astype(int)
            max_consecutive_losses = (
                max(
                    sum(1 for _ in group)
                    for key, group in itertools.groupby(loss_streaks)
                    if key == 1
                )
                if len(loss_streaks) > 0
                else 0
            )

            performance = {
                "total_return": float(total_return),
                "annualized_return": float(annualized_return),
                "sharpe_ratio": float(sharpe),
                "max_drawdown": float(max_drawdown),
                "win_rate": float(win_rate),
                "num_trades": int(num_trades),
                "avg_trade_return": float(avg_trade_return),
                "max_consecutive_losses": int(max_consecutive_losses),
            }

        # Add strategy-specific metrics
        if isinstance(strategy, MLStrategyCombiner):
            feature_importance = pd.DataFrame(
                {
                    "feature": strategy.prepare_features(data[:1]).columns,
                    "importance": strategy.model.feature_importances_,
                }
            ).sort_values("importance", ascending=False)

            performance.update(
                {
                    "top_features": feature_importance.head(10).to_dict("records"),
                    "prediction_threshold": strategy.prediction_threshold,
                    "lookback_period": strategy.lookback_period,
                }
            )

        return {
            "symbol": symbol,
            "strategy_name": strategy.__class__.__name__,
            "performance": performance,
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "test_period": (
                {"start": data.index[0].isoformat(), "end": data.index[-1].isoformat()}
                if isinstance(strategy, MLStrategyCombiner)
                else None
            ),
        }

    except Exception as e:
        print(
            f"Error in benchmark for {strategy.__class__.__name__} on {symbol} (4h): {str(e)}"
        )
        return None


def run_benchmarks(symbols: List[str] = None) -> List[Dict[str, Any]]:
    """Run comprehensive benchmarks for all strategies."""
    if symbols is None:
        symbols = ["AVAX_USDT"]  # Start with just AVAX for testing

    # Initialize strategies with optimized parameters
    strategies = [
        BreakoutStrategy(),
        MLStrategyCombiner(
            lookback_period=30,  # Increased for better trend capture
            prediction_threshold=0.65,  # More selective signal generation
            position_size=1.0,
            stop_loss=0.015,  # Tighter stop loss
            take_profit=0.035,  # Realistic take profit
        ),
    ]

    # Prepare benchmark tasks
    tasks = []
    for symbol in symbols:
        print(f"Loading data for {symbol}...")
        try:
            # Load 4h data
            data = load_mexc_data(symbol)
            print(f"Loaded {len(data)} periods of data for {symbol}")

            # Add tasks for each strategy
            for strategy in strategies:
                tasks.append((strategy, data, symbol))
        except Exception as e:
            print(f"Error loading data for {symbol}: {str(e)}")
            continue

    # Run benchmarks in parallel
    results = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_strategy_benchmark, *task) for task in tasks]

        for future in as_completed(futures):
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"Error in benchmark task: {e}")

    return results


def print_results(results: List[Dict[str, Any]], output_dir: str) -> None:
    """Print and save benchmark results."""
    print("\nBenchmark Results:")
    print("=" * 80)

    # Group results by strategy and symbol
    strategy_results = {}
    for result in results:
        strategy_name = result.get("strategy_name", "Unknown")
        if strategy_name not in strategy_results:
            strategy_results[strategy_name] = []
        strategy_results[strategy_name].append(result)

    # Print results by strategy and symbol
    for strategy_name, strat_results in strategy_results.items():
        print(f"\n{strategy_name}:")
        print("-" * 40)

        # Sort results by symbol
        strat_results.sort(key=lambda x: x["symbol"])

        for result in strat_results:
            symbol = result["symbol"]
            perf = result["performance"]
            print(f"\n{symbol}:")
            print(f"  Total Return: {perf['total_return']:.2%}")
            print(f"  Annualized Return: {perf['annualized_return']:.2%}")
            print(f"  Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
            print(f"  Max Drawdown: {perf['max_drawdown']:.2%}")
            print(f"  Win Rate: {perf['win_rate']:.2%}")
            print(f"  Number of Trades: {perf['num_trades']}")
            print(f"  Execution Time: {result['execution_time']:.3f}s")

    # Save results to JSON file
    results_file = os.path.join(output_dir, "benchmark_results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, cls=NumpyEncoder, indent=2)

    # Generate markdown report
    report_file = os.path.join(output_dir, "benchmark_report.md")
    with open(report_file, "w") as f:
        f.write("# Trading Strategy Benchmark Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for strategy_name, strat_results in strategy_results.items():
            f.write(f"## {strategy_name}\n\n")

            # Create performance comparison table
            f.write("### Performance Metrics\n\n")
            f.write(
                "| Symbol | Total Return | Sharpe Ratio | Max Drawdown | Win Rate | Trades |\n"
            )
            f.write(
                "|--------|--------------|--------------|--------------|-----------|--------|\n"
            )

            for result in strat_results:
                symbol = result["symbol"]
                perf = result["performance"]
                f.write(
                    f"| {symbol} | {perf['total_return']:.2%} | {perf['sharpe_ratio']:.2f} | "
                    f"{perf['max_drawdown']:.2%} | {perf['win_rate']:.2%} | {perf['num_trades']} |\n"
                )

            f.write("\n### Execution Metrics\n\n")
            f.write("| Symbol | Execution Time (s) | Memory Usage (MB) |\n")
            f.write("|--------|-------------------|------------------|\n")

            for result in strat_results:
                symbol = result["symbol"]
                f.write(
                    f"| {symbol} | {result['execution_time']:.3f} | "
                    f"{result['memory_usage']:.1f} |\n"
                )
            f.write("\n")


if __name__ == "__main__":
    # Create output directory
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    output_dir = f"./benchmarks/benchmark-{timestamp}"
    ensure_dir(output_dir)

    # Run benchmarks
    results = run_benchmarks(
        symbols=["AVAX_USDT"],  # Start with just AVAX for testing
    )

    # Print and save results
    print_results(results, output_dir)

    print(f"\nBenchmark results saved to: {output_dir}")
