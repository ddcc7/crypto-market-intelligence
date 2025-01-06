"""Script for optimizing trading strategies using genetic algorithms."""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from pathlib import Path
import json
from tqdm import tqdm
import random
from concurrent.futures import ProcessPoolExecutor, as_completed

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crypto_analytics.strategies.strategy_generator import (
    StrategyGenerator,
    AdaptiveStrategy,
)


def fetch_data(symbol: str, start_date: str, end_date: str = None) -> pd.DataFrame:
    """Fetch historical data from Yahoo Finance."""
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)

    # Ensure consistent column names
    data.columns = data.columns.str.lower()

    # Add price column for compatibility
    data["price"] = data["close"]

    return data


def split_data(data: pd.DataFrame, train_ratio: float = 0.7) -> tuple:
    """Split data into training and test sets."""
    split_idx = int(len(data) * train_ratio)
    return data.iloc[:split_idx], data.iloc[split_idx:]


def save_strategy(params: dict, metrics: dict, symbol: str) -> None:
    """Save strategy parameters and metrics."""
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    output_dir = Path(f"optimized_strategies/{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save parameters
    params_file = output_dir / f"{symbol}_params.json"
    with open(params_file, "w") as f:
        json.dump(params.__dict__, f, indent=4)

    # Save metrics
    metrics_file = output_dir / f"{symbol}_metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4)


def evaluate_individual(args):
    """Evaluate a single individual (for parallel processing)."""
    params, train_data, evaluator = args
    strategy = AdaptiveStrategy(params)
    signals = strategy.calculate_signals(train_data)
    metrics = evaluator.calculate_metrics(signals)
    fitness = evaluator.calculate_fitness(metrics)
    return params, fitness, metrics


def optimize_with_progress(generator, population_size, generations, mutation_rate):
    """Run optimization with progress bar."""
    population = [generator.generate_random_params() for _ in range(population_size)]
    best_params = None
    best_fitness = -float("inf")
    best_metrics = None
    generations_without_improvement = 0
    max_generations_without_improvement = 15

    # Progress bar for generations
    pbar = tqdm(range(generations), desc="Optimizing generations")

    # Create a process pool for parallel evaluation
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for generation in pbar:
            # Prepare evaluation arguments
            eval_args = [
                (params, generator.train_data, generator.train_evaluator)
                for params in population
            ]

            # Evaluate population in parallel
            fitness_scores = list(executor.map(evaluate_individual, eval_args))
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            current_best_fitness = fitness_scores[0][1]

            if current_best_fitness > best_fitness:
                best_params = fitness_scores[0][0]
                best_fitness = current_best_fitness
                best_metrics = fitness_scores[0][2]
                generations_without_improvement = 0
                pbar.set_postfix(
                    {"Best Fitness": f"{best_fitness:.4f}", "Gen": generation}
                )
            else:
                generations_without_improvement += 1

            # Early stopping if no improvement for several generations
            if generations_without_improvement >= max_generations_without_improvement:
                print(
                    f"\nEarly stopping: No improvement for {max_generations_without_improvement} generations"
                )
                break

            elite_size = max(2, population_size // 10)
            new_population = [score[0] for score in fitness_scores[:elite_size]]

            # Select parents from top half of population
            top_half = fitness_scores[: population_size // 2]

            while len(new_population) < population_size:
                if random.random() < 0.7:
                    parent1, parent2 = random.sample(top_half, 2)
                    child = generator.crossover_params(parent1[0], parent2[0])
                else:
                    parent = random.choice(top_half)
                    child = generator.mutate_params(parent[0], mutation_rate)
                new_population.append(child)

            population = new_population

            # Check if we've found a good enough strategy
            if best_fitness > 0.75:
                print("\nFound satisfactory strategy. Stopping early.")
                break

    if best_params is not None:
        strategy = AdaptiveStrategy(best_params)
        test_signals = strategy.calculate_signals(generator.test_data)
        test_metrics = generator.test_evaluator.calculate_metrics(test_signals)

        # Relaxed criteria for accepting strategies
        if test_metrics["sharpe_ratio"] > -0.5 and test_metrics["max_drawdown"] > -0.6:
            return best_params, test_metrics

    return generator.generate_random_params(), {}


def main():
    """Main function to optimize strategies."""
    # Configuration
    symbols = ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD", "BNB-USD"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=240)
    population_size = 80
    generations = 40
    mutation_rate = 0.25

    # Progress bar for symbols
    for symbol in tqdm(symbols, desc="Processing symbols"):
        print(f"\nOptimizing strategy for {symbol}")

        # Fetch data
        print("Fetching data...")
        data = fetch_data(symbol, start_date.strftime("%Y-%m-%d"))

        # Split data
        print("Splitting data into train/test sets...")
        train_data, test_data = split_data(data)

        # Create and run strategy generator with progress
        print("Optimizing strategy parameters...")
        generator = StrategyGenerator(train_data, test_data)
        best_params, test_metrics = optimize_with_progress(
            generator,
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
        )

        # Save results
        if test_metrics:
            print("\nBest strategy metrics:")
            print(f"Sharpe Ratio: {test_metrics['sharpe_ratio']:.2f}")
            print(f"Sortino Ratio: {test_metrics['sortino_ratio']:.2f}")
            print(f"Max Drawdown: {test_metrics['max_drawdown']:.2%}")
            print(f"Win Rate: {test_metrics['win_rate']:.2%}")
            print(f"Profit Factor: {test_metrics['profit_factor']:.2f}")

            save_strategy(best_params, test_metrics, symbol)
            print(f"\nStrategy saved to optimized_strategies/")
        else:
            print(
                "\nNo satisfactory strategy found. Try adjusting optimization parameters."
            )


if __name__ == "__main__":
    main()
