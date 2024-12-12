# Getting Started with Crypto Analytics

## Installation

```bash
pip install crypto-analytics
```

## Basic Usage

```python
from crypto_analytics import MACDStrategy
from crypto_analytics.config import ConfigManager

# Initialize configuration
config = ConfigManager()
config.load_config("config.yaml")

# Create and run a MACD strategy
strategy = MACDStrategy(config)
results = strategy.run()
print(f"Strategy performance: {results.performance_metrics}")
```

## Next Steps

- Learn about [creating custom indicators](custom_indicators.md)
- Explore [creating custom strategies](custom_strategies.md)
- Check out the [example MACD strategy](../examples/macd_strategy.md) 