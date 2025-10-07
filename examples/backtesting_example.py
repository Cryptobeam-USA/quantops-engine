"""Example: Backtesting a strategy on historical data."""

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

from quantops.backtesting.backtester import Backtester
from quantops.strategies.momentum import MomentumStrategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_data(symbol: str, days: int = 365) -> pd.DataFrame:
    """Generate sample historical OHLCV data for demonstration."""
    start_date = datetime.now() - timedelta(days=days)
    
    dates = pd.date_range(start=start_date, periods=days * 24, freq='1H')
    
    # Generate synthetic price data with some trends
    close_prices = 50000 + np.cumsum(np.random.randn(len(dates)) * 100)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': close_prices + np.random.randn(len(dates)) * 50,
        'high': close_prices + abs(np.random.randn(len(dates)) * 100),
        'low': close_prices - abs(np.random.randn(len(dates)) * 100),
        'close': close_prices,
        'volume': np.random.rand(len(dates)) * 1000000
    })
    
    return df


async def main():
    logger.info("Starting backtest example...")
    
    # Generate sample historical data
    logger.info("Generating sample historical data...")
    historical_data = {
        "BTC/USDT": generate_sample_data("BTC/USDT", days=365),
        "ETH/USDT": generate_sample_data("ETH/USDT", days=365)
    }
    
    # Initialize backtester
    backtester = Backtester(
        initial_capital=100000.0,
        commission=0.001,  # 0.1% commission
        slippage=0.0005    # 0.05% slippage
    )
    
    # Create strategy
    strategy = MomentumStrategy({
        "name": "momentum_backtest",
        "symbols": ["BTC/USDT"],
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "position_size": 1.0  # Trade 1 BTC at a time
    })
    
    # Run backtest
    logger.info("Running backtest...")
    results = await backtester.run(strategy, historical_data)
    
    # Print results
    logger.info("\n" + "="*60)
    logger.info("BACKTEST RESULTS")
    logger.info("="*60)
    logger.info(f"Initial Capital: ${results['initial_capital']:,.2f}")
    logger.info(f"Final Value: ${results['final_value']:,.2f}")
    logger.info(f"Total Return: {results['total_return_pct']:.2f}%")
    logger.info(f"Number of Trades: {results['num_trades']}")
    logger.info(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    logger.info(f"Volatility: {results['volatility']:.2%}")
    logger.info(f"Max Drawdown: {results['max_drawdown_pct']:.2f}%")
    logger.info("="*60)
    
    # Get results as DataFrame
    results_df = backtester.get_results_dataframe()
    logger.info(f"\nEquity curve has {len(results_df)} data points")
    
    # Print sample trades
    if results['trades']:
        logger.info("\nSample Trades (first 5):")
        for trade in results['trades'][:5]:
            logger.info(f"  {trade['timestamp']}: {trade['action'].upper()} "
                       f"{trade['amount']} {trade['symbol']} @ ${trade['price']:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
