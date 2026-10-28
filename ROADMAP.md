# Roadmap

Longer-term features for `mech`. [PLAN.md](PLAN.md) holds the near-term tasks with their status: the historical-data module, the backtest engine, run history and the command line. This file is for what comes after those, in rough order. Nothing here is promised for a date, and the order changes when something turns out to matter more.

Each item is marked **Next** (starts once the modules in PLAN.md are verified), **Later** or **Exploring** (an idea I have not validated).

## Next

### A database for historical data
Bars live today in one JSON file per symbol. Refreshing rewrites the whole file, nothing can be queried across symbols, and there is no incremental update. The plan is a local database (SQLite first, DuckDB or Parquet if scans over many symbols get slow) with bars, manifests and quality warnings in tables. Downloads become incremental: only the missing days are fetched, and running the same download twice is harmless. The JSON files stay as an export format.

### Parallel backtests for N strategies
Running 200 parameter sets or 20 strategies one after another wastes most of the machine. The engine is CPU-bound pure Python, so threads would be held back by the GIL. The plan is a process pool (`concurrent.futures`) where bars are loaded once per worker and every worker only reads them. Results must not depend on the number of workers, and there will be a test for that. Workers return results to a single writer so SQLite never fights itself, and a run can report progress and be cancelled.

### FastAPI service
A small local service over the same core the command line uses: list and download data, start a backtest as a background job, poll its status, list runs and compare two of them. Request and response models are Pydantic models shared with the command line, so the OpenAPI schema comes for free. It binds to localhost by default.

### FastMCP server
The same operations exposed as MCP tools, so an AI assistant can download data, run a backtest and read results without screen-scraping a CLI. Read-only tools first. Tools that start runs have limits (maximum date range, maximum concurrent runs) and write to the run history like any other run. The service layer is shared with FastAPI so the logic exists once.

## Later

### Agent-driven backtests and optimization
An LLM agent proposes a hypothesis and a set of parameters, runs the backtest through the MCP tools, reads the result and tries again. Because an agent can try hundreds of variants, the harness has to protect against fooling itself:
- the in-sample and out-of-sample split is fixed before the loop starts, and the agent never sees out-of-sample numbers until its final answer
- a budget caps the number of runs and the spend
- every run is stored with the agent's stated hypothesis, the model name and the seed, so the whole session can be replayed
- the number of trials is recorded and reported next to the final result, since the more variants tried the less one good Sharpe ratio means

### Search and validation methods
Grid and random search, Bayesian optimization (probably Optuna, added only when this lands), anchored and rolling walk-forward, parameter robustness maps, and Monte Carlo over the order of trades to see how bad a drawdown could have been.

### A richer engine
Commission and spread models, position sizing rules, shorts, several positions at once with a shared cash limit, take-profit and trailing stops, and a proper exchange calendar. Intraday bars and the Alpaca data provider (PLAN item DH-09) belong here too.

### More data providers
A provider interface so Yahoo Finance is one implementation among several. Alpaca first, then whichever free source covers the symbols I actually test.

### Strategy plugins and examples
A documented interface for a strategy (`warmup`, `prepare`, `signal`), loading a strategy from a path, and three worked examples: RSI mean reversion, a moving-average cross and a breakout.

### Reports
A Markdown or HTML report per run with the equity curve, drawdowns and the trade table, and a side-by-side report for two runs.

## Project health (alongside everything above)
GitHub Actions running the tests on Python 3.10 to 3.13, ruff, type checking, a coverage number, a changelog with semantic versions, a Docker image for the service, and a small benchmark that fails when the engine gets noticeably slower.

## Exploring
- Vectorized indicators with NumPy where the pure-Python version is too slow, kept optional so the core stays dependency-light.
- A web page for browsing run history, on top of the FastAPI service.

## Out of scope
`mech` does not place orders. Anything that talks to a broker for live or paper trading would be a separate project that uses `mech` as a library.
