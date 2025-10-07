"""FastAPI REST API for the trading engine."""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uvicorn

from quantops.core.engine import TradingEngine
from quantops.config.settings import load_config

logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="QuantOps Engine API",
    description="Algorithmic Liquidity & Quantitative Strategy Engine API",
    version="0.1.0"
)

# Global engine instance
engine: Optional[TradingEngine] = None


# Pydantic models for request/response
class EngineConfig(BaseModel):
    """Engine configuration model."""
    initial_capital: float = Field(default=100000.0, description="Initial trading capital")
    cycle_interval: float = Field(default=1.0, description="Trading cycle interval in seconds")
    symbols: List[str] = Field(default=[], description="Trading symbols")
    exchanges: Dict[str, Dict[str, Any]] = Field(default={}, description="Exchange configurations")


class StrategyConfig(BaseModel):
    """Strategy configuration model."""
    name: str = Field(..., description="Strategy name")
    type: str = Field(..., description="Strategy type")
    config: Dict[str, Any] = Field(default={}, description="Strategy configuration")


class SignalRequest(BaseModel):
    """Manual signal request model."""
    action: str = Field(..., description="Action: buy or sell")
    symbol: str = Field(..., description="Trading symbol")
    amount: float = Field(..., description="Amount to trade")
    price: Optional[float] = Field(None, description="Optional limit price")


class StatusResponse(BaseModel):
    """Engine status response model."""
    running: bool
    strategies: int
    portfolio_value: float
    positions: Dict[str, Any]
    timestamp: str


@app.on_event("startup")
async def startup_event():
    """Initialize engine on startup."""
    global engine
    try:
        config = load_config()
        engine = TradingEngine(config)
        logger.info("Trading engine initialized")
    except Exception as e:
        logger.error(f"Failed to initialize engine: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    global engine
    if engine and engine.running:
        await engine.stop()
        logger.info("Trading engine stopped")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "QuantOps Engine API",
        "version": "0.1.0",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get engine status."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    return engine.get_status()


@app.post("/engine/start")
async def start_engine(background_tasks: BackgroundTasks):
    """Start the trading engine."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    if engine.running:
        raise HTTPException(status_code=400, detail="Engine already running")
    
    background_tasks.add_task(engine.start)
    
    return {"message": "Engine started", "timestamp": datetime.utcnow().isoformat()}


@app.post("/engine/stop")
async def stop_engine():
    """Stop the trading engine."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    if not engine.running:
        raise HTTPException(status_code=400, detail="Engine not running")
    
    await engine.stop()
    
    return {"message": "Engine stopped", "timestamp": datetime.utcnow().isoformat()}


@app.post("/strategies/add")
async def add_strategy(strategy_config: StrategyConfig):
    """Add a strategy to the engine."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    # This is a placeholder - in production you'd load strategy from config
    return {
        "message": f"Strategy '{strategy_config.name}' added",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/strategies")
async def list_strategies():
    """List active strategies."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    return {
        "strategies": [
            {"name": s.__class__.__name__, "symbols": s.symbols}
            for s in engine.strategies
        ],
        "count": len(engine.strategies)
    }


@app.post("/signals/execute")
async def execute_signal(signal: SignalRequest):
    """Execute a manual trading signal."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    signal_dict = {
        "action": signal.action,
        "symbol": signal.symbol,
        "amount": signal.amount,
    }
    
    if signal.price:
        signal_dict["price"] = signal.price
    
    await engine._execute_signal(signal_dict)
    
    return {
        "message": "Signal executed",
        "signal": signal_dict,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/portfolio")
async def get_portfolio():
    """Get current portfolio information."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    return {
        "value": engine.portfolio_value,
        "positions": engine.positions,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/exchanges")
async def get_exchanges():
    """Get connected exchanges."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    return {
        "exchanges": list(engine.exchange_manager.exchanges.keys()),
        "default": engine.exchange_manager.default_exchange,
        "count": len(engine.exchange_manager.exchanges)
    }


@app.get("/market/{symbol}")
async def get_market_data(symbol: str, exchange: Optional[str] = None):
    """Get market data for a symbol."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        ticker = await engine.exchange_manager.fetch_ticker(symbol, exchange)
        orderbook = await engine.exchange_manager.fetch_order_book(symbol, exchange_name=exchange)
        
        return {
            "symbol": symbol,
            "ticker": ticker,
            "orderbook": {
                "bids": orderbook.get("bids", [])[:10],
                "asks": orderbook.get("asks", [])[:10]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "engine_initialized": engine is not None,
        "engine_running": engine.running if engine else False,
        "timestamp": datetime.utcnow().isoformat()
    }


def run_api(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Run the FastAPI application.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        reload: Enable auto-reload for development
    """
    uvicorn.run("quantops.api.app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_api(reload=True)
