import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot


def plotly_treemap():
    df = px.data.tips()
    fig = px.treemap(df, path=[px.Constant("all"), 'day', 'time', 'sex'], values='total_bill')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    return fig