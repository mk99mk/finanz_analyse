import panel as pn
from pathlib import Path
import datetime
import pandas as pd
import copy
import functools

from finanz_analyse.load import checking
from finanz_analyse.ui import chart_generation


def main():
    pn.extension()
    pn.extension('bokeh')

    accounts = ['c24', 'c24_spari', 'volksbank']

    pages = [chart_generation.checking_tab(name) for name in accounts]

    main_content = pn.Row()
    def switch_page(page, event):
        main_content.clear()
        main_content.append(page)

    page_buttons = [pn.widgets.Button(name=f'Checking account - {name}', button_type='primary') for name in accounts]
    for page, page_button in zip(pages, page_buttons):
        page_button.on_click(functools.partial(switch_page, page))

    dashboard = pn.Row(pn.Column(*page_buttons), pn.Spacer(width=50), main_content)

    main_content.append(pages[0])

    dashboard.show()
