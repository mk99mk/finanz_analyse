import plotly.graph_objects as go
import plotly.express as px
import datetime
import numpy as np
import time
from finanz_analyse.load import checking
import panel as pn
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.models import tools
from bokeh.models import Range1d


def create_balance_plot(df: pd.DataFrame):
    source = ColumnDataSource(df)
    p = figure(title="Account Balance Over Time", x_axis_label='Date', y_axis_label='Balance',
               x_axis_type='datetime', width=1000, height=400, tools="")
    p.line(x='date', y='balance', source=source, line_width=2, color='blue', legend_label='Balance')
    p.scatter(x='date', y='balance', source=source, size=5, color='blue')

    wheel_zoom = tools.WheelZoomTool()
    wheel_zoom.dimensions = 'height'
    pan_tool = tools.PanTool()
    pan_tool.dimensions = 'height'
    hover = HoverTool()
    hover.tooltips = [("Date", "@date{%F}"), ("Balance", "@balance{0.2f}")]
    hover.formatters = {'@date': 'datetime'}
    p.add_tools(wheel_zoom, pan_tool, hover)

    p.legend.location = "top_left"
    return p

def checking_tab(name: str):
    loaded = checking.load(name)

    loaded = loaded.sort_values(by='date', ascending=True)
    loaded['balance'] = loaded['amount'].cumsum()

    def filter_transactions(start_date, end_date):
        filtered_df = loaded[(loaded['date'] >= start_date) & (loaded['date'] <= end_date)]
        return filtered_df

    start_date_picker = pn.widgets.DatePicker(name='Start Date', value=datetime.date(2024, 1, 1))
    end_date_picker = pn.widgets.DatePicker(name='End Date', value=datetime.date(2024, 12, 31))

    transactions_table = pn.widgets.DataFrame(loaded, show_index=False, sizing_mode='stretch_width')

    balance_plot = create_balance_plot(loaded)

    def update_plot(event):
        start_date = start_date_picker.value
        end_date = end_date_picker.value
        filtered_df = filter_transactions(start_date, end_date)
        balance_plot.renderers = []  # Clear existing renderers
        new_plot = create_balance_plot(filtered_df)
        balance_plot.renderers.extend(new_plot.renderers)  

    def update_table(event):
        start_date = start_date_picker.value
        end_date = end_date_picker.value
        filtered_df = filter_transactions(start_date, end_date)
        transactions_table.value = filtered_df

    start_date_picker.param.watch(update_table, 'value')
    end_date_picker.param.watch(update_table, 'value')
    start_date_picker.param.watch(update_plot, 'value')
    end_date_picker.param.watch(update_plot, 'value')

    return pn.Tabs(
        (name, pn.Column(
            pn.pane.Markdown("## Checking Account Transactions", sizing_mode='stretch_width'),
            pn.Row(start_date_picker, end_date_picker, sizing_mode='stretch_width'),
            transactions_table,
            width=1000
        )),
        (f"{name} - balance", pn.Column(
            pn.pane.Markdown("## Checking Account Balance", sizing_mode='stretch_width'),
            pn.Row(start_date_picker, end_date_picker, sizing_mode='stretch_width'),
            balance_plot,
            width=1000
        ))
    )
