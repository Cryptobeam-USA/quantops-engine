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

## AI / Codex Guidance

You are the engineering copilot for the **QuantOps-Engine** repo.

- Stack: **Node.js + Fastify** microservice.
- Role: orchestrates quant workflows (strategy metadata, backtests, risk checks, execution hooks), **not** a full monolithic trading engine.
- Keep endpoints small and clear: e.g. `/health`, `/plan`, `/strategies`, `/backtests`, `/runs`.
- Put business logic into services/modules, not directly in route handlers.
- **Do NOT** implement KYC/AML, UI, or compliance flows here.

Integration guidelines:
- Treat execution and market connectivity as **adapters** (e.g. CCXT, matching engine, message bus) in separate modules/services.
- No secrets in code: use environment variables or vault/KMS placeholders.

Style:
- Prefer small, focused changes with explicit filenames/paths.
- Keep this repo focused on quant orchestration and API surface, not “do everything” trading logic.
