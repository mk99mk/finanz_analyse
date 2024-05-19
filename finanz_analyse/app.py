import panel as pn
from pathlib import Path
import datetime
import pandas as pd
import copy

from finanz_analyse.load import checking
from finanz_analyse.ui import chart_generation


def main():
    pn.extension()
    pn.extension('bokeh')


    tabs = chart_generation.checking_tab('c24')

    template = pn.template.FastListTemplate(
        title="Personal Finance Dashboard",
        sidebar=[
            pn.pane.Markdown("# Income Expense analysis"),
            pn.pane.Markdown(
                "Overview of income and expense based on my bank transactions. Categories are obtained using local LLMs."
            ),
        ],
        main=[tabs],
    )

    template.show()
