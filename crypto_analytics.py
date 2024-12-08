import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Literal
import json
from pathlib import Path
import logging
from datetime import datetime

MarketCondition = Literal["trending_up", "trending_down", "ranging", "volatile"]


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

    def calculate_wma(self, prices: pd.Series, window: int) -> pd.Series:
        """
        Calculate Weighted Moving Average for a given price series.
        Recent prices have higher weights.

        Args:
            prices: Series of price data
            window: Number of periods for moving average

        Returns:
            pd.Series: Weighted Moving Average values
        """
        weights = np.arange(1, window + 1)
        wma = prices.rolling(window=window).apply(
            lambda x: np.sum(weights * x) / weights.sum(), raw=True
        )
        return wma

    def generate_wma_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        short_window: int = 20,
        long_window: int = 50,
    ) -> Dict:
        """
        Generate trading signals using WMA crossover strategy for a specific symbol.

        Args:
            df: DataFrame with historical price data
            symbol: Cryptocurrency symbol to analyze
            short_window: Window for shorter WMA (default: 20)
            long_window: Window for longer WMA (default: 50)

        Returns:
            Dict: Trading signals and performance metrics
        """
        if "close" not in df.columns:
            raise ValueError("DataFrame must contain 'close' price column")

        # Calculate WMAs
        short_wma = self.calculate_wma(df["close"], short_window)
        long_wma = self.calculate_wma(df["close"], long_window)

        # Identify crossovers
        crossovers = self.identify_crossovers(short_wma, long_wma)

        # Generate signals
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]
        signals["short_wma"] = short_wma
        signals["long_wma"] = long_wma
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
            "strategy": "WMA",
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
                "short_wma": float(signals["short_wma"].iloc[-1]),
                "long_wma": float(signals["long_wma"].iloc[-1]),
                "crossover": int(signals["signal"].iloc[-1]),
            },
        }

        return results

    def compare_strategies(
        self,
        historical_data: Dict[str, pd.DataFrame],
        short_window: int = 20,
        long_window: int = 50,
    ) -> Dict:
        """
        Compare SMA and WMA strategies across multiple cryptocurrencies.

        Args:
            historical_data: Dict of DataFrames with historical price data for each symbol
            short_window: Window for shorter average (default: 20)
            long_window: Window for longer average (default: 50)

        Returns:
            Dict: Comparison results and signals for each strategy
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "parameters": {"short_window": short_window, "long_window": long_window},
            "strategies": {"SMA": {"signals": {}}, "WMA": {"signals": {}}},
        }

        # Generate signals for each symbol and strategy
        for symbol, df in historical_data.items():
            try:
                # Get SMA signals
                sma_results = self.generate_sma_signals(
                    df, symbol, short_window, long_window
                )
                results["strategies"]["SMA"]["signals"][symbol] = sma_results

                # Get WMA signals
                wma_results = self.generate_wma_signals(
                    df, symbol, short_window, long_window
                )
                results["strategies"]["WMA"]["signals"][symbol] = wma_results

            except Exception as e:
                logging.error(f"Error generating signals for {symbol}: {e}")
                continue

        # Calculate strategy-level metrics
        for strategy in ["SMA", "WMA"]:
            signals = results["strategies"][strategy]["signals"]
            if signals:
                returns = [s["performance"]["total_return"] for s in signals.values()]
                sharpe_ratios = [
                    s["performance"]["sharpe_ratio"] for s in signals.values()
                ]

                results["strategies"][strategy]["metrics"] = {
                    "mean_return": float(np.mean(returns)),
                    "std_return": float(np.std(returns)),
                    "mean_sharpe": float(np.mean(sharpe_ratios)),
                    "best_symbol": max(
                        signals.items(),
                        key=lambda x: x[1]["performance"]["total_return"],
                    )[0],
                    "worst_symbol": min(
                        signals.items(),
                        key=lambda x: x[1]["performance"]["total_return"],
                    )[0],
                }

        # Save comparison results
        self.save_predictions(results)

        return results

    def calculate_bollinger_bands(
        self, prices: pd.Series, window: int = 20, num_std: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands for a given price series.

        Args:
            prices: Series of price data
            window: Period for moving average (default: 20)
            num_std: Number of standard deviations for bands (default: 2.0)

        Returns:
            Tuple[pd.Series, pd.Series, pd.Series]: Upper band, middle band, lower band
        """
        middle_band = self.calculate_sma(prices, window)
        rolling_std = prices.rolling(window=window).std()

        upper_band = middle_band + (rolling_std * num_std)
        lower_band = middle_band - (rolling_std * num_std)

        return upper_band, middle_band, lower_band

    def generate_bollinger_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        window: int = 20,
        num_std: float = 2.0,
    ) -> Dict:
        """
        Generate trading signals using Bollinger Bands strategy.

        Args:
            df: DataFrame with historical price data
            symbol: Cryptocurrency symbol to analyze
            window: Period for moving average (default: 20)
            num_std: Number of standard deviations for bands (default: 2.0)

        Returns:
            Dict: Trading signals and performance metrics
        """
        if "close" not in df.columns:
            raise ValueError("DataFrame must contain 'close' price column")

        # Calculate Bollinger Bands
        upper_band, middle_band, lower_band = self.calculate_bollinger_bands(
            df["close"], window, num_std
        )

        # Generate signals
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]
        signals["upper_band"] = upper_band
        signals["middle_band"] = middle_band
        signals["lower_band"] = lower_band

        # 1 for buy (price crosses below lower band)
        # -1 for sell (price crosses above upper band)
        # 0 for no signal
        signals["signal"] = 0
        signals.loc[df["close"] < lower_band, "signal"] = 1
        signals.loc[df["close"] > upper_band, "signal"] = -1

        # Calculate strategy returns
        signals["position"] = signals["signal"].fillna(0)
        signals["returns"] = df["close"].pct_change()
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
            "strategy": "Bollinger Bands",
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "window": window,
                "num_std": num_std,
            },
            "performance": {
                "total_return": float(total_return),
                "annual_return": float(annual_return),
                "sharpe_ratio": float(sharpe_ratio),
                "num_trades": int(abs(signals["signal"]).sum()),
            },
            "current_position": int(signals["position"].iloc[-1]),
            "latest_signal": {
                "timestamp": signals.index[-1].isoformat(),
                "price": float(signals["price"].iloc[-1]),
                "upper_band": float(signals["upper_band"].iloc[-1]),
                "middle_band": float(signals["middle_band"].iloc[-1]),
                "lower_band": float(signals["lower_band"].iloc[-1]),
                "signal": int(signals["signal"].iloc[-1]),
            },
        }

        return results

    def backtest_bollinger_strategy(
        self,
        historical_data: Dict[str, pd.DataFrame],
        window: int = 20,
        num_std: float = 2.0,
    ) -> Dict:
        """
        Backtest Bollinger Bands strategy across multiple cryptocurrencies.

        Args:
            historical_data: Dict of DataFrames with historical price data for each symbol
            window: Period for moving average (default: 20)
            num_std: Number of standard deviations for bands (default: 2.0)

        Returns:
            Dict: Backtest results and signals for each symbol
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "strategy": "Bollinger Bands",
            "parameters": {
                "window": window,
                "num_std": num_std,
            },
            "signals": {},
        }

        # Generate signals for each symbol
        for symbol, df in historical_data.items():
            try:
                symbol_results = self.generate_bollinger_signals(
                    df, symbol, window, num_std
                )
                results["signals"][symbol] = symbol_results
            except Exception as e:
                logging.error(f"Error generating signals for {symbol}: {str(e)}")
                continue

        # Calculate portfolio-level metrics
        if results["signals"]:
            returns = [
                s["performance"]["total_return"] for s in results["signals"].values()
            ]
            sharpe_ratios = [
                s["performance"]["sharpe_ratio"] for s in results["signals"].values()
            ]

            results["portfolio_metrics"] = {
                "mean_return": float(np.mean(returns)),
                "std_return": float(np.std(returns)),
                "mean_sharpe": float(np.mean(sharpe_ratios)),
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

    def calculate_ema(self, prices: pd.Series, window: int) -> pd.Series:
        """
        Calculate Exponential Moving Average for a given price series.

        Args:
            prices: Series of price data
            window: Number of periods for moving average

        Returns:
            pd.Series: Exponential Moving Average values
        """
        return prices.ewm(span=window, adjust=False).mean()

    def generate_ema_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        short_window: int = 20,
        long_window: int = 50,
    ) -> Dict:
        """
        Generate trading signals using EMA crossover strategy for a specific symbol.

        Args:
            df: DataFrame with historical price data
            symbol: Cryptocurrency symbol to analyze
            short_window: Window for shorter EMA (default: 20)
            long_window: Window for longer EMA (default: 50)

        Returns:
            Dict: Trading signals and performance metrics
        """
        if "close" not in df.columns:
            raise ValueError("DataFrame must contain 'close' price column")

        # Calculate EMAs
        short_ema = self.calculate_ema(df["close"], short_window)
        long_ema = self.calculate_ema(df["close"], long_window)

        # Identify crossovers
        crossovers = self.identify_crossovers(short_ema, long_ema)

        # Generate signals
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]
        signals["short_ema"] = short_ema
        signals["long_ema"] = long_ema
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
            "strategy": "EMA",
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
                "short_ema": float(signals["short_ema"].iloc[-1]),
                "long_ema": float(signals["long_ema"].iloc[-1]),
                "crossover": int(signals["signal"].iloc[-1]),
            },
        }

        return results

    def backtest_ema_strategy(
        self,
        historical_data: Dict[str, pd.DataFrame],
        short_window: int = 20,
        long_window: int = 50,
    ) -> Dict:
        """
        Backtest EMA crossover strategy across multiple cryptocurrencies.

        Args:
            historical_data: Dict of DataFrames with historical price data for each symbol
            short_window: Window for shorter EMA (default: 20)
            long_window: Window for longer EMA (default: 50)

        Returns:
            Dict: Backtest results and signals for each symbol
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "strategy": "EMA",
            "parameters": {
                "short_window": short_window,
                "long_window": long_window,
            },
            "signals": {},
        }

        # Generate signals for each symbol
        for symbol, df in historical_data.items():
            try:
                symbol_results = self.generate_ema_signals(
                    df, symbol, short_window, long_window
                )
                results["signals"][symbol] = symbol_results
            except Exception as e:
                logging.error(f"Error generating signals for {symbol}: {str(e)}")
                continue

        # Calculate portfolio-level metrics
        if results["signals"]:
            returns = [
                s["performance"]["total_return"] for s in results["signals"].values()
            ]
            sharpe_ratios = [
                s["performance"]["sharpe_ratio"] for s in results["signals"].values()
            ]

            results["portfolio_metrics"] = {
                "mean_return": float(np.mean(returns)),
                "std_return": float(np.std(returns)),
                "mean_sharpe": float(np.mean(sharpe_ratios)),
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

    def calculate_stochastic(
        self,
        df: pd.DataFrame,
        k_period: int = 14,
        d_period: int = 3,
        overbought: float = 80.0,
        oversold: float = 20.0,
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator (%K and %D lines).

        Args:
            df: DataFrame with high, low, close prices
            k_period: Period for %K calculation (default: 14)
            d_period: Period for %D calculation (default: 3)
            overbought: Overbought threshold (default: 80)
            oversold: Oversold threshold (default: 20)

        Returns:
            Tuple[pd.Series, pd.Series]: %K and %D lines
        """
        # Calculate %K
        low_min = df["low"].rolling(window=k_period).min()
        high_max = df["high"].rolling(window=k_period).max()
        k_line = 100 * (df["close"] - low_min) / (high_max - low_min)

        # Calculate %D (3-period SMA of %K)
        d_line = k_line.rolling(window=d_period).mean()

        return k_line, d_line

    def generate_stochastic_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        k_period: int = 14,
        d_period: int = 3,
        overbought: float = 80.0,
        oversold: float = 20.0,
    ) -> Dict:
        """
        Generate trading signals using Stochastic Oscillator.

        Args:
            df: DataFrame with historical price data
            symbol: Cryptocurrency symbol to analyze
            k_period: Period for %K calculation (default: 14)
            d_period: Period for %D calculation (default: 3)
            overbought: Overbought threshold (default: 80)
            oversold: Oversold threshold (default: 20)

        Returns:
            Dict: Trading signals and performance metrics
        """
        required_columns = {"high", "low", "close"}
        if not all(col in df.columns for col in required_columns):
            raise ValueError(
                "DataFrame must contain 'high', 'low', and 'close' columns"
            )

        # Calculate Stochastic Oscillator
        k_line, d_line = self.calculate_stochastic(
            df, k_period, d_period, overbought, oversold
        )

        # Generate signals
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]
        signals["k_line"] = k_line
        signals["d_line"] = d_line

        # Buy when both lines cross above oversold
        # Sell when both lines cross below overbought
        signals["signal"] = 0
        signals.loc[
            (k_line > oversold) & (d_line > oversold) & (k_line.shift(1) <= oversold),
            "signal",
        ] = 1  # Buy
        signals.loc[
            (k_line < overbought)
            & (d_line < overbought)
            & (k_line.shift(1) >= overbought),
            "signal",
        ] = -1  # Sell

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
            "strategy": "Stochastic",
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "k_period": k_period,
                "d_period": d_period,
                "overbought": overbought,
                "oversold": oversold,
            },
            "performance": {
                "total_return": float(total_return),
                "annual_return": float(annual_return),
                "sharpe_ratio": float(sharpe_ratio),
                "num_trades": int(abs(signals["signal"]).sum()),
            },
            "current_position": int(signals["position"].iloc[-1]),
            "latest_signal": {
                "timestamp": signals.index[-1].isoformat(),
                "price": float(signals["price"].iloc[-1]),
                "k_line": float(signals["k_line"].iloc[-1]),
                "d_line": float(signals["d_line"].iloc[-1]),
                "signal": int(signals["signal"].iloc[-1]),
            },
        }

        return results

    def backtest_stochastic_strategy(
        self,
        historical_data: Dict[str, pd.DataFrame],
        k_period: int = 14,
        d_period: int = 3,
        overbought: float = 80.0,
        oversold: float = 20.0,
    ) -> Dict:
        """
        Backtest Stochastic Oscillator strategy across multiple cryptocurrencies.

        Args:
            historical_data: Dict of DataFrames with historical price data for each symbol
            k_period: Period for %K calculation (default: 14)
            d_period: Period for %D calculation (default: 3)
            overbought: Overbought threshold (default: 80)
            oversold: Oversold threshold (default: 20)

        Returns:
            Dict: Backtest results and signals for each symbol
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "strategy": "Stochastic",
            "parameters": {
                "k_period": k_period,
                "d_period": d_period,
                "overbought": overbought,
                "oversold": oversold,
            },
            "signals": {},
        }

        # Generate signals for each symbol
        for symbol, df in historical_data.items():
            try:
                symbol_results = self.generate_stochastic_signals(
                    df, symbol, k_period, d_period, overbought, oversold
                )
                results["signals"][symbol] = symbol_results
            except Exception as e:
                logging.error(f"Error generating signals for {symbol}: {str(e)}")
                continue

        # Calculate portfolio-level metrics
        if results["signals"]:
            returns = [
                s["performance"]["total_return"] for s in results["signals"].values()
            ]
            sharpe_ratios = [
                s["performance"]["sharpe_ratio"] for s in results["signals"].values()
            ]

            results["portfolio_metrics"] = {
                "mean_return": float(np.mean(returns)),
                "std_return": float(np.std(returns)),
                "mean_sharpe": float(np.mean(sharpe_ratios)),
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

    def classify_market_condition(
        self,
        df: pd.DataFrame,
        window: int = 20,
        volatility_threshold: float = 0.02,
        trend_threshold: float = 0.1,
    ) -> MarketCondition:
        """
        Classify market condition based on price action and volatility.

        Args:
            df: DataFrame with price data
            window: Period for analysis (default: 20)
            volatility_threshold: Threshold for high volatility (default: 0.02 or 2%)
            trend_threshold: Threshold for trend determination (default: 0.1 or 10%)

        Returns:
            MarketCondition: Current market condition
        """
        # Calculate price changes and volatility
        returns = df["close"].pct_change()
        volatility = returns.rolling(window=window).std()

        # Calculate trend using linear regression
        x = np.arange(len(df[-window:]))
        y = df["close"].values[-window:]
        slope, _ = np.polyfit(x, y, 1)
        price_change = (df["close"].iloc[-1] - df["close"].iloc[-window]) / df[
            "close"
        ].iloc[-window]

        # Classify market condition
        is_volatile = volatility.iloc[-1] > volatility_threshold

        if is_volatile:
            return "volatile"
        elif price_change > trend_threshold:
            return "trending_up"
        elif price_change < -trend_threshold:
            return "trending_down"
        else:
            return "ranging"

    def evaluate_strategy_by_market_condition(
        self, df: pd.DataFrame, strategy_signals: pd.DataFrame, window: int = 20
    ) -> Dict:
        """
        Evaluate strategy performance under different market conditions.

        Args:
            df: DataFrame with price data
            strategy_signals: DataFrame with strategy signals and returns
            window: Period for market condition analysis

        Returns:
            Dict: Performance metrics by market condition
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "window": window,
            "market_conditions": {},
        }

        # Analyze each window period
        for i in range(window, len(df), window):
            period_slice = slice(i - window, i)
            period_df = df.iloc[period_slice].copy()
            period_signals = strategy_signals.iloc[period_slice].copy()

            # Skip periods with insufficient data
            if len(period_df) < window or len(period_signals) < window:
                continue

            # Classify market condition for this period
            condition = self.classify_market_condition(period_df, window)

            # Reset position for this period
            period_signals["position"] = period_signals["signal"].fillna(0).cumsum()
            period_signals["returns"] = period_df["close"].pct_change().fillna(0)
            period_signals["strategy_returns"] = (
                period_signals["position"].shift(1) * period_signals["returns"]
            )

            # Calculate period performance
            period_returns = period_signals["strategy_returns"].fillna(0)
            period_return = (1 + period_returns).prod() - 1

            # Calculate Sharpe ratio only if there's variance in returns
            returns_std = period_returns.std()
            if returns_std > 0 and not np.isnan(returns_std):
                period_sharpe = np.sqrt(252) * period_returns.mean() / returns_std
            else:
                period_sharpe = 0

            # Calculate number of trades in this period
            period_trades = abs(period_signals["signal"]).sum()

            # Add to results
            if condition not in results["market_conditions"]:
                results["market_conditions"][condition] = {
                    "periods": 0,
                    "total_return": 0.0,
                    "returns": [],
                    "sharpe_ratios": [],
                    "trades": [],
                    "win_rate": 0.0,
                    "profitable_periods": 0,
                }

            results["market_conditions"][condition]["periods"] += 1
            results["market_conditions"][condition]["returns"].append(
                float(period_return)
            )
            results["market_conditions"][condition]["sharpe_ratios"].append(
                float(period_sharpe)
            )
            results["market_conditions"][condition]["trades"].append(int(period_trades))

            if period_return > 0:
                results["market_conditions"][condition]["profitable_periods"] += 1

        # Calculate average metrics for each condition
        for condition in results["market_conditions"]:
            condition_data = results["market_conditions"][condition]
            returns = condition_data["returns"]
            sharpe_ratios = condition_data["sharpe_ratios"]
            trades = condition_data["trades"]

            if returns:
                condition_data["avg_return"] = float(np.mean(returns))
                condition_data["return_std"] = float(np.std(returns))
                condition_data["total_return"] = float(
                    (1 + np.array(returns)).prod() - 1
                )
                condition_data["win_rate"] = float(
                    condition_data["profitable_periods"] / condition_data["periods"]
                )
            else:
                condition_data["avg_return"] = 0.0
                condition_data["return_std"] = 0.0
                condition_data["total_return"] = 0.0
                condition_data["win_rate"] = 0.0

            if sharpe_ratios:
                valid_sharpe = [s for s in sharpe_ratios if not np.isnan(s)]
                condition_data["avg_sharpe"] = (
                    float(np.mean(valid_sharpe)) if valid_sharpe else 0.0
                )
            else:
                condition_data["avg_sharpe"] = 0.0

            if trades:
                condition_data["avg_trades"] = float(np.mean(trades))
                condition_data["total_trades"] = int(sum(trades))
            else:
                condition_data["avg_trades"] = 0.0
                condition_data["total_trades"] = 0

            # Clean up arrays to make JSON serializable
            del condition_data["returns"]
            del condition_data["sharpe_ratios"]
            del condition_data["trades"]

        return results

    def compare_all_strategies(
        self,
        historical_data: Dict[str, pd.DataFrame],
        short_window: int = 20,
        long_window: int = 50,
        market_window: int = 20,
    ) -> Dict:
        """
        Compare all strategies under different market conditions.

        Args:
            historical_data: Dict of DataFrames with historical price data
            short_window: Window for shorter moving averages
            long_window: Window for longer moving averages
            market_window: Window for market condition analysis

        Returns:
            Dict: Comprehensive comparison results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "short_window": short_window,
                "long_window": long_window,
                "market_window": market_window,
            },
            "strategies": {},
        }

        strategies = {
            "SMA": self.generate_sma_signals,
            "WMA": self.generate_wma_signals,
            "EMA": self.generate_ema_signals,
            "Bollinger": lambda df, symbol: self.generate_bollinger_signals(df, symbol),
            "Stochastic": lambda df, symbol: self.generate_stochastic_signals(
                df, symbol
            ),
        }

        for symbol, df in historical_data.items():
            results["strategies"][symbol] = {}

            for strategy_name, strategy_func in strategies.items():
                try:
                    # Generate strategy signals
                    if strategy_name in ["SMA", "WMA", "EMA"]:
                        strategy_results = strategy_func(
                            df, symbol, short_window, long_window
                        )
                    else:
                        strategy_results = strategy_func(df, symbol)

                    # Create signals DataFrame
                    signals = pd.DataFrame(index=df.index)
                    signals["price"] = df["close"]

                    # Extract signals based on strategy type
                    if strategy_name in ["SMA", "WMA", "EMA"]:
                        # For MA strategies, we need to reconstruct the signals
                        if strategy_name == "SMA":
                            short_ma = self.calculate_sma(df["close"], short_window)
                            long_ma = self.calculate_sma(df["close"], long_window)
                        elif strategy_name == "WMA":
                            short_ma = self.calculate_wma(df["close"], short_window)
                            long_ma = self.calculate_wma(df["close"], long_window)
                        else:  # EMA
                            short_ma = self.calculate_ema(df["close"], short_window)
                            long_ma = self.calculate_ema(df["close"], long_window)

                        signals["signal"] = self.identify_crossovers(short_ma, long_ma)

                    elif strategy_name == "Bollinger":
                        # For Bollinger Bands, generate signals directly
                        upper, middle, lower = self.calculate_bollinger_bands(
                            df["close"]
                        )
                        signals["signal"] = 0
                        signals.loc[df["close"] < lower, "signal"] = 1
                        signals.loc[df["close"] > upper, "signal"] = -1

                    else:  # Stochastic
                        # For Stochastic, generate signals directly
                        k_line, d_line = self.calculate_stochastic(df)
                        signals["signal"] = 0
                        signals.loc[
                            (k_line > 20) & (d_line > 20) & (k_line.shift(1) <= 20),
                            "signal",
                        ] = 1
                        signals.loc[
                            (k_line < 80) & (d_line < 80) & (k_line.shift(1) >= 80),
                            "signal",
                        ] = -1

                    # Calculate positions and returns
                    signals["position"] = signals["signal"].fillna(0).cumsum()
                    signals["returns"] = df["close"].pct_change().fillna(0)
                    signals["strategy_returns"] = (
                        signals["position"].shift(1) * signals["returns"]
                    )

                    # Evaluate strategy by market condition
                    market_performance = self.evaluate_strategy_by_market_condition(
                        df, signals, market_window
                    )

                    results["strategies"][symbol][strategy_name] = {
                        "overall_performance": strategy_results["performance"],
                        "market_condition_performance": market_performance,
                    }

                except Exception as e:
                    logging.error(
                        f"Error evaluating {strategy_name} for {symbol}: {str(e)}"
                    )
                    continue

        # Save comprehensive results
        self.save_predictions(results)

        return results
