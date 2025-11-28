# QuantOps Engine

Backtesting, live trading hooks, and risk controls.

Stack: Node.js (CJS), minimal workflow runner.

## Scope
- Interfaces: HTTP/GraphQL/gRPC placeholders
- Domains: auth, telemetry, observability hooks
- Artifacts: sample workflow runner in src/index.js

## Quick start
- npm install
- npm run dev (runs src/index.js)
- npm run test (sanity)

## Layout
- src/index.js: orchestrator + health probe + planWorkflow
- .env.example: PORT/LOG_LEVEL/ENDPOINT placeholders
- .devcontainer/: Node 20
- .github/workflows/ci.yml: lint/test/build
