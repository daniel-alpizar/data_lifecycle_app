import numpy as np
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from .plotly_app import plotly_treemap
from .models import Datawarehouse


app = DjangoDash(name='dash_semana')

def dash_test():

    # App layout
    app_layout = html.Div([
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Treemap', 'value': 'TM'},
                {'label': 'Sunburst', 'value': 'SB'}
            ],
            value='TM'
        ),
        dcc.Graph(id='graph-output')
    ])
    return app_layout
app.layout = dash_test


# Callback to update the graph
@app.callback(
    Output('graph-output', 'figure'),
    Input('chart-type', 'value')
)
def update_graph(chart_type):

    orders_query = Datawarehouse.objects.all()
    df = pd.DataFrame(orders_query.values())

    if chart_type == 'TM':
        fig = px.treemap(df, 
                        path=['customer_id', 'product_id'],
                        values='line_item_amount',
                        title='Treemap of Transactions')
    else:
        fig = px.sunburst(df,
                        path=['customer_id', 'product_id'],
                        values='line_item_amount',
                        title='Sunburst of Transactions')
    return fig
