# Getting Started with QuantOps Engine

This guide will help you get started with QuantOps Engine quickly.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/REDDNoC/quantops-engine.git
cd quantops-engine
pip install -r requirements.txt
pip install -e .
```

## Configuration

### 1. Create Environment File

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET=your_binance_secret
INITIAL_CAPITAL=100000.0
```

### 2. Create Configuration File

Copy the example config:

```bash
cp config.example.json config.json
```

Edit `config.json` to customize:
- Trading symbols
- Strategy parameters
- Risk management settings
- AI agent configuration

## Your First Strategy

### Simple Buy/Sell Strategy

```python
import asyncio
from quantops.strategies.base import BaseStrategy

class SimpleStrategy(BaseStrategy):
    async def generate_signal(self, market_data):
        symbol = "BTC/USDT"
        
        if symbol not in market_data:
            return None
        
        price = market_data[symbol]["ticker"]["last"]
        
        # Buy when price is below threshold
        if price < 45000:
            return {
                "action": "buy",
                "symbol": symbol,
                "amount": 0.1
            }
        # Sell when price is above threshold
        elif price > 55000:
            return {
                "action": "sell",
                "symbol": symbol,
                "amount": 0.1
            }
        
        return None
```

### Running Your Strategy

```python
import asyncio
from quantops import TradingEngine
from quantops.config.settings import load_config

async def main():
    config = load_config("config.json")
    engine = TradingEngine(config)
    
    strategy = SimpleStrategy({
        "name": "my_strategy",
        "symbols": ["BTC/USDT"]
    })
    
    engine.add_strategy(strategy)
    await engine.start()

if __name__ == "__main__":
    asyncio.run(main())
```

## Backtesting

Test your strategy on historical data before risking real capital:

```python
import asyncio
import pandas as pd
from quantops.backtesting.backtester import Backtester

async def run_backtest():
    # Load your historical data
    historical_data = {
        "BTC/USDT": pd.read_csv("btc_historical.csv")
    }
    
    backtester = Backtester(
        initial_capital=100000.0,
        commission=0.001
    )
    
    strategy = SimpleStrategy({
        "name": "test",
        "symbols": ["BTC/USDT"]
    })
    
    results = await backtester.run(strategy, historical_data)
    
    print(f"Return: {results['total_return_pct']:.2f}%")
    print(f"Sharpe: {results['sharpe_ratio']:.2f}")
    print(f"Max DD: {results['max_drawdown_pct']:.2f}%")

asyncio.run(run_backtest())
```

## Using the API

Start the API server:

```bash
uvicorn quantops.api.app:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Calls

```python
import requests

# Check status
response = requests.get("http://localhost:8000/status")
print(response.json())

# Start engine
response = requests.post("http://localhost:8000/engine/start")
print(response.json())

# Get portfolio
response = requests.get("http://localhost:8000/portfolio")
print(response.json())
```

## Next Steps

1. **Explore Examples**: Check the `examples/` directory for more examples
2. **Read Documentation**: Review the README and API documentation
3. **Create Strategies**: Develop custom strategies using technical indicators
4. **Test Thoroughly**: Always backtest before live trading
5. **Join Community**: Contribute and get help on GitHub

## Common Issues

### ModuleNotFoundError
```bash
pip install -e .
```

### API Key Errors
- Verify your `.env` file has correct API keys
- Check exchange API key permissions
- Ensure keys are not expired

### Connection Errors
- Check internet connectivity
- Verify exchange API endpoints are accessible
- Review rate limiting settings

## Resources

- [Full Documentation](README.md)
- [API Reference](http://localhost:8000/docs)
- [Contributing Guide](CONTRIBUTING.md)
- [Example Scripts](examples/)
- [GitHub Issues](https://github.com/REDDNoC/quantops-engine/issues)

## Warning

⚠️ **IMPORTANT**: This software is for educational purposes only. Trading cryptocurrencies involves substantial risk. Never trade with money you can't afford to lose. Always test strategies thoroughly on historical data before live trading.
