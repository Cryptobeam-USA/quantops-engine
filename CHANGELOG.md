# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial release of QuantOps Engine
- Core trading engine with multi-strategy support
- CCXT integration for 100+ cryptocurrency exchanges
- Comprehensive backtesting framework with realistic fee modeling
- AI agent swarm for autonomous decision-making
- FastAPI REST API for real-time control
- Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR)
- Momentum-based trading strategy example
- Configuration management with environment variable support
- Unit tests for core functionality
- Example scripts for trading, backtesting, and agent swarm
- Comprehensive documentation

### Features
- **TradingEngine**: Asynchronous trading engine with strategy execution
- **ExchangeManager**: Multi-exchange connectivity and order management
- **Backtester**: Historical strategy testing with performance metrics
- **AgentSwarm**: Neural network-based agent consensus system
- **BaseStrategy**: Abstract base class for custom strategies
- **Technical Indicators**: Comprehensive technical analysis utilities
- **FastAPI Integration**: REST API with automatic OpenAPI documentation
- **Risk Management**: Configurable position sizing and stop-loss

### Dependencies
- numpy >= 1.21.0
- pandas >= 1.3.0
- tensorflow >= 2.10.0 (optional, for AI features)
- ccxt >= 3.0.0
- fastapi >= 0.100.0
- uvicorn >= 0.23.0
- pydantic >= 2.0.0
- aiohttp >= 3.8.0
- python-dotenv >= 0.19.0

[0.1.0]: https://github.com/REDDNoC/quantops-engine/releases/tag/v0.1.0
