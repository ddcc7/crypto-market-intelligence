"""Breakout trading strategy implementation."""

import pandas as pd
import numpy as np
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy
from ..indicators import BaseIndicator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BreakoutStrategy(BaseStrategy):
    """Breakout trading strategy implementation."""

    def __init__(
        self,
        config_path: str = "config/trading_params.yaml",
        indicators: Optional[List[BaseIndicator]] = None,
    ):
        """Initialize strategy with parameters from config file."""
        super().__init__(indicators)

        # Load config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)["breakout_strategy"]

        # Strategy parameters
        self.lookback_period = config["lookback_period"]
        self.volume_factor = config["volume_factor"]
        self.resistance_periods = config["resistance_periods"]

        # Risk management
        self.profit_target = config["profit_target"]
        self.stop_loss = config["stop_loss"]

        # Trade management
        self.min_bars_between_trades = config["min_bars_between_trades"]
        self.max_consecutive_losses = config["max_consecutive_losses"]

        # Volatility adjustments
        self.atr_multiplier = config["atr_multiplier"]
        self.min_momentum = config["min_momentum"]
        self.min_breakout_size = config["min_breakout_size"]

        # Volume thresholds
        self.volume_std_multiplier = config["volume_std_multiplier"]

        logger.info("Strategy initialized with parameters:")
        logger.info(f"Lookback period: {self.lookback_period}")
        logger.info(f"Volume factor: {self.volume_factor}")
        logger.info(f"Min momentum: {self.min_momentum}")
        logger.info(f"Min breakout size: {self.min_breakout_size}")

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate trading signals for the given data."""
        # Call parent's calculate_signals first
        signals = super().calculate_signals(data)

        # Add required price data
        signals["high"] = data["high"]
        signals["low"] = data["low"]
        signals["volume"] = data["volume"]

        # Calculate ATR
        tr = pd.DataFrame(
            {
                "hl": data["high"] - data["low"],
                "hc": abs(data["high"] - data["close"].shift(1)),
                "lc": abs(data["low"] - data["close"].shift(1)),
            }
        ).max(axis=1)
        signals["atr"] = tr.rolling(window=self.resistance_periods).mean()

        # Calculate volume metrics
        signals["avg_volume"] = (
            data["volume"].rolling(window=self.lookback_period).mean()
        )

        # Identify resistance levels
        signals["resistance_level"] = None
        resistance_mask = self.identify_resistance(data)
        signals.loc[resistance_mask, "resistance_level"] = data.loc[
            resistance_mask, "high"
        ]

        # Initialize stop loss and take profit columns
        signals["stop_loss"] = None
        signals["take_profit"] = None

        return signals

    def identify_resistance(self, data: pd.DataFrame) -> pd.Series:
        """Identify resistance and support levels using local highs and lows."""
        # Calculate rolling max/min of highs/lows
        highs = data["high"].rolling(window=self.resistance_periods, center=False).max()
        lows = data["low"].rolling(window=self.resistance_periods, center=False).min()

        # Calculate average true range for dynamic thresholds
        tr = pd.DataFrame(
            {
                "hl": data["high"] - data["low"],
                "hc": abs(data["high"] - data["close"].shift(1)),
                "lc": abs(data["low"] - data["close"].shift(1)),
            }
        ).max(axis=1)
        atr = tr.rolling(window=self.resistance_periods).mean()

        # Calculate volume profile
        volume_ma = data["volume"].rolling(window=self.lookback_period).mean()
        volume_std = data["volume"].rolling(window=self.lookback_period).std()
        high_volume = data["volume"] > (
            volume_ma + volume_std * self.volume_std_multiplier
        )

        # Calculate price momentum
        returns = data["close"].pct_change()
        momentum = returns.rolling(window=3).sum()

        # A point is resistance if:
        # 1. It's a local high (higher than previous and next periods)
        # 2. Price hasn't exceeded it in the recent lookback period
        # 3. The high is significant compared to ATR
        # 4. Volume is above average or momentum is positive
        is_local_high = (data["high"] > data["high"].shift(1)) & (
            data["high"] > data["high"].shift(-1)
        )
        not_exceeded_high = (
            data["high"].rolling(window=self.lookback_period, center=False).max()
            <= data["high"]
        )
        is_significant_high = (data["high"] - data["low"]) > (
            atr * self.min_breakout_size
        )
        has_momentum_up = momentum > 0

        is_resistance = (
            is_local_high
            & not_exceeded_high
            & is_significant_high
            & (high_volume | has_momentum_up)
        )

        # A point is support if:
        # 1. It's a local low (lower than previous and next periods)
        # 2. Price hasn't gone below it in the recent lookback period
        # 3. The low is significant compared to ATR
        # 4. Volume is above average or momentum is negative
        is_local_low = (data["low"] < data["low"].shift(1)) & (
            data["low"] < data["low"].shift(-1)
        )
        not_exceeded_low = (
            data["low"].rolling(window=self.lookback_period, center=False).min()
            >= data["low"]
        )
        is_significant_low = (data["high"] - data["low"]) > (
            atr * self.min_breakout_size
        )
        has_momentum_down = momentum < 0

        is_support = (
            is_local_low
            & not_exceeded_low
            & is_significant_low
            & (high_volume | has_momentum_down)
        )

        # Log levels found
        resistance_count = is_resistance.sum()
        support_count = is_support.sum()
        logger.info(
            f"Found {resistance_count} resistance and {support_count} support points"
        )

        # Create a series that marks both resistance (1) and support (-1) levels
        levels = pd.Series(0, index=data.index)
        levels[is_resistance] = 1
        levels[is_support] = -1

        return levels

    def generate_signal_rules(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on breakout conditions."""
        current_position = 0
        last_level = None
        last_trade_price = None
        consecutive_losses = 0
        last_trade_time = None

        # Initialize signal column if not present
        signals["signal"] = 0

        for i in range(self.lookback_period, len(signals)):
            # Update position based on previous signal
            if i > 0:
                current_position = (
                    signals["position"].iloc[i - 1]
                    if "position" in signals.columns
                    else current_position
                )

            # Get current prices and levels
            current_close = signals["price"].iloc[i]
            current_high = signals["high"].iloc[i]
            current_low = signals["low"].iloc[i]
            current_volume = signals["volume"].iloc[i]
            avg_volume = signals["avg_volume"].iloc[i]
            atr = signals["atr"].iloc[i]

            # Check for exit conditions if in a position
            if current_position != 0:
                stop_loss = signals["stop_loss"].iloc[i - 1]
                take_profit = signals["take_profit"].iloc[i - 1]

                # Dynamic exit conditions based on ATR and price action
                if current_position > 0:
                    trailing_stop = max(
                        stop_loss, current_high - atr * self.atr_multiplier
                    )
                    if current_low <= trailing_stop or current_high >= take_profit:
                        signals.loc[signals.index[i], "signal"] = -current_position
                        current_position = 0
                        last_level = None
                        last_trade_time = i

                        logger.info(f"Long exit signal at {signals.index[i]}")
                        logger.info(f"Exit price: {current_close}")
                        if current_low <= trailing_stop:
                            logger.info("Exit reason: Stop loss hit")
                            if (
                                last_trade_price is not None
                                and current_low < last_trade_price
                            ):
                                consecutive_losses += 1
                                logger.info(f"Consecutive losses: {consecutive_losses}")
                            else:
                                consecutive_losses = 0
                        else:
                            logger.info("Exit reason: Take profit hit")
                            consecutive_losses = 0
                else:  # Short position
                    trailing_stop = min(
                        stop_loss, current_low + atr * self.atr_multiplier
                    )
                    if current_high >= trailing_stop or current_low <= take_profit:
                        signals.loc[signals.index[i], "signal"] = -current_position
                        current_position = 0
                        last_level = None
                        last_trade_time = i

                        logger.info(f"Short exit signal at {signals.index[i]}")
                        logger.info(f"Exit price: {current_close}")
                        if current_high >= trailing_stop:
                            logger.info("Exit reason: Stop loss hit")
                            if (
                                last_trade_price is not None
                                and current_high > last_trade_price
                            ):
                                consecutive_losses += 1
                                logger.info(f"Consecutive losses: {consecutive_losses}")
                            else:
                                consecutive_losses = 0
                        else:
                            logger.info("Exit reason: Take profit hit")
                            consecutive_losses = 0

            # Check for entry conditions if not in a position
            elif current_position == 0:
                # Skip trading if too many consecutive losses or too soon after last trade
                if consecutive_losses >= self.max_consecutive_losses:
                    continue
                if (
                    last_trade_time is not None
                    and i - last_trade_time < self.min_bars_between_trades
                ):
                    continue

                # Get current level
                level = signals["resistance_level"].iloc[i]

                # Only consider new levels
                if level != last_level and level != 0:
                    # Calculate breakout metrics
                    breakout_size = abs(current_close - signals["price"].iloc[i - 1])
                    volume_increase = current_volume / avg_volume
                    price_momentum = (
                        current_close - signals["price"].iloc[i - 1]
                    ) / signals["price"].iloc[i - 1]

                    # Calculate volatility-adjusted thresholds
                    volatility_factor = min(1.5, max(0.8, atr / current_close * 100))
                    min_breakout_size = atr * self.min_breakout_size * volatility_factor
                    min_volume_increase = self.volume_factor * (
                        1 - (volatility_factor - 1) * 0.2
                    )
                    min_momentum = self.min_momentum * volatility_factor

                    # Log entry conditions
                    logger.info(f"\nAnalyzing potential entry at {signals.index[i]}")
                    logger.info(f"Current close: {current_close}")
                    logger.info(f"Level: {level}")
                    logger.info(
                        f"Breakout size: {breakout_size} (min: {min_breakout_size})"
                    )
                    logger.info(
                        f"Volume increase: {volume_increase:.2f}x (min: {min_volume_increase:.2f}x)"
                    )
                    logger.info(
                        f"Price momentum: {price_momentum:.4f} (min: {min_momentum:.4f})"
                    )

                    # Check for long entry (resistance breakout)
                    if (
                        level == 1
                        and current_close > signals["high"].iloc[i - 1]
                        and volume_increase > min_volume_increase
                        and breakout_size > min_breakout_size
                        and price_momentum > min_momentum
                    ):

                        signals.loc[signals.index[i], "signal"] = 1
                        current_position = 1
                        last_level = level
                        last_trade_price = current_close
                        last_trade_time = i

                        # Set dynamic stop loss and take profit based on ATR and volatility
                        stop_distance = max(
                            atr * 0.8,
                            current_close * self.stop_loss * volatility_factor,
                        )
                        profit_distance = max(
                            atr * 1.2,
                            current_close * self.profit_target * volatility_factor,
                        )

                        signals.loc[signals.index[i], "stop_loss"] = (
                            current_close - stop_distance
                        )
                        signals.loc[signals.index[i], "take_profit"] = (
                            current_close + profit_distance
                        )

                        logger.info("Long entry signal generated!")
                        logger.info(f"Entry price: {current_close}")
                        logger.info(f"Stop loss: {current_close - stop_distance}")
                        logger.info(f"Take profit: {current_close + profit_distance}")

                    # Check for short entry (support breakdown)
                    elif (
                        level == -1
                        and current_close < signals["low"].iloc[i - 1]
                        and volume_increase > min_volume_increase
                        and breakout_size > min_breakout_size
                        and price_momentum < -min_momentum
                    ):

                        signals.loc[signals.index[i], "signal"] = -1
                        current_position = -1
                        last_level = level
                        last_trade_price = current_close
                        last_trade_time = i

                        # Set dynamic stop loss and take profit based on ATR and volatility
                        stop_distance = max(
                            atr * 0.8,
                            current_close * self.stop_loss * volatility_factor,
                        )
                        profit_distance = max(
                            atr * 1.2,
                            current_close * self.profit_target * volatility_factor,
                        )

                        signals.loc[signals.index[i], "stop_loss"] = (
                            current_close + stop_distance
                        )
                        signals.loc[signals.index[i], "take_profit"] = (
                            current_close - profit_distance
                        )

                        logger.info("Short entry signal generated!")
                        logger.info(f"Entry price: {current_close}")
                        logger.info(f"Stop loss: {current_close + stop_distance}")
                        logger.info(f"Take profit: {current_close - profit_distance}")

            # Update position
            signals.loc[signals.index[i], "position"] = current_position

        # Log final statistics
        total_entries = (signals["signal"] != 0).sum()
        long_entries = (signals["signal"] == 1).sum()
        short_entries = (signals["signal"] == -1).sum()
        logger.info(f"\nStrategy Statistics:")
        logger.info(f"Total entries: {total_entries}")
        logger.info(f"Long entries: {long_entries}")
        logger.info(f"Short entries: {short_entries}")

        return signals
