import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

import dash_bootstrap_components as dbc

from fetchFunction import *

def conceptsBar(uni_code, mod_code):
    #Load the relevant data concepts
    data_dict = fetch_data(uni_code, mod_code)
    concepts = data_dict["key_concepts"].upper().split(", ")
    glossary_list = [fetch_glossary()[x.lower()] for x in concepts]

    #Create dataframe 
    data = {
        "concept": concepts,
        "val": [1 for i in range(len(concepts))],
        "x": [1 for i in range(len(concepts))]
    }
    df = pd.DataFrame(data)

    fig = px.bar(
        df, x = "x", y = 'val', 
        color = 'concept', text = 'concept', orientation="h")

    fig.update_traces(
        textfont_size = 20, textposition="inside", 
        insidetextanchor="middle", showlegend=False, width = 0.5, 
        hoverinfo = 'skip', hovertemplate = None)
    fig.update_yaxes(showgrid = False, visible = False)
    fig.update_xaxes(showgrid = False, visible = False)
    fig.update_layout(plot_bgcolor = 'rgba(0, 0, 0, 0)')
    fig.update_layout(margin = dict(l = 0.1, r = 0.1, t = 0.1, b = 0.1, pad = 0))


    return html.Div(
        [
            html.H3("Key Concepts:", className = 'bartitle'),
            dcc.Graph(figure = fig, className = 'conceptBar')
        ]
    )