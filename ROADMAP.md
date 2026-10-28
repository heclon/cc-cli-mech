# Roadmap

Planned work, roughly in order. Checked items are done and verified by a test or command.

## 1. Historical data (`mech.data`)
- [ ] Download with metadata: per-file manifest (provider, requested and actual date range, row count, sha256, UTC download time)
- [ ] `end` date and range slicing; `history()` verifies the cache hash and fails loudly if the file was modified
- [ ] Adopt an existing cache that has no manifest without downloading again
- [ ] Data-quality checks: duplicate or unordered dates (reject), inconsistent OHLC and long gaps (warn)
- [ ] Command line: `python -m mech.data download SYMBOL... --start --end` and `status`
- [ ] Tests that run offline
- [ ] Alpaca market-data provider and intraday bars

## 2. Backtest engine
- [ ] Move the daily long-only engine here (next-open execution, slippage, in-sample / out-of-sample split)
- [ ] Indicators (SMA, EMA, RSI, ATR, rolling VWAP) with tests
- [ ] Metrics: return, Sharpe, max drawdown, win rate, profit factor

## 3. Backtest history
- [ ] Every run is stored with start and end time (UTC), parameters, data manifest and results
- [ ] Command line flags: `--from --to --symbols --param key=value --tag`; sweeps never overwrite the published run
- [ ] `runs`, `runs show`, `runs compare`

## 4. Research tools
- [ ] Parameter sweeps and walk-forward validation
- [ ] Multi-symbol evaluation
