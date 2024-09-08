import plotly.express as px
import pandas as pd
from dataclasses import dataclass
from finanz_analyse import cache
from finanz_analyse.load.depot import load_depots
from finanz_analyse.data_loader.finance_yahoo_adapter import load_tickers

from .shared import LAYOUT

@dataclass
class Ratio:
    symbol: str
    kind: str
    value: float

@dataclass
class Holding:
    symbol: str
    kind: str
    value: float
    amount: float
    value: float

def generate(holdings: dict[str, Holding]) -> str:
    df = pd.DataFrame(holdings.values())
    fig = px.sunburst(df, path=['symbol'], values='value')
    fig.update_layout(LAYOUT)
    return fig.to_html()

def sunburst(name: str) -> str:

    figures = []
    if name not in cache.DEPOTS:
        return f"Unknown depot {name}"

    transactions = cache.DEPOTS[name]
    holdings: dict[str, Holding] = {}
    for index, transaction in transactions.iterrows():
        symbol = transaction['symbol']
        amount = transaction['amount']
        if symbol in holdings:
            holdings[symbol].amount += amount
        else:
            holdings[symbol] = Holding(symbol=symbol, kind="", amount=amount, value=0)
    for holding in holdings.values():
        quote = cache.SECURITIES[holding.symbol]['Close'].iloc[-1]
        holding.value = round(holding.amount * quote, 2)
    return generate(holdings)
