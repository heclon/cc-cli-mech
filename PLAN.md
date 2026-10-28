# Plan

Work planned for `mech`, grouped by module. This file is the only plan for the project and gets updated after every task.

**Status legend:** ⬜ not started · 🟡 written but not verified · ✅ done and verified by the test or command in the Evidence column · ⛔ blocked

**Rule:** a task is ✅ only after its check has passed. The date is the day the check passed.

**Next task:** DH-02 and DH-03 (manifest model and `download()`).

## Module: historical data (`mech.data`)  ·  0/9 verified

| ID | Task | Status | Evidence | Date |
|---|---|---|---|---|
| DH-01 | Daily bars from Yahoo Finance with a JSON cache (`history`, `recent`) | 🟡 | code exists in `src/mech/data.py`, no tests yet | |
| DH-02 | Manifest model (Pydantic): provider, requested and actual date range, row count, sha256, UTC download time | ⬜ | | |
| DH-03 | `download(symbol, start, end)` writes the bars and a sibling `.meta.json`; rejects empty, duplicated or unordered data and saves nothing | ⬜ | | |
| DH-04 | `history(symbol, start, end, refresh)` slices by date range and fails if the cached file no longer matches its sha256 | ⬜ | | |
| DH-05 | Adopt a cache that has no manifest without downloading again | ⬜ | | |
| DH-06 | Quality checks: inconsistent OHLC and long gaps become warnings stored in the manifest | ⬜ | | |
| DH-07 | Command line: `python -m mech.data download SYMBOL... --start --end` and `status` | ⬜ | | |
| DH-08 | Offline test suite (network call replaced by a fake); each rule above has a test that fails when the rule is broken | ⬜ | | |
| DH-09 | Alpaca market-data provider and intraday bars | ⬜ | | |

## Module: backtest engine (`mech.engine`, `mech.indicators`, `mech.metrics`)  ·  0/6 verified

| ID | Task | Status | Evidence | Date |
|---|---|---|---|---|
| BT-01 | Daily long-only engine: next-open execution, slippage, intraday stop, one position per symbol | ⬜ | | |
| BT-02 | Indicators: SMA, EMA, RSI, ATR, rolling VWAP, with tests | ⬜ | | |
| BT-03 | Metrics: return, Sharpe, max drawdown, win rate, profit factor, with tests | ⬜ | | |
| BT-04 | In-sample and out-of-sample split with a fixed split date, and a written report | ⬜ | | |
| BT-05 | Reproducibility test: same data (same sha256) and same config give the same metrics | ⬜ | | |
| BT-06 | Example strategy (RSI + EMA + VWAP mean reversion on QQQ) with synthetic-data tests | ⬜ | | |

## Module: run history (`mech.runs`)  ·  0/5 verified

Goal: every backtest is stored with its start and end time (UTC), parameters, the data it used and its results, so runs can be compared later.

| ID | Task | Status | Evidence | Date |
|---|---|---|---|---|
| HB-01 | SQLite schema: `runs`, `run_trades`, `run_equity` | ⬜ | | |
| HB-02 | `start_run` and `finish_run`: UTC start and end, status (running, ok, failed), parameters, config hash, data manifests | ⬜ | | |
| HB-03 | Results of each run are archived and never overwritten by the next one | ⬜ | | |
| HB-04 | A view that lists runs with duration, period, parameters and headline metrics | ⬜ | | |
| HB-05 | Tests: two runs on the same day keep both results; a failed run is recorded | ⬜ | | |

## Module: command line (`mech.cli`)  ·  0/4 verified

| ID | Task | Status | Evidence | Date |
|---|---|---|---|---|
| CL-01 | `backtest` command with `--from --to --symbols --param key=value --tag --publish`; invalid input is rejected before a run is opened | ⬜ | | |
| CL-02 | Parameter sweeps do not overwrite the published run unless `--publish` is given | ⬜ | | |
| CL-03 | `runs`, `runs show N` and `runs compare A B` | ⬜ | | |
| CL-04 | Tests with a toy strategy and a temporary database | ⬜ | | |

## Later: research tools

- Parameter sweeps with a robustness map
- Walk-forward validation
- Multi-symbol evaluation and a simple portfolio view
- Monte Carlo on trade sequences

## Conventions

- Python standard library first; each new dependency is named in the task that needs it.
- Tests run offline.
- No keys, tokens or personal paths in code, tests or docs. Secrets go in `.env`, which is ignored; `.env.example` only has placeholders.
- One commit per finished task, with a message that says what changed.
