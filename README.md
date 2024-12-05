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

The strategy:
- Calculates short and long-term Simple Moving Averages (SMA)
- Identifies bullish (short crosses above long) and bearish (short crosses below long) signals
- Generates trading signals and calculates performance metrics
- Provides portfolio-level analysis across multiple cryptocurrencies

Output includes:
- Entry/exit signals
- Total and annual returns
- Sharpe ratio
- Number of trades
- Current positions
- Portfolio-level metrics

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