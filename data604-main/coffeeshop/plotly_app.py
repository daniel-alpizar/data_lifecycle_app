import pandas as pd
import plotly.express as px
from plotly.offline import plot


def plotly_treemap(df):
    fig = px.treemap(df, 
                path=['customer_id', 'product_id'], # Hierarchical data: first customer_id, then product_id
                values='line_item_amount', # Size of the rectangles represent line item amount
                title='Treemap of Transactions')

    return fig