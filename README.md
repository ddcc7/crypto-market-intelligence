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
  - WMA Crossover Strategy
  - EMA Crossover Strategy
  - Bollinger Bands Strategy
  - Stochastic Oscillator Strategy
  - Market Conditions Analysis
    - Trend Detection
    - Volatility Analysis
    - Strategy Performance by Market State

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
The system includes a comprehensive technical analysis module with multiple strategies:

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

# Compare strategies under different market conditions
results = analytics.compare_all_strategies(
    historical_data,
    short_window=20,    # For MA strategies
    long_window=50,     # For MA strategies
    market_window=20    # For market condition analysis
)
```

### Market Conditions Analysis
The system now includes advanced market condition classification and strategy evaluation:

1. Market Condition Types:
   - Trending Up: Strong upward price movement
   - Trending Down: Strong downward price movement
   - Ranging: Sideways price movement
   - Volatile: High price volatility

2. Strategy Evaluation by Market State:
   ```python
   # Run market condition analysis
   results = analytics.compare_all_strategies(historical_data)
   
   # Results include:
   # - Overall strategy performance
   # - Performance metrics by market condition
   # - Comparative analysis across strategies
   ```

3. Performance Metrics:
   - Returns (total and average)
   - Sharpe ratios
   - Number of trades
   - Return volatility
   - Market condition distribution

Results are saved to `data/predictions.json` with detailed performance metrics for each strategy under different market conditions.

## Testing
Run the test suite:
```bash
python test_market_conditions.py  # Test market condition analysis
python test_strategies.py         # Test trading strategies
```

## License
MIT License - see LICENSE file for details. 