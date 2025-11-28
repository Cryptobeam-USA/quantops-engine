# QuantOps Engine

Backtesting, live trading hooks, and risk controls.

Stack: Node.js + Fastify (Node 20).

## Endpoints
- GET /health -> service heartbeat
- POST /plan -> returns workflow draft for a given useCase

## Quick start
- npm install
- npm run dev
- curl http://localhost:3000/health

## Layout
- src/index.js: Fastify server + health + planWorkflow
- .env.example: PORT/LOG_LEVEL/ENDPOINT placeholders
- .github/workflows/ci.yml: lint/test/build
