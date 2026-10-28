# mech

A small Python toolkit for mechanical (rules-based) trading research on daily bars: download and cache
historical data, then backtest a strategy on it. I use it for my own swing-trading experiments
(for example an RSI + EMA + VWAP mean-reversion rule on QQQ), and I am extracting it from a private
setup so others can reuse it.

**Status: early.** Today the repository contains the historical-data module only. The backtest engine
is being moved here next.

## What works today

`mech.data` downloads daily bars from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance)
(adjusted for splits and dividends) and caches them as JSON so that repeated backtests use identical data.

```python
from mech.data import history, recent

bars = history("QQQ", start="2010-01-01")   # downloads once, then reads ~/.cache/mech/QQQ_1d.json
live = recent("QQQ")                        # always from the network; drops today's bar before 16:15 ET
```

Each bar is a dict: `date, open, high, low, close, volume`.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Requires Python 3.10+. The cache folder can be changed with `MECH_CACHE_DIR` (see `.env.example`).

## Built with

Python standard library plus `yfinance`.

## Limitations

- Daily timeframe and Yahoo Finance only for now.
- The cache has no metadata, no expiry and no data-quality checks yet (first on the to-do list).
- No tests yet.

## Planned

- Data: per-file manifest with checksum, range slicing, data-quality checks, a `download`/`status` command line, offline tests
- Backtest engine (daily, long-only, in-sample/out-of-sample) and indicators
- A stored history of every backtest run (start/end time, parameters, data used, results)

## License

MIT, see [LICENSE](LICENSE).
