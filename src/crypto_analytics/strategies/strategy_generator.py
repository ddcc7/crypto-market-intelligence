"""Strategy generator module for automated strategy creation and optimization."""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import random
from ..indicators import MACD, BollingerBands
from .base_strategy import BaseStrategy


@dataclass
class StrategyParams:
    """Parameters for strategy generation."""

    indicator_weights: Dict[str, float]
    entry_thresholds: Dict[str, float]
    exit_thresholds: Dict[str, float]
    position_size: float
    stop_loss: float
    take_profit: float
    lookback_period: int


class StrategyEvaluator:
    """Evaluates strategy performance using multiple metrics."""

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.metrics_weights = {
            "sharpe_ratio": 0.3,
            "sortino_ratio": 0.2,
            "max_drawdown": 0.2,
            "win_rate": 0.15,
            "profit_factor": 0.15,
        }

    def calculate_metrics(self, signals: pd.DataFrame) -> Dict[str, float]:
        returns = signals["strategy_returns"].dropna()
        if len(returns) == 0:
            return {metric: 0.0 for metric in self.metrics_weights}

        sharpe = (
            returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0
        )
        downside_returns = returns[returns < 0]
        sortino = (
            returns.mean() * np.sqrt(252) / downside_returns.std()
            if len(downside_returns) > 0 and downside_returns.std() != 0
            else 0
        )

        cum_returns = (1 + returns).cumprod()
        rolling_max = cum_returns.expanding().max()
        drawdowns = (cum_returns - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()

        win_rate = (returns > 0).mean()
        profit_factor = (
            abs(returns[returns > 0].sum()) / abs(returns[returns < 0].sum())
            if len(returns[returns < 0]) > 0
            else float("inf")
        )
        profit_factor = min(profit_factor, 1000.0)

        return {
            "sharpe_ratio": float(sharpe),
            "sortino_ratio": float(sortino),
            "max_drawdown": float(max_drawdown),
            "win_rate": float(win_rate),
            "profit_factor": float(profit_factor),
        }

    def calculate_fitness(self, metrics: Dict[str, float]) -> float:
        normalized = {
            "sharpe_ratio": np.clip(metrics["sharpe_ratio"] / 3.0, 0, 1),
            "sortino_ratio": np.clip(metrics["sortino_ratio"] / 4.0, 0, 1),
            "max_drawdown": 1 + np.clip(metrics["max_drawdown"], -1, 0),
            "win_rate": metrics["win_rate"],
            "profit_factor": np.clip(metrics["profit_factor"] / 3.0, 0, 1),
        }
        return float(
            sum(
                normalized[metric] * weight
                for metric, weight in self.metrics_weights.items()
            )
        )


class StrategyGenerator:
    """Generates optimized trading strategies."""

    def __init__(self, train_data: pd.DataFrame, test_data: pd.DataFrame):
        self.train_data = train_data
        self.test_data = test_data
        self.train_evaluator = StrategyEvaluator(train_data)
        self.test_evaluator = StrategyEvaluator(test_data)

    def generate_random_params(self) -> StrategyParams:
        return StrategyParams(
            indicator_weights={"macd": random.random(), "bollinger": random.random()},
            entry_thresholds={
                "oversold": -random.random() * 2,
                "overbought": random.random() * 2,
            },
            exit_thresholds={
                "profit": random.random() * 0.05,
                "loss": -random.random() * 0.05,
            },
            position_size=random.uniform(0.1, 1.0),
            stop_loss=random.uniform(0.02, 0.1),
            take_profit=random.uniform(0.02, 0.2),
            lookback_period=random.randint(5, 50),
        )

    def mutate_params(
        self, params: StrategyParams, mutation_rate: float = 0.2
    ) -> StrategyParams:
        new_params = StrategyParams(
            indicator_weights=params.indicator_weights.copy(),
            entry_thresholds=params.entry_thresholds.copy(),
            exit_thresholds=params.exit_thresholds.copy(),
            position_size=params.position_size,
            stop_loss=params.stop_loss,
            take_profit=params.take_profit,
            lookback_period=params.lookback_period,
        )

        if random.random() < mutation_rate:
            new_params.indicator_weights["macd"] *= random.uniform(0.8, 1.2)
            new_params.indicator_weights["bollinger"] *= random.uniform(0.8, 1.2)

        if random.random() < mutation_rate:
            new_params.entry_thresholds["oversold"] *= random.uniform(0.8, 1.2)
            new_params.entry_thresholds["overbought"] *= random.uniform(0.8, 1.2)

        if random.random() < mutation_rate:
            new_params.position_size = min(
                1.0, new_params.position_size * random.uniform(0.8, 1.2)
            )

        if random.random() < mutation_rate:
            new_params.stop_loss = min(
                0.2, new_params.stop_loss * random.uniform(0.8, 1.2)
            )
            new_params.take_profit = min(
                0.4, new_params.take_profit * random.uniform(0.8, 1.2)
            )

        if random.random() < mutation_rate:
            new_params.lookback_period = max(
                5, min(50, int(new_params.lookback_period * random.uniform(0.8, 1.2)))
            )

        return new_params

    def crossover_params(
        self, params1: StrategyParams, params2: StrategyParams
    ) -> StrategyParams:
        return StrategyParams(
            indicator_weights={
                k: random.choice(
                    [params1.indicator_weights[k], params2.indicator_weights[k]]
                )
                for k in params1.indicator_weights
            },
            entry_thresholds={
                k: random.choice(
                    [params1.entry_thresholds[k], params2.entry_thresholds[k]]
                )
                for k in params1.entry_thresholds
            },
            exit_thresholds={
                k: random.choice(
                    [params1.exit_thresholds[k], params2.exit_thresholds[k]]
                )
                for k in params1.exit_thresholds
            },
            position_size=random.choice([params1.position_size, params2.position_size]),
            stop_loss=random.choice([params1.stop_loss, params2.stop_loss]),
            take_profit=random.choice([params1.take_profit, params2.take_profit]),
            lookback_period=random.choice(
                [params1.lookback_period, params2.lookback_period]
            ),
        )

    def optimize_strategy(
        self,
        population_size: int = 50,
        generations: int = 20,
        mutation_rate: float = 0.2,
    ) -> Tuple[StrategyParams, Dict[str, float]]:
        population = [self.generate_random_params() for _ in range(population_size)]
        best_params = None
        best_fitness = -float("inf")
        best_metrics = None

        for generation in range(generations):
            fitness_scores = []
            for params in population:
                strategy = AdaptiveStrategy(params)
                signals = strategy.calculate_signals(self.train_data)
                metrics = self.train_evaluator.calculate_metrics(signals)
                fitness = self.train_evaluator.calculate_fitness(metrics)
                fitness_scores.append((params, fitness, metrics))

            fitness_scores.sort(key=lambda x: x[1], reverse=True)

            if fitness_scores[0][1] > best_fitness:
                best_params = fitness_scores[0][0]
                best_fitness = fitness_scores[0][1]
                best_metrics = fitness_scores[0][2]

            elite_size = max(2, population_size // 10)
            new_population = [score[0] for score in fitness_scores[:elite_size]]

            while len(new_population) < population_size:
                if random.random() < 0.7:
                    parent1 = random.choice(fitness_scores[: population_size // 2])[0]
                    parent2 = random.choice(fitness_scores[: population_size // 2])[0]
                    child = self.crossover_params(parent1, parent2)
                else:
                    parent = random.choice(fitness_scores[: population_size // 2])[0]
                    child = self.mutate_params(parent, mutation_rate)
                new_population.append(child)

            population = new_population

        if best_params is not None:
            strategy = AdaptiveStrategy(best_params)
            test_signals = strategy.calculate_signals(self.test_data)
            test_metrics = self.test_evaluator.calculate_metrics(test_signals)

            if test_metrics["sharpe_ratio"] > 0 and test_metrics["max_drawdown"] > -0.5:
                return best_params, test_metrics

        return self.generate_random_params(), {}


class AdaptiveStrategy(BaseStrategy):
    """Adaptive strategy that combines multiple indicators."""

    def __init__(self, params: StrategyParams):
        super().__init__(
            [
                MACD({"fast_period": 12, "slow_period": 26, "signal_period": 9}),
                BollingerBands({"window": 20, "num_std": 2}),
            ]
        )
        self.params = params

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = data.copy()
        signals["signal"] = pd.Series(0.0, index=signals.index, dtype="float64")
        signals["position"] = pd.Series(0.0, index=signals.index, dtype="float64")

        if "close" in signals.columns:
            signals["price"] = signals["close"]
        elif "Close" in signals.columns:
            signals["price"] = signals["Close"]
            signals["close"] = signals["Close"]

        macd_data = self.indicators[0].calculate(signals)
        bb_data = self.indicators[1].calculate(signals)

        for i in range(self.params.lookback_period, len(signals)):
            macd_trend = (
                macd_data["macd_line"].iloc[i] * self.params.indicator_weights["macd"]
                + bb_data["bandwidth"].iloc[i]
                * self.params.indicator_weights["bollinger"]
            )

            if macd_trend < self.params.entry_thresholds["oversold"]:
                signals.iloc[i, signals.columns.get_loc("signal")] = 1
            elif macd_trend > self.params.entry_thresholds["overbought"]:
                signals.iloc[i, signals.columns.get_loc("signal")] = -1

            new_position = signals.iloc[i - 1]["position"] + signals.iloc[i]["signal"]
            signals.iloc[i, signals.columns.get_loc("position")] = np.clip(
                new_position, -self.params.position_size, self.params.position_size
            )

            if signals.iloc[i - 1]["position"] != 0:
                returns = (
                    signals.iloc[i]["price"] - signals.iloc[i - 1]["price"]
                ) / signals.iloc[i - 1]["price"]
                if returns * signals.iloc[i - 1]["position"] <= -self.params.stop_loss:
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0
                elif (
                    returns * signals.iloc[i - 1]["position"] >= self.params.take_profit
                ):
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0

        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        return signals

    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on indicator rules."""
        # The signal generation is already handled in calculate_signals
        return signals
