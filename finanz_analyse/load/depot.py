import pandas as pd
from finanz_analyse.config import DATA
import datetime
from dataclasses import dataclass


@dataclass
class Transaction:
    date: datetime.date
    symbol: str
    amount: float
    quote: float

def load_depots() -> dict[str, pd.DataFrame]:
    depots = {}
    for depot_file in (DATA / "depots").glob('*.pkl'):
        depot = pd.read_pickle(depot_file)
        depots[depot_file.stem] = depot

    return depots
