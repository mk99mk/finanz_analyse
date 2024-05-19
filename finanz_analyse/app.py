import panel
from pathlib import Path
import datetime

from finanz_analyse.load import checking
from finanz_analyse.ui import chart_generation


def main():
    loaded = checking.load('c24')
    c24_sum = checking.sum(history=loaded, start=datetime.date(2023,7,1))

    tabs = panel.Tabs(
        ('c24', chart_generation.make_daily_bar_chart(c24_sum)),
        ('c24 spari', chart_generation.make_daily_bar_chart(c24_sum))
    )

    template = panel.template.FastListTemplate(
        title="Personal Finance Dashboard",
        sidebar=[
            panel.pane.Markdown("# Income Expense analysis"),
            panel.pane.Markdown(
                "Overview of income and expense based on my bank transactions. Categories are obtained using local LLMs."
            ),
        ],
        main=[tabs],
    )

    template.show()
