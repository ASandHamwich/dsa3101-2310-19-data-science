import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

dash.register_page(__name__, path = '/home')

search_bar = html.Div(
    children = [
        dcc.Input(
            id = 'search', 
            type = 'text',
            placeholder = 'Search Universities, Modules here...', 
            size = '70', 
            style = {'margin': '50px auto', 'height': '30px', 'font-size': '20px'}
        ),
    ],
    style = {'display': 'flex', 'justifyContent': 'center'}
)

layout = html.Div(
    children = [
        search_bar,
        
        html.Div(
            children= html.P('Course credit conversion for the universities: 4MC (NUS) = 3AU (NTU) = 2CU(SMU)', className = 'info--text'), 
            className = 'info'   
        ),

        html.Div(
            children = [
                dcc.Location(id = 'url'),
                html.Button('NUS: Data Science and Analytics', id = 'nus1'),
                html.Button('NUS: Data Science and Economics', id = 'nus2'),
                html.Button('NTU: Data Science and Artifical Intelligence', id = 'ntu1'),
                html.Button('SMU: Data Science and Analytics (2nd Major)', id = 'smu1'),

            ],
            style = {'display':'flex', 'margin': '25px', 'justifyContent': 'center'}

        ),
        html.Div(
            html.Button('Compare', id = 'comp'),
            style = {'display':'flex', 'margin': '25px', 'justifyContent': 'center'}
        )
    ],
    style = {'background-color':'white'}
)


@callback(
    Output('url', 'pathname'),
    [Input('nus1', 'n_clicks'),
        Input('nus2', 'n_clicks'),
        Input('ntu1', 'n_clicks'),
        Input('smu1', 'n_clicks'),
        Input('comp', 'n_clicks')
    ]
)


def buttonPress(nus1_clicks, nus2_clicks, ntu1_clicks, smu1_clicks, comp_clicks):
    if nus1_clicks is not None:
        return '/course/nus1'
    if nus2_clicks is not None:
        return '/course/nus2'
    if ntu1_clicks is not None:
        return '/course/ntu1'
    if smu1_clicks is not None:
        return '/course/smu1'
    if comp_clicks is not None:
        return '/compare'
    else:
        return None
