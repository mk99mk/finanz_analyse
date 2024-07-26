from pathlib import Path
import plotly.express as px
from plotly.graph_objs import Layout
from base64 import b64encode
import io

iris_html = Path(__file__).parent.parent / "finanz_analyse_skeleton" / "static" / "iris.html"

def main():
    df = px.data.iris() # replace with your own data source
    fig = px.scatter(
        df, x="sepal_width", y="sepal_length", 
        color="species")
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={
                "color":"black",
                "size":20
            },
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='black')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
    fig.update_layout(layout)
    # fig.show()
    with open(iris_html, "w") as open_iris_html:
        fig.write_html(open_iris_html)