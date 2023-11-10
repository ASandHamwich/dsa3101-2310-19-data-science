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
                html.H1(children = 'DataCompass', className = "header--title")
            ], 
            href = '/home'
        )
    ]
)


app.layout = html.Div(
    [
        header,
        dash.page_container
    ]
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
