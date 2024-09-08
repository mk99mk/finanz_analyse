import pandas as pd
from finanz_analyse.data_loader.finance_yahoo_adapter import load_tickers
from finanz_analyse.load.depot import load_depots

SECURITIES: dict[str, pd.DataFrame] | None = None
DEPOTS: dict[str, pd.DataFrame] | None = None

def load_all_tickers() -> None:
    global SECURITIES
    symbols = []
    for name, transactions in DEPOTS.items():
        symbols.extend(transactions['symbol'].unique().tolist())
    SECURITIES = load_tickers(symbols)

DEPOTS = load_depots()
print(DEPOTS)
load_all_tickers()