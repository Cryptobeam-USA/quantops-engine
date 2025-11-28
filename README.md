# QuantOps Engine

Backtesting, live trading hooks, and risk controls.

## Scope
- Interfaces: HTTP/GraphQL/gRPC placeholders
- Domains: auth, telemetry, observability hooks
- Artifacts: sample workflow runner in src/index.js

## Quick start
- Decide runtime (Node/Go/Java) and replace the JS stub.
- Wire real storage + message bus clients.
- Add tests (unit + contract) and CI gates.

## Current layout
- src/index.js: sample orchestrator + health probe
- .devcontainer/: Node 20 base image for quick editing
- README.md: this file
