from strategies.macd_strategy import MACDStrategy
from utils.data_manager import DataManager
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def print_macd_results(results: dict, period_desc: str):
    """Print MACD strategy results in a readable format."""
    print(f"\nMACD Strategy Results - {period_desc}")
    print("=" * 50)

    for symbol in results["signals"]:
        perf = results["signals"][symbol]["performance"]
        latest = results["signals"][symbol]["latest_signal"]

        print(f"\n{symbol}:")
        print(f"Total Return: {perf['total_return']*100:.2f}%")
        print(f"Annual Return: {perf['annual_return']*100:.2f}%")
        print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
        print(f"Number of Trades: {perf['num_trades']}")

        print("\nLatest Signal:")
        print(f"Price: ${latest['price']:.2f}")
        print(f"MACD Line: {latest['macd_line']:.4f}")
        print(f"Signal Line: {latest['signal_line']:.4f}")
        print(f"Histogram: {latest['histogram']:.4f}")
        print(f"Signal: {latest['signal']} (1: Buy, -1: Sell, 0: Hold)")

    if "portfolio_metrics" in results:
        print("\nPortfolio Metrics:")
        metrics = results["portfolio_metrics"]
        print(f"Mean Return: {metrics['mean_return']*100:.2f}%")
        print(f"Return Std Dev: {metrics['std_return']*100:.2f}%")
        print(f"Mean Sharpe: {metrics['mean_sharpe']:.2f}")
        print(f"Best Symbol: {metrics['best_symbol']}")
        print(f"Worst Symbol: {metrics['worst_symbol']}")


def main():
    # Initialize data manager and strategy
    data_manager = DataManager()
    strategy = MACDStrategy(output_dir=data_manager.output_dir)

    # Prepare historical data
    logging.info("Preparing historical data...")
    symbols = ["BTC-USD", "ETH-USD", "XRP-USD"]
    historical_data = data_manager.fetch_historical_data(symbols, period="2y")

    if not historical_data:
        logging.error("No historical data available. Exiting...")
        return

    # Test different MACD parameter combinations
    parameter_sets = [
        # Standard settings
        {"fast": 12, "slow": 26, "signal": 9, "desc": "Standard (12/26/9)"},
        # Faster response
        {"fast": 8, "slow": 17, "signal": 9, "desc": "Fast (8/17/9)"},
        # Slower, more stable
        {"fast": 19, "slow": 39, "signal": 9, "desc": "Slow (19/39/9)"},
    ]

    # Run backtests with different parameters
    for params in parameter_sets:
        logging.info(f"\nTesting MACD strategy with {params['desc']} parameters...")
        try:
            results = strategy.backtest(
                historical_data,
                fast_period=params["fast"],
                slow_period=params["slow"],
                signal_period=params["signal"],
            )
            print_macd_results(results, params["desc"])

            # Save results with clean filename
            clean_desc = (
                params["desc"]
                .lower()
                .replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("/", "_")
            )
            data_manager.save_results(results, f"macd_{clean_desc}")

        except Exception as e:
            logging.error(f"Error testing MACD strategy: {str(e)}")
            continue

    logging.info(f"\nResults saved to {data_manager.results_dir}")


if __name__ == "__main__":
    main()
