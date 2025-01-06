"""Adaptive strategy framework for cryptocurrency trading."""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class MarketRegime(Enum):
    """Market regime classification."""

    STRONG_BULL = "strong_bull"
    WEAK_BULL = "weak_bull"
    SIDEWAYS = "sideways"
    WEAK_BEAR = "weak_bear"
    STRONG_BEAR = "strong_bear"
    HIGH_VOL = "high_volatility"
    LOW_VOL = "low_volatility"


@dataclass
class MarketContext:
    """Market context information."""

    regime: MarketRegime
    trend_strength: float
    volatility: float
    volume_trend: float
    risk_level: float


@dataclass
class PositionConfig:
    """Position configuration parameters."""

    max_position_size: float = 1.0
    max_portfolio_heat: float = 0.5
    base_risk_per_trade: float = 0.02
    max_correlation: float = 0.7
    min_volatility: float = 0.01
    max_volatility: float = 0.5


class AdaptiveStrategy(ABC):
    """Base class for adaptive trading strategies."""

    def __init__(
        self,
        position_config: Optional[PositionConfig] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        """Initialize strategy.

        Args:
            position_config: Position and risk configuration
            params: Strategy-specific parameters
        """
        self.position_config = position_config or PositionConfig()
        self.params = params or {}
        self.current_context = None

    def detect_market_regime(self, data: pd.DataFrame) -> MarketContext:
        """Detect current market regime and context.

        Args:
            data: Market data with OHLCV prices

        Returns:
            MarketContext object with regime classification
        """
        # Calculate trend strength using ADX
        high_low = data["High"] - data["Low"]
        high_close = np.abs(data["High"] - data["Close"].shift())
        low_close = np.abs(data["Low"] - data["Close"].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(14).mean()

        # Calculate directional movement
        plus_dm = data["High"].diff()
        minus_dm = -data["Low"].diff()
        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

        # Smooth directional movement
        plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(14).mean()

        # Calculate volatility regime
        returns = data["Close"].pct_change()
        volatility = returns.rolling(20).std() * np.sqrt(252)

        # Calculate volume trend
        volume_sma = data["Volume"].rolling(20).mean()
        volume_trend = (data["Volume"] / volume_sma - 1).rolling(5).mean()

        # Determine market regime
        if adx.iloc[-1] > 25:
            if plus_di.iloc[-1] > minus_di.iloc[-1]:
                regime = (
                    MarketRegime.STRONG_BULL
                    if plus_di.iloc[-1] > 30
                    else MarketRegime.WEAK_BULL
                )
            else:
                regime = (
                    MarketRegime.STRONG_BEAR
                    if minus_di.iloc[-1] > 30
                    else MarketRegime.WEAK_BEAR
                )
        else:
            regime = MarketRegime.SIDEWAYS

        # Override with volatility regime if extreme
        if volatility.iloc[-1] > self.position_config.max_volatility:
            regime = MarketRegime.HIGH_VOL
        elif volatility.iloc[-1] < self.position_config.min_volatility:
            regime = MarketRegime.LOW_VOL

        # Calculate risk level (0 to 1)
        risk_level = min(
            1.0,
            max(
                0.0,
                (volatility.iloc[-1] - self.position_config.min_volatility)
                / (
                    self.position_config.max_volatility
                    - self.position_config.min_volatility
                ),
            ),
        )

        return MarketContext(
            regime=regime,
            trend_strength=adx.iloc[-1] / 100.0,
            volatility=volatility.iloc[-1],
            volume_trend=volume_trend.iloc[-1],
            risk_level=risk_level,
        )

    def calculate_position_size(self, signal: float, context: MarketContext) -> float:
        """Calculate appropriate position size based on market context.

        Args:
            signal: Raw trading signal (-1 to 1)
            context: Current market context

        Returns:
            Position size (-1 to 1)
        """
        # Base position size from signal
        position = signal * self.position_config.max_position_size

        # Adjust for market regime
        regime_factors = {
            MarketRegime.STRONG_BULL: 1.0,
            MarketRegime.WEAK_BULL: 0.7,
            MarketRegime.SIDEWAYS: 0.5,
            MarketRegime.WEAK_BEAR: 0.3,
            MarketRegime.STRONG_BEAR: 0.2,
            MarketRegime.HIGH_VOL: 0.3,
            MarketRegime.LOW_VOL: 0.4,
        }
        position *= regime_factors[context.regime]

        # Adjust for trend strength
        position *= 0.5 + 0.5 * context.trend_strength

        # Adjust for risk level
        position *= 1.0 - 0.5 * context.risk_level

        # Apply portfolio heat limit
        position = np.clip(
            position,
            -self.position_config.max_portfolio_heat,
            self.position_config.max_portfolio_heat,
        )

        return position

    def calculate_adaptive_stops(
        self, data: pd.DataFrame, position: float, context: MarketContext
    ) -> Tuple[float, float]:
        """Calculate adaptive stop loss and take profit levels.

        Args:
            data: Market data
            position: Current position size
            context: Market context

        Returns:
            Tuple of (stop_loss_price, take_profit_price)
        """
        current_price = data["Close"].iloc[-1]
        atr = data["High"].rolling(14).max() - data["Low"].rolling(14).min()

        # Base stops on ATR and regime
        regime_stop_factors = {
            MarketRegime.STRONG_BULL: 3.0,
            MarketRegime.WEAK_BULL: 2.5,
            MarketRegime.SIDEWAYS: 2.0,
            MarketRegime.WEAK_BEAR: 1.5,
            MarketRegime.STRONG_BEAR: 1.0,
            MarketRegime.HIGH_VOL: 4.0,
            MarketRegime.LOW_VOL: 1.5,
        }

        stop_distance = atr.iloc[-1] * regime_stop_factors[context.regime]

        # Adjust for position size and risk level
        stop_distance *= 1.0 + abs(position)
        stop_distance *= 1.0 + context.risk_level

        if position > 0:
            stop_loss = current_price - stop_distance
            take_profit = current_price + (stop_distance * 1.5)
        elif position < 0:
            stop_loss = current_price + stop_distance
            take_profit = current_price - (stop_distance * 1.5)
        else:
            stop_loss = take_profit = current_price

        return stop_loss, take_profit

    @abstractmethod
    def calculate_raw_signal(self, data: pd.DataFrame) -> float:
        """Calculate raw trading signal.

        Args:
            data: Market data

        Returns:
            Signal value between -1 and 1
        """
        pass

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate trading signals with position sizing and risk management.

        Args:
            data: Market data with OHLCV prices

        Returns:
            DataFrame with signals and positions
        """
        signals = data.copy()
        signals["signal"] = 0.0
        signals["position"] = 0.0
        signals["stop_loss"] = signals["Close"]
        signals["take_profit"] = signals["Close"]
        signals["price"] = signals[
            "Close"
        ]  # Set price column for performance calculation

        # Initialize with first observation
        self.current_context = self.detect_market_regime(
            signals.iloc[: max(20, len(signals) // 10)]
        )

        for i in range(20, len(signals)):
            # Update market context every 5 periods
            if i % 5 == 0:
                self.current_context = self.detect_market_regime(
                    signals.iloc[max(0, i - 100) : i + 1]
                )

            # Calculate raw signal
            raw_signal = self.calculate_raw_signal(
                signals.iloc[max(0, i - 100) : i + 1]
            )

            # Calculate position size
            position = self.calculate_position_size(raw_signal, self.current_context)

            # Calculate stops
            stop_loss, take_profit = self.calculate_adaptive_stops(
                signals.iloc[max(0, i - 100) : i + 1], position, self.current_context
            )

            # Check if we hit stops
            current_price = signals["Close"].iloc[i]
            prev_position = signals["position"].iloc[i - 1]

            if prev_position != 0:
                prev_stop = signals["stop_loss"].iloc[i - 1]
                prev_target = signals["take_profit"].iloc[i - 1]

                if (prev_position > 0 and current_price <= prev_stop) or (
                    prev_position < 0 and current_price >= prev_stop
                ):
                    # Stop loss hit
                    position = 0
                elif (prev_position > 0 and current_price >= prev_target) or (
                    prev_position < 0 and current_price <= prev_target
                ):
                    # Take profit hit
                    position = 0

            # Record signal if position changed
            if position != prev_position:
                signals.iloc[i, signals.columns.get_loc("signal")] = (
                    position - prev_position
                )

            # Update position and stops
            signals.iloc[i, signals.columns.get_loc("position")] = position
            signals.iloc[i, signals.columns.get_loc("stop_loss")] = stop_loss
            signals.iloc[i, signals.columns.get_loc("take_profit")] = take_profit

        return signals
