import yfinance as yf
import pandas as pd

from pathlib import Path

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

ASSETS = Path(__file__).parent.parent / "assets"


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(2, Duration.SECOND * 5)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

hitories = {}


def load_tickers(symbols: list[str]):
    global session
    tickers = yf.Tickers(symbols, session=session)
    print(tickers.tickers)
    for symbol, ticker in tickers.tickers.items():
        history = ticker.history(start="2015-01-01", interval="1d", repair=True)
        hitories[symbol] = history


def main():
    load_tickers(["AAPL", "EXW1.DE"])
