from .base_strategy import BaseStrategy
import pandas as pd
from typing import Dict, Any
from datetime import datetime
import numpy as np
import logging


class MACDStrategy(BaseStrategy):
    """MACD (Moving Average Convergence Divergence) trading strategy."""

    def calculate_macd(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> pd.DataFrame:
        """Calculate MACD indicators."""
        # Calculate EMAs
        fast_ema = df["close"].ewm(span=fast_period, adjust=False).mean()
        slow_ema = df["close"].ewm(span=slow_period, adjust=False).mean()

        # Calculate MACD line and Signal line
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        return pd.DataFrame(
            {
                "macd_line": macd_line,
                "signal_line": signal_line,
                "histogram": histogram,
            },
            index=df.index,
        )

    def generate_signals(
        self,
        df: pd.DataFrame,
        symbol: str,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> Dict[str, Any]:
        """Generate trading signals based on MACD crossovers."""
        signals = pd.DataFrame(index=df.index)
        signals["price"] = df["close"]

        # Calculate MACD indicators
        macd_data = self.calculate_macd(df, fast_period, slow_period, signal_period)
        signals = pd.concat([signals, macd_data], axis=1)

        # Generate signals on crossovers
        signals["signal"] = 0
        signals.loc[
            (signals["macd_line"] > signals["signal_line"])
            & (signals["macd_line"].shift(1) <= signals["signal_line"].shift(1)),
            "signal",
        ] = 1  # Buy signal

        signals.loc[
            (signals["macd_line"] < signals["signal_line"])
            & (signals["macd_line"].shift(1) >= signals["signal_line"].shift(1)),
            "signal",
        ] = -1  # Sell signal

        # Calculate strategy returns
        signals["position"] = signals["signal"].cumsum()
        signals["returns"] = signals["price"].pct_change()
        signals["strategy_returns"] = signals["position"].shift(1) * signals["returns"]

        # Calculate performance metrics
        performance = self.calculate_performance_metrics(signals)

        return {
            "symbol": symbol,
            "strategy": self.name,
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "fast_period": fast_period,
                "slow_period": slow_period,
                "signal_period": signal_period,
            },
            "performance": performance,
            "current_position": int(signals["position"].iloc[-1]),
            "latest_signal": {
                "timestamp": signals.index[-1].isoformat(),
                "price": float(signals["price"].iloc[-1]),
                "macd_line": float(signals["macd_line"].iloc[-1]),
                "signal_line": float(signals["signal_line"].iloc[-1]),
                "histogram": float(signals["histogram"].iloc[-1]),
                "signal": int(signals["signal"].iloc[-1]),
            },
        }

    def backtest(
        self,
        historical_data: Dict[str, pd.DataFrame],
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> Dict[str, Any]:
        """Backtest MACD strategy across multiple cryptocurrencies."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "strategy": self.name,
            "parameters": {
                "fast_period": fast_period,
                "slow_period": slow_period,
                "signal_period": signal_period,
            },
            "signals": {},
        }

        # Generate signals for each symbol
        for symbol, df in historical_data.items():
            try:
                symbol_results = self.generate_signals(
                    df, symbol, fast_period, slow_period, signal_period
                )
                results["signals"][symbol] = symbol_results
            except Exception as e:
                logging.error(f"Error generating MACD signals for {symbol}: {str(e)}")
                continue

        # Calculate portfolio-level metrics
        if results["signals"]:
            results["portfolio_metrics"] = self.calculate_portfolio_metrics(
                results["signals"]
            )

        return results
