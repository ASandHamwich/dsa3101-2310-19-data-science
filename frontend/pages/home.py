import dash
from dash import Dash, html, dcc, callback, Output, Input, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from datetime import datetime

import dash_bootstrap_components as dbc

dash.register_page(__name__, path = '/home')

search_bar = html.Div(
    children = [
        dcc.Location(id = 'search_nav'),
        dcc.Input(
            id = 'search', 
            type = 'text',
            placeholder = 'Search Universities, Modules here...', 
            size = '70', 
            style = {'margin': '50px auto', 'height': '30px', 'font-size': '20px'},
        ),
    ],
    style = {'display': 'flex', 'justifyContent': 'center'}
)

def buttonFormat(name, id):
    return html.Div(
        children = [
            html.Button(name, id = id, className = 'course--link'),
            dbc.Checkbox(id = f'checkbox_{id}', className = 'course--add')
        ],
        className = 'course--rect'
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
                buttonFormat('NUS: Data Science and Analytics', 'nus-dsa'),
                buttonFormat('NUS: Data Science and Economics', 'nus-dse'),
                buttonFormat('NTU: Data Science and Artificial Intelligence', 'ntu-dsa'),
                buttonFormat('SMU: Data Science and Analytics (2nd Major)', 'smu-dsa')
            ],
            className = 'course'
        ),

        html.Div(
            html.Button('Compare', id = 'comp'),
            style = {'display':'flex', 'margin': '25px', 'justifyContent': 'center'}
        )
    ],
    style = {'background-color':'white'}
)


@callback(
    Output('url', 'pathname'), [
        Input('nus-dsa', 'n_clicks'),
        Input('nus-dse', 'n_clicks'),
        Input('ntu-dsa', 'n_clicks'),
        Input('smu-dsa', 'n_clicks'),
        Input('comp', 'n_clicks'),
        Input('checkbox_nus-dsa', 'value'),
        Input('checkbox_nus-dse', 'value'),
        Input('checkbox_ntu-dsa', 'value'),
        Input('checkbox_smu-dsa', 'value')
    ]
)

def buttonPress(nus1_clicks, nus2_clicks, ntu1_clicks, smu1_clicks, comp, checkbox_nus1, checkbox_nus2, checkbox_ntu1, checkbox_smu1):
    if nus1_clicks is not None:
        return '/course/nus-dsa'
    if nus2_clicks is not None:
        return '/course/nus-dse'
    if ntu1_clicks is not None:
        return '/course/ntu-dsa'
    if smu1_clicks is not None:
        return '/course/smu-dsa'

    #Checkbox
    if comp is not None:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'comp' in changed_id:

            checkbox = []
            cb_dict = {'nus1':checkbox_nus1, 'nus2':checkbox_nus2, 'ntu1':checkbox_ntu1, 'smu1':checkbox_smu1}
            for key in cb_dict:
                if  cb_dict[key] == None:
                    continue
                else:
                    checkbox.append(key)
            
            if len(checkbox) == 2:
                return f'/compare/course1={checkbox[0]}&course2={checkbox[1]}'

    else:
        return None


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
