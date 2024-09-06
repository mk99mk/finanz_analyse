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


def load_tickers(symbols: list[str]) -> dict[str, pd.DataFrame]:
    global session
    tickers = yf.Tickers(symbols, session=session)
    print(tickers.tickers)
    securities = {}
    for symbol, ticker in tickers.tickers.items():
        history = ticker.history(period="5y", interval="3mo", repair=True)
        history2 = ticker.history(period="1d", repair=True)
        securities[symbol] = pd.concat([history, history2])
    return securities


def main():
    secs = load_tickers(["AAPL", "EXW1.DE"])
    print('secs ', secs)
