import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

# Top header
header = html.Div(
    className='header',
    children=[
        dcc.Link(
            id="header",
            children=[
                html.Img(src='/assets/logo.png', className="logo")
            ],
            href='/'
        )
    ]
)

search_bar = html.Div(
    children=[
        dcc.Location(id='search_nav'),
        html.Div(
            children=[
                html.Img(src='/assets/glass_logo.png', className='magnifying-glass-icon', style={
                    'width': '40px',
                    'height': '30px',
                    'margin-right': '0px',
                    'margin-top': '0px',
                    'background-color': '#F9CA84',
                    'padding': '5px',
                    'border-top-left-radius': '15px',
                    'border-bottom-left-radius': '15px',
                    'border-top-right-radius': '0px',
                    'border-bottom-right-radius': '0px',
                }),
                dcc.Input(
                    id='search',
                    type='text',
                    placeholder='Search Concepts, Modules here...',
                    size='70',
                    style={
                        'height': '30px',
                        'font-size': '20px',
                        'border': '4px solid #F9CA84',
                        'border-radius': '15px',
                        'padding-left': '10px',
                        'border-top-left-radius': '0px',  
                        'border-bottom-left-radius': '0px',
                        'border-top-right-radius': '15px',
                        'border-bottom-right-radius': '15px', 
                    },
                ),
            ],
            style={'margin': '50px auto', 'display': 'flex', 'justifyContent': 'center'}
        ),
    ]
)

app.layout = html.Div(
    [
        header,
        search_bar,
        dash.page_container
    ]
)

@app.callback(
    Output("search_nav", "pathname"),
    [Input("search", "value"), Input("search", "n_submit")],
    prevent_initial_call=True
)
def searchFunction(query, submit):
    if submit == 1:
        return f'/search={query}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
