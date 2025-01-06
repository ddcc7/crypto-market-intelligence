#!/usr/bin/env python3
"""Script to test and backtest the adaptive risk management system."""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from crypto_analytics.strategies import MLStrategyCombiner
from crypto_analytics.strategies.risk_manager import AdaptiveRiskManager


def load_data(symbol: str) -> pd.DataFrame:
    """Load historical data for testing."""
    # Find most recent data file
    data_dir = Path("data")
    file_pattern = f"mexc_{symbol.lower()}_4h_*.csv"
    latest_file = max(data_dir.glob(file_pattern), key=lambda x: x.stat().st_mtime)

    # Load and prepare data
    data = pd.read_csv(latest_file)
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data.set_index("timestamp", inplace=True)
    return data


def backtest_with_risk_management(
    data: pd.DataFrame, base_strategy: MLStrategyCombiner
) -> dict:
    """Run backtest with risk management."""
    # Initialize risk manager with conservative settings
    risk_manager = AdaptiveRiskManager(
        base_position_size=1.0,
        max_position_size=2.0,
        min_position_size=0.1,
        base_stop_loss=0.02,
        base_take_profit=0.04,
        lookback_period=20,
        volatility_scaling=True,
        kelly_fraction=0.5,  # Half-Kelly for more conservative sizing
    )

    # Generate base signals
    signals = base_strategy.generate_signals(data)

    # Apply risk management
    risk_metrics = risk_manager.get_risk_metrics(data, signals)
    risk_adjusted_signals = risk_manager.apply_risk_management(signals, risk_metrics)

    # Calculate performance metrics
    returns = risk_adjusted_signals["strategy_returns"].dropna()

    if len(returns) == 0:
        return {
            "total_return": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "risk_metrics": None,
        }

    # Calculate metrics
    total_return = (1 + returns).prod() - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0

    cum_returns = (1 + returns).cumprod()
    drawdowns = cum_returns / cum_returns.cummax() - 1
    max_drawdown = drawdowns.min()

    win_rate = (returns > 0).mean()

    # Prepare results
    results = {
        "total_return": float(total_return),
        "sharpe_ratio": float(sharpe),
        "max_drawdown": float(max_drawdown),
        "win_rate": float(win_rate),
        "risk_metrics": {
            "kelly_fraction": float(risk_metrics.kelly_fraction),
            "avg_position_size": float(risk_adjusted_signals["position"].abs().mean()),
            "stop_loss": float(risk_metrics.stop_loss),
            "take_profit": float(risk_metrics.take_profit),
            "risk_ratio": float(risk_metrics.risk_ratio),
            "volatility_factor": float(risk_metrics.volatility_factor),
        },
    }

    return results


def main():
    """Run risk management backtest."""
    # Load data
    data = load_data("avaxusdt")

    # Initialize base strategy
    base_strategy = MLStrategyCombiner(
        lookback_period=30,
        prediction_threshold=0.65,
        position_size=1.0,
        stop_loss=0.02,
        take_profit=0.04,
    )

    # Train the strategy
    train_size = int(len(data) * 0.7)
    train_data = data[:train_size]
    test_data = data[train_size:]
    base_strategy.train(train_data)

    # Run backtest with risk management
    results = backtest_with_risk_management(test_data, base_strategy)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"predictions.json"

    # Load existing results if any
    if Path(results_file).exists():
        with open(results_file, "r") as f:
            existing_results = json.load(f)
    else:
        existing_results = {}

    # Add new results
    existing_results[f"risk_managed_strategy_{timestamp}"] = results

    # Save updated results
    with open(results_file, "w") as f:
        json.dump(existing_results, f, indent=2)

    print("\nBacktest Results:")
    print(f"Total Return: {results['total_return']:.2%}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2%}")
    print(f"Win Rate: {results['win_rate']:.2%}")
    print("\nRisk Metrics:")
    print(f"Kelly Fraction: {results['risk_metrics']['kelly_fraction']:.2f}")
    print(f"Avg Position Size: {results['risk_metrics']['avg_position_size']:.2f}")
    print(f"Stop Loss: {results['risk_metrics']['stop_loss']:.2%}")
    print(f"Take Profit: {results['risk_metrics']['take_profit']:.2%}")
    print(f"Risk Ratio: {results['risk_metrics']['risk_ratio']:.2f}")
    print(f"Volatility Factor: {results['risk_metrics']['volatility_factor']:.2f}")


if __name__ == "__main__":
    main()
