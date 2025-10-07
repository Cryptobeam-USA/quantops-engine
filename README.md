# QuantOps Engine

**Algorithmic Liquidity & Quantitative Strategy Engine**

Python-based quantitative trading engine powering Cryptobeam's liquidity algorithms. Integrates with CCXT for multi-exchange execution, backtesting modules, and agent swarm AI models for autonomous market-making.

## Features

- 🔄 **Multi-Exchange Support**: Seamless integration with 100+ cryptocurrency exchanges via CCXT
- 📊 **Backtesting Framework**: Comprehensive backtesting with realistic fee modeling and slippage
- 🤖 **AI Agent Swarm**: TensorFlow-powered agent swarm for autonomous decision-making
- ⚡ **FastAPI REST API**: High-performance API for real-time control and monitoring
- 📈 **Technical Analysis**: Built-in indicators (RSI, MACD, Bollinger Bands, etc.)
- 🎯 **Strategy Framework**: Flexible base classes for implementing custom strategies
- 🔐 **Risk Management**: Configurable position sizing, stop-loss, and drawdown limits

## Tech Stack

- **Python** 3.8+
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation and analysis
- **TensorFlow** - Machine learning and neural networks
- **CCXT** - Cryptocurrency exchange integration
- **FastAPI** - Modern web framework for APIs
- **Uvicorn** - ASGI server

## Installation

### From Source

```bash
git clone https://github.com/REDDNoC/quantops-engine.git
cd quantops-engine
pip install -r requirements.txt
pip install -e .
```

### Using pip (when published)

```bash
pip install quantops-engine
```

## Quick Start

### 1. Configuration

Copy the example configuration files:

```bash
cp .env.example .env
cp config.example.json config.json
```

Edit `.env` with your exchange API keys:

```env
BINANCE_API_KEY=your_api_key
BINANCE_SECRET=your_secret
```

### 2. Basic Usage

```python
import asyncio
from quantops import TradingEngine
from quantops.strategies.momentum import MomentumStrategy
from quantops.config.settings import load_config

async def main():
    # Load configuration
    config = load_config("config.json")
    
    # Initialize engine
    engine = TradingEngine(config)
    
    # Add strategies
    strategy = MomentumStrategy({
        "name": "momentum_btc",
        "symbols": ["BTC/USDT"],
        "position_size": 0.1
    })
    engine.add_strategy(strategy)
    
    # Start trading
    await engine.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Run the API Server

```bash
python -m quantops.api.app
```

Or use uvicorn directly:

```bash
uvicorn quantops.api.app:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at: http://localhost:8000/docs

### 4. Backtesting

```python
import asyncio
import pandas as pd
from quantops.backtesting.backtester import Backtester
from quantops.strategies.momentum import MomentumStrategy

async def run_backtest():
    # Load historical data
    historical_data = {
        "BTC/USDT": pd.DataFrame({
            "timestamp": [...],
            "open": [...],
            "high": [...],
            "low": [...],
            "close": [...],
            "volume": [...]
        })
    }
    
    # Initialize backtester
    backtester = Backtester(
        initial_capital=100000.0,
        commission=0.001,
        slippage=0.0005
    )
    
    # Create strategy
    strategy = MomentumStrategy({
        "name": "momentum_test",
        "symbols": ["BTC/USDT"]
    })
    
    # Run backtest
    results = await backtester.run(strategy, historical_data)
    
    print(f"Total Return: {results['total_return_pct']:.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown_pct']:.2f}%")

asyncio.run(run_backtest())
```

## Project Structure

```
quantops-engine/
├── quantops/
│   ├── core/              # Core trading engine
│   │   └── engine.py
│   ├── exchange/          # Exchange integration (CCXT)
│   │   └── manager.py
│   ├── backtesting/       # Backtesting framework
│   │   └── backtester.py
│   ├── models/            # AI/ML models
│   │   └── agent_swarm.py
│   ├── strategies/        # Trading strategies
│   │   ├── base.py
│   │   └── momentum.py
│   ├── api/               # FastAPI REST API
│   │   └── app.py
│   ├── config/            # Configuration management
│   │   └── settings.py
│   └── utils/             # Utility functions
│       └── indicators.py
├── tests/                 # Unit and integration tests
├── examples/              # Example scripts
├── setup.py
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - API information
- `GET /status` - Engine status
- `GET /health` - Health check
- `POST /engine/start` - Start trading engine
- `POST /engine/stop` - Stop trading engine
- `GET /strategies` - List active strategies
- `POST /strategies/add` - Add new strategy
- `GET /portfolio` - Get portfolio status
- `GET /exchanges` - List connected exchanges
- `GET /market/{symbol}` - Get market data
- `POST /signals/execute` - Execute manual signal

## Creating Custom Strategies

```python
from quantops.strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    async def generate_signal(self, market_data):
        # Your strategy logic here
        symbol = "BTC/USDT"
        
        if symbol not in market_data:
            return None
        
        # Analyze market data
        ticker = market_data[symbol]["ticker"]
        price = ticker["last"]
        
        # Generate signal
        if self.should_buy(price):
            return {
                "action": "buy",
                "symbol": symbol,
                "amount": 0.1
            }
        
        return None
    
    def should_buy(self, price):
        # Your logic here
        return price < 50000
```

## AI Agent Swarm

The agent swarm uses multiple AI agents to collectively evaluate trading signals:

```python
from quantops.models.agent_swarm import AgentSwarm, Agent

# Create custom agent
agent = Agent(
    name="custom_agent",
    agent_type="neural",
    config={"weight": 1.0, "input_dim": 10}
)

# Initialize swarm
swarm = AgentSwarm({
    "consensus_threshold": 0.7,
    "agents": []
})

# Add agent
swarm.add_agent(agent)

# Process signals through swarm
approved_signals = await swarm.process_signals(signals, market_data)
```

## Risk Management

Configure risk parameters in `config.json`:

```json
{
  "risk_management": {
    "max_position_size": 0.1,
    "max_drawdown": 0.2,
    "stop_loss": 0.05
  }
}
```

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=quantops tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**IMPORTANT**: This software is for educational and research purposes only. Trading cryptocurrencies carries substantial risk of loss. Use at your own risk. The authors and contributors are not responsible for any financial losses incurred through the use of this software.

## Tags

`quant` `liquidity` `trading` `backtesting` `ccxt` `ai-trading` `cryptocurrency` `algorithmic-trading` `market-making` `quantitative-finance`

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- CCXT for exchange integration
- TensorFlow team for ML framework
- FastAPI for the web framework
- The open-source community
