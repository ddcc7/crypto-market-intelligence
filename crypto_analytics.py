import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path
import logging
from datetime import datetime


class CryptoAnalytics:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.required_columns = {
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
        }

    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the cryptocurrency market data for completeness and accuracy.

        Returns:
            Tuple[bool, List[str]]: (is_valid, list of validation messages)
        """
        messages = []

        # Check required columns
        missing_cols = self.required_columns - set(df.columns)
        if missing_cols:
            messages.append(f"Missing required columns: {missing_cols}")
            return False, messages

        # Check for null values in critical columns
        null_counts = df[list(self.required_columns)].isnull().sum()
        if null_counts.any():
            for col, count in null_counts[null_counts > 0].items():
                messages.append(f"Found {count} null values in {col}")

        # Check for data type consistency
        numeric_columns = [
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
        ]
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                messages.append(f"Column {col} is not numeric")
                return False, messages

        # Check for negative values where inappropriate
        for col in ["current_price", "market_cap", "total_volume"]:
            if (df[col] < 0).any():
                messages.append(f"Found negative values in {col}")
                return False, messages

        is_valid = len(messages) == 0
        if is_valid:
            messages.append("All validations passed successfully")

        return is_valid, messages

    def calculate_market_stats(self, df: pd.DataFrame) -> Dict:
        """
        Calculate key market statistics.
        """
        stats = {
            "timestamp": datetime.now().isoformat(),
            "market_overview": {
                "total_market_cap": float(df["market_cap"].sum()),
                "total_volume_24h": float(df["total_volume"].sum()),
                "num_cryptocurrencies": len(df),
            },
            "price_changes_24h": {
                "mean": float(df["price_change_percentage_24h"].mean()),
                "median": float(df["price_change_percentage_24h"].median()),
                "std": float(df["price_change_percentage_24h"].std()),
                "min": float(df["price_change_percentage_24h"].min()),
                "max": float(df["price_change_percentage_24h"].max()),
            },
        }

        # Calculate market dominance (top 5)
        total_market_cap = df["market_cap"].sum()
        dominance = df.nlargest(5, "market_cap")[["symbol", "market_cap"]]
        stats["market_dominance"] = {
            row["symbol"]: float(row["market_cap"] / total_market_cap * 100)
            for _, row in dominance.iterrows()
        }

        # Volume/Market Cap ratios (liquidity indicator)
        df["volume_to_mcap"] = df["total_volume"] / df["market_cap"]
        stats["liquidity_metrics"] = {
            "avg_volume_to_mcap": float(df["volume_to_mcap"].mean()),
            "median_volume_to_mcap": float(df["volume_to_mcap"].median()),
        }

        return stats

    def detect_anomalies(
        self, df: pd.DataFrame, z_score_threshold: float = 2.0
    ) -> Dict:
        """
        Detect unusual market movements using statistical methods.
        Uses a modified Z-score approach that's more sensitive to extreme values.
        """
        anomalies = {
            "timestamp": datetime.now().isoformat(),
            "price_movements": [],
            "volume_spikes": [],
            "market_cap_changes": [],
        }

        def get_outliers(series: pd.Series, threshold: float) -> List[Dict]:
            if len(series) < 2:
                return []

            # Use median and MAD for more robust outlier detection
            median = series.median()
            mad = np.median(np.abs(series - median))

            if mad == 0:  # If MAD is 0, use standard deviation instead
                std = series.std()
                if std == 0:
                    return []
                z_scores = np.abs((series - series.mean()) / std)
            else:
                # Modified Z-score using MAD
                z_scores = 0.6745 * np.abs(series - median) / mad

            outliers_idx = z_scores > threshold

            if not outliers_idx.any():
                return []

            return [
                {
                    "symbol": df.loc[idx, "symbol"],
                    "value": float(series[idx]),
                    "z_score": float(z_scores[idx]),
                }
                for idx in series[outliers_idx].index
            ]

        # Detect price change anomalies
        price_outliers = get_outliers(
            df["price_change_percentage_24h"], z_score_threshold
        )
        if price_outliers:
            anomalies["price_movements"].extend(price_outliers)

        # Detect volume spikes
        df["volume_to_mcap"] = df["total_volume"] / df["market_cap"]
        volume_outliers = get_outliers(df["volume_to_mcap"], z_score_threshold)
        if volume_outliers:
            anomalies["volume_spikes"].extend(volume_outliers)

        return anomalies

    def save_analytics(self, stats: Dict, anomalies: Dict) -> bool:
        """
        Save analytics results to JSON file.
        """
        try:
            analytics = {
                "timestamp": datetime.now().isoformat(),
                "market_stats": stats,
                "anomalies": anomalies,
            }

            filepath = self.output_dir / "analytics.json"
            with open(filepath, "w") as f:
                json.dump(analytics, f, indent=4)

            logging.info(f"Analytics saved successfully to {filepath}")
            return True

        except Exception as e:
            logging.error(f"Error saving analytics: {str(e)}")
            return False

    def calculate_sma(self, prices: pd.Series, window: int) -> pd.Series:
        """
        Calculate Simple Moving Average for a given price series.

        Args:
            prices: Series of price data
            window: Number of periods for moving average

        Returns:
            pd.Series: Simple Moving Average values
        """
        return prices.rolling(window=window).mean()

    def identify_crossovers(
        self, short_sma: pd.Series, long_sma: pd.Series
    ) -> pd.Series:
        """
        Identify crossover points between two moving averages.

        Args:
            short_sma: Shorter-term SMA series
            long_sma: Longer-term SMA series

        Returns:
            pd.Series: 1 for bullish crossover (short crosses above long)
                      -1 for bearish crossover (short crosses below long)
                      0 for no crossover
        """
        # Previous day's position
        prev_position = (short_sma.shift(1) > long_sma.shift(1)).astype(int)
        # Current position
        curr_position = (short_sma > long_sma).astype(int)

        # Identify crossovers
        crossovers = curr_position - prev_position

        return crossovers

    def generate_sma_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        short_window: int = 20,
        long_window: int = 50,
    ) -> Dict:
        """
        Generate trading signals using SMA crossover strategy for a specific symbol.

        Args:
            df: DataFrame with historical price data
            symbol: Cryptocurrency symbol to analyze
            short_window: Window for shorter SMA (default: 20)
            long_window: Window for longer SMA (default: 50)

        Returns:
            Dict: Trading signals and performance metrics
        """
        if "close" not in df.columns:
            raise ValueError("DataFrame must contain 'close' price column")

        # Calculate SMAs
        short_sma = self.calculate_sma(df["close"], short_window)
        long_sma = self.calculate_sma(df["close"], long_window)

        # Identify crossovers
        crossovers = self.identify_crossovers(short_sma, long_sma)

        # Generate signals
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]
        signals["short_sma"] = short_sma
        signals["long_sma"] = long_sma
        signals["signal"] = crossovers

        # Calculate strategy returns
        signals["position"] = signals["signal"].cumsum()
        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        # Calculate performance metrics
        total_return = (1 + signals["strategy_returns"]).prod() - 1
        annual_return = (1 + total_return) ** (252 / len(signals)) - 1
        sharpe_ratio = (
            np.sqrt(252)
            * signals["strategy_returns"].mean()
            / signals["strategy_returns"].std()
        )

        results = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "parameters": {"short_window": short_window, "long_window": long_window},
            "performance": {
                "total_return": float(total_return),
                "annual_return": float(annual_return),
                "sharpe_ratio": float(sharpe_ratio),
                "num_trades": int(abs(signals["signal"]).sum() / 2),
            },
            "current_position": int(signals["position"].iloc[-1]),
            "latest_signal": {
                "timestamp": signals.index[-1].isoformat(),
                "price": float(signals["price"].iloc[-1]),
                "short_sma": float(signals["short_sma"].iloc[-1]),
                "long_sma": float(signals["long_sma"].iloc[-1]),
                "crossover": int(signals["signal"].iloc[-1]),
            },
        }

        return results

    def backtest_sma_strategy(
        self,
        historical_data: Dict[str, pd.DataFrame],
        short_window: int = 20,
        long_window: int = 50,
    ) -> Dict:
        """
        Backtest SMA crossover strategy across multiple cryptocurrencies.

        Args:
            historical_data: Dict of DataFrames with historical price data for each symbol
            short_window: Window for shorter SMA (default: 20)
            long_window: Window for longer SMA (default: 50)

        Returns:
            Dict: Backtest results and signals for each symbol
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "strategy_params": {
                "short_window": short_window,
                "long_window": long_window,
            },
            "signals": {},
        }

        # Generate signals for each symbol
        for symbol, df in historical_data.items():
            try:
                symbol_results = self.generate_sma_signals(
                    df, symbol, short_window, long_window
                )
                results["signals"][symbol] = symbol_results
            except Exception as e:
                logging.error(f"Error generating signals for {symbol}: {str(e)}")
                continue

        # Calculate portfolio-level metrics
        portfolio_returns = []
        for symbol in results["signals"]:
            returns = results["signals"][symbol]["performance"]["total_return"]
            portfolio_returns.append(returns)

        if portfolio_returns:
            results["portfolio_metrics"] = {
                "mean_return": float(np.mean(portfolio_returns)),
                "std_return": float(np.std(portfolio_returns)),
                "best_symbol": max(
                    results["signals"].items(),
                    key=lambda x: x[1]["performance"]["total_return"],
                )[0],
                "worst_symbol": min(
                    results["signals"].items(),
                    key=lambda x: x[1]["performance"]["total_return"],
                )[0],
            }

        # Save results
        self.save_predictions(results)

        return results

    def save_predictions(self, predictions: Dict) -> bool:
        """
        Save trading signals and predictions to JSON file.

        Args:
            predictions: Dictionary containing prediction results

        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            filepath = self.output_dir / "predictions.json"
            with open(filepath, "w") as f:
                json.dump(predictions, f, indent=4)

            logging.info(f"Predictions saved successfully to {filepath}")
            return True

        except Exception as e:
            logging.error(f"Error saving predictions: {str(e)}")
            return False
