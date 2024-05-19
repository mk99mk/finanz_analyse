import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time

def make_daily_bar_chart(history):
    history['date_name'] = history['date']

    history['date_name'] = history['date_name'].map(
        lambda v: time.strftime("%d.%m.%Y", time.localtime(v)))

    fig = px.line(history, x='date_name', y='sum')

    fig.update_xaxes(
        tickangle=45,
        tickmode = 'array',
        tickvals = history['date_name'][0::40],
    )
                 

    
    return fig