import panel
from pathlib import Path
from finanz_analyse.load import checking


def main():
    # template = panel.template.FastListTemplate(
    #     title="Personal Finance Dashboard",
    #     sidebar=[
    #         panel.pane.Markdown("# Income Expense analysis"),
    #         panel.pane.Markdown(
    #             "Overview of income and expense based on my bank transactions. Categories are obtained using local LLMs."
    #         ),
    #     ],
    #     # main=[
    #     #     panel.Row(panel.Column(panel.Row(tabs))),
    #     # ],
    #     main=[],
    # )

    # template.show()
    checking.load('c24', '/home/michel/Dokumente/finanzen/c24/2023_12_17.csv')

