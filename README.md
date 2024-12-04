# Cryptocurrency Market Intelligence System

A Python-based system for collecting and analyzing cryptocurrency market data using the CoinGecko API. This project is part of a larger initiative to develop AI-driven cryptocurrency market intelligence tools.

## Features

- Real-time cryptocurrency market data ingestion
- Automatic rate limit handling and retry mechanisms
- Structured data storage in CSV format
- Statistical summaries and logging
- Error handling and recovery

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

Run the data ingestion script:
```bash
python crypto_data_ingestion.py
```

The script will:
- Fetch current market data from CoinGecko API
- Save data to timestamped CSV files in the `data` directory
- Generate summary statistics in `latest_stats.json`
- Create detailed logs in `crypto_ingestion.log`

## Project Structure

```
├── crypto_data_ingestion.py   # Main data ingestion script
├── requirements.txt           # Python dependencies
├── data/                     # Directory for stored market data
│   ├── crypto_market_data_*.csv
│   └── latest_stats.json
└── crypto_ingestion.log      # Execution logs
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

[MIT License](LICENSE) 