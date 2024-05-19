import panel as pn
from pathlib import Path
import datetime
import pandas as pd
import copy

from finanz_analyse.load import checking
from finanz_analyse.ui import chart_generation


def main():
    c24_folder = Path('/home/michel/Dokumente/finanzen/c24/volksbank_tagesgeld')
    for csv_file in c24_folder.glob("*.csv"):
        print('load ', csv_file)
        loaded = checking.add('volksbank', csv_file)