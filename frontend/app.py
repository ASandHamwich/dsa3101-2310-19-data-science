import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

#Top header 
header = html.Div(
    className = 'header',
    children = [
        dcc.Link(
            id = "header",
            children = [
                html.Img(src = '/assets/logo.png', className = "logo")
            ], 
            href = '/home'
        )
    ]
)


search_bar = html.Div(
    children = [
        dcc.Location(id = 'search_nav'),
        dcc.Input(
            id = 'search', 
            type = 'text',
            placeholder = 'Search Concepts, Modules here...', 
            size = '70', 
            style = {'margin': '50px auto', 'height': '30px', 'font-size': '20px'},
        ),
    ],
    style = {'display': 'flex', 'justifyContent': 'center'}
)


app.layout = html.Div(
    [
        header,
        search_bar,
        dash.page_container
    ]
)


@callback(
    Output("search_nav", "pathname"),
    [
        Input("search", "value"), 
        Input("search", "n_submit")
    ],
    prevent_initial_call = True
)

def searchFunction(query, submit):
    if submit == 1:
        return f'/search={query}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
