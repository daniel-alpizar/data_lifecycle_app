import pandas as pd


# Dataframe column types
cols_integers = ['transaction_id','customer_id','order','product_id','quantity']
cols_floats = ['line_item_amount', 'unit_price']
cols_dates = ['transaction_date','transaction_time']

# Dataframe format properties
# CSS dataframe style
styles = [dict(selector="th", props=[("font-size", "80%"), ("text-align", "center"),
                               ("background-color", "#000086"), ("color", "white")]),
        dict(selector="caption", props=[("caption-side", "top"), ("color", "darkblue"),
                        ("font-size", "120%"), ('font-weight','bold'), ("text-align", "center")]),
        dict(selector="tr:hover", props=[("background-color", "%s" % "#D3D3D3")]),
        dict(selector="td:hover", props=[("background-color", "#ffffb3")])]

# Columns properties
date_props = {'min-width': '90px', 'text-align': 'center', 'font-size': '10pt'}
int_props = {'min-width': '70px', 'text-align': 'center', 'font-size': '10pt'}
float_props = {'min-width': '40px', 'text-align': 'right', 'font-size': '10pt'}

# Highlight colors
c1 = 'background-color: lightblue'
c2 = 'background-color: lightgreen'
c3 = 'background-color: lightsteelblue'


def df_format(df, title):
    '''Apply custom formatting style to dataframes'''

    if len(df) > 0:
        df = (df.style
                .hide(axis='index')
                .set_properties(subset=cols_dates, **date_props)
                .set_properties(subset=cols_integers, **int_props)
                .set_properties(subset=cols_floats, **float_props)                
                .format(precision=2)
                .set_table_styles(styles)
                .set_caption(title)
                # .set_sticky(axis='index')
                )

    else:        
        df = (df.style
                .set_table_styles(styles)
                .set_caption(title))

    return df