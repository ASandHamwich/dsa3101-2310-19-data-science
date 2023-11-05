
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc


app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1(children='DataCompass', style={'textAlign':'left'}),

        html.Div(
            children = [
                    dcc.Input(
                        id = 'search', 
                        type = 'text',
                        placeholder = 'Search Universities, Modules here...', 
                        size = '70', 
                        style = {'margin': '50px auto', 'height': '30px', 'font-size': '20px'}),
            ],
            style = {'display': 'flex', 'justifyContent': 'center'}
        ),
        
        html.Div(
            html.P(
                children='Course credit conversion for the universities: 4MC (NUS) = 3AU (NTU) = 2CU(SMU)', 
                style={'textAlign':'center', 'background-color':'white'}
            )
        ),
        html.Div(
            children = [
                html.Button('1'),
                html.Button('2'),
                html.Button('3'),
                html.Button('4'),
            ],
            style = {'display':'flex', 'margin': '25px', 'justifyContent': 'center'}

        ),
        html.Div(
            html.Button('Compare'),
            style = {'display':'flex', 'margin': '25px', 'justifyContent': 'center'}

        )
    ],
    style = {'background-color':'white'}
)

if __name__ == '__main__':
    app.run(debug=True)

