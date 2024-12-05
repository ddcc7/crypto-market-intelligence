# Cryptocurrency Market Intelligence System

A Python-based system for collecting and analyzing cryptocurrency market data using the CoinGecko API. This project is part of a larger initiative to develop AI-driven cryptocurrency market intelligence tools.

## Features

- Real-time cryptocurrency market data ingestion
- Automatic rate limit handling and retry mechanisms
- Structured data storage in CSV format
- Statistical summaries and logging
- Error handling and recovery
- Technical Analysis
  - SMA Crossover Strategy
  - Performance Backtesting
  - Trading Signal Generation
  - Bollinger Bands Strategy
  - EMA Crossover Strategy
  - Stochastic Oscillator Strategy

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Ingestion
Run the data ingestion script:
```bash
python crypto_data_ingestion.py
```

The script will:
- Fetch current market data from CoinGecko API
- Save data to timestamped CSV files in the `data` directory
- Generate summary statistics in `latest_stats.json`
- Create detailed logs in `crypto_ingestion.log`

### Technical Analysis
The system includes a powerful technical analysis module with SMA crossover strategy:

```python
from crypto_analytics import CryptoAnalytics
from pathlib import Path

# Initialize analytics
analytics = CryptoAnalytics(output_dir=Path("data"))

# Load historical data (example format)
historical_data = {
    "BTC": pd.DataFrame({
        "close": [...],  # Close prices
        "timestamp": [...],  # Timestamps
    }).set_index("timestamp"),
    "ETH": pd.DataFrame({...}),
}

# Run backtest with custom parameters
results = analytics.backtest_sma_strategy(
    historical_data,
    short_window=20,  # 20-day short SMA
    long_window=50    # 50-day long SMA
)

# Results will be saved to data/predictions.json
```

# Bollinger Bands Strategy
The system also implements Bollinger Bands for generating trading signals:

```python
# Run Bollinger Bands strategy
results = analytics.backtest_bollinger_strategy(
    historical_data,
    window=20,       # 20-day moving average
    num_std=2.0      # 2 standard deviations for bands
)
```

The Bollinger Bands strategy:
- Calculates middle band (20-day SMA by default)
- Generates upper and lower bands (±2 standard deviations)
- Identifies oversold (price below lower band) and overbought (price above upper band) conditions
- Provides comprehensive performance metrics and trading signals

Output includes:
- Band values (upper, middle, lower)
- Trading signals (-1 for sell, 1 for buy)
- Performance metrics (returns, Sharpe ratio)
- Portfolio-level analysis

# EMA Strategy
The system implements Exponential Moving Average (EMA) for generating trading signals:

```python
# Run EMA strategy
results = analytics.backtest_ema_strategy(
    historical_data,
    short_window=20,  # 20-day short EMA
    long_window=50    # 50-day long EMA
)

# Compare all strategies (SMA, WMA, EMA)
comparison = analytics.compare_all_strategies(
    historical_data,
    short_window=20,
    long_window=50
)
```

The EMA strategy:
- Calculates exponential moving averages with higher weights on recent prices
- Identifies bullish (short crosses above long) and bearish (short crosses below long) signals
- Provides performance comparison with SMA and WMA strategies
- Supports multiple timeframe analysis (short/medium/long-term)

Output includes:
- Trading signals and positions
- Performance metrics (returns, Sharpe ratio)
- Strategy comparison analytics
- Portfolio-level analysis

# Stochastic Oscillator Strategy
The system implements Stochastic Oscillator for generating trading signals:

```python
# Run Stochastic strategy
results = analytics.backtest_stochastic_strategy(
    historical_data,
    k_period=14,    # Period for %K line
    d_period=3,     # Period for %D line
    overbought=80,  # Overbought threshold
    oversold=20     # Oversold threshold
)

# Compare with other strategies
comparison = analytics.compare_all_strategies(
    historical_data,
    short_window=20,  # For MA strategies
    long_window=50,
    k_period=14,      # For Stochastic
    d_period=3
)
```

The Stochastic strategy:
- Calculates %K (fast) and %D (slow) lines
- Identifies overbought and oversold conditions
- Generates buy signals when crossing above oversold
- Generates sell signals when crossing below overbought
- Provides comparison with moving average strategies

Output includes:
- %K and %D line values
- Trading signals and positions
- Performance metrics (returns, Sharpe ratio)
- Strategy comparison analytics

## Project Structure

```
├── crypto_data_ingestion.py   # Main data ingestion script
├── crypto_analytics.py        # Technical analysis and signal generation
├── requirements.txt           # Python dependencies
├── data/                     # Directory for stored market data
│   ├── crypto_market_data_*.csv
│   ├── latest_stats.json
│   └── predictions.json      # Trading signals and backtest results
└── crypto_ingestion.log      # Execution logs
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

[MIT License](LICENSE) 