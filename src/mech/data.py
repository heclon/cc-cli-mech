"""Daily historical bars (yfinance, adjusted for splits and dividends) with a local JSON cache.

Backtests read from the cache so results are reproducible. `recent` always hits the network and
drops today's bar if the market has not closed yet (16:15 ET).
"""
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CACHE = Path(os.environ.get("MECH_CACHE_DIR") or Path.home() / ".cache" / "mech")
ET = ZoneInfo("America/New_York")


def _fetch(symbol, start):
    import yfinance as yf
    df = yf.Ticker(symbol).history(start=start, auto_adjust=True)
    return [dict(date=idx.strftime("%Y-%m-%d"), open=float(r.Open), high=float(r.High), low=float(r.Low),
                 close=float(r.Close), volume=float(r.Volume)) for idx, r in df.iterrows() if r.Close == r.Close]


def history(symbol, start="1993-01-01", refresh=False):
    f = CACHE / f"{symbol}_1d.json"
    if f.exists() and not refresh:
        return json.loads(f.read_text())
    bars = _fetch(symbol, start)
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(bars))
    return bars


def recent(symbol, start="2023-01-01", now=None):
    """Bars for a live runner: without today's bar if the market has not closed yet (16:15 ET)."""
    bars = _fetch(symbol, start)
    now = now or datetime.now(ET)
    if bars and bars[-1]["date"] == now.strftime("%Y-%m-%d") and (now.hour, now.minute) < (16, 15):
        bars = bars[:-1]
    return bars
