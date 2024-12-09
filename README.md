# Cryptocurrency Market Intelligence System

A modular Python-based system for analyzing cryptocurrency markets using various technical indicators and trading strategies.

## Project Structure

```
crypto_analytics/
├── src/
│   └── crypto_analytics/
│       ├── strategies/      # Trading strategies
│       ├── indicators/      # Technical indicators
│       ├── utils/          # Utility functions
│       ├── config/         # Configuration management
│       └── data/           # Data storage
├── tests/                  # Test suite
└── docs/                   # Documentation
```

## Features

### Technical Indicators
- MACD (Moving Average Convergence Divergence)
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- Bollinger Bands
- Stochastic Oscillator

### Trading Strategies
- MACD Crossover
- Moving Average Crossover
- Bollinger Bands Mean Reversion
- Stochastic Oscillator

### Performance Analytics
- Total and Annual Returns
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Portfolio Correlation Matrix

## Installation

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

### Basic Example
```python
from src.crypto_analytics.strategies import MACDStrategy
from src.crypto_analytics.utils import DataManager
from src.crypto_analytics.config import ConfigManager

# Initialize components
config = ConfigManager()
data_manager = DataManager()
strategy = MACDStrategy()

# Fetch data and run strategy
symbols = ["BTC-USD", "ETH-USD"]
data = data_manager.fetch_historical_data(symbols)
results = strategy.backtest(data)
```

### Configuration
The system uses a configuration file (`config.json`) for default parameters:

```json
{
    "data": {
        "historical_dir": "data/historical",
        "results_dir": "data/results",
        "default_period": "2y",
        "default_interval": "1d"
    },
    "strategies": {
        "macd": {
            "default_fast_period": 12,
            "default_slow_period": 26,
            "default_signal_period": 9
        }
    }
}
```

### Adding New Strategies
1. Create a new indicator in `src/crypto_analytics/indicators/`
2. Create a new strategy in `src/crypto_analytics/strategies/`
3. Add tests in `tests/`

## Testing
Run the test suite:
```bash
python -m pytest tests/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License - see LICENSE file for details. 