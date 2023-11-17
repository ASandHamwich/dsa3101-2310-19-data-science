import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

from fetchFunction import *
from moduleFunction import *

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/modcompare/<uni1>&<mod1>/<uni2>&<mod2>')

def link_gen(uni_code, mod_code):
        return html.A(
        children = [html.H5("See More Here")], 
        href = f"http://localhost:9001/module/{uni_code}/{mod_code}",
        className = 'modInfo--desc'
    )

def half_page_layout(uni_code, mod_code):
    data_dict = fetch_data(uni_code, mod_code)

    if(uni_code.startswith("nus")):
        header = "[NUS] " + data_dict["module_code"]
    
    if(uni_code.startswith("ntu")):
        header = "[NTU] " + data_dict["module_code"]

    if(uni_code.startswith("smu")):
        header = "[SMU] " + data_dict["module_code"]

    title = data_dict["module_name"]
    desc = data_dict["module_description"]

    page = html.Div(
        children = [
            html.Div(
                className = 'modInfo',
                children = [
                    html.H1(header, className = 'modInfo--header'),
                    html.H2(title, className = 'modInfo--title'),
                    html.P(desc, className = 'modInfo--desc'),
                    html.Div(conceptsBar(uni_code, mod_code), className = 'conceptBar'),
                    link_gen(uni_code, mod_code)
                ]
            )
        ]
    )
    return page

def layout(uni1, mod1, uni2, mod2):

    left = half_page_layout(uni1, mod1)
    right = half_page_layout(uni2, mod2)

    return html.Div(
        children = [
            html.Div(children = left, className = 'compare--child'),
            html.Div(children = right, className = 'compare--child')
        ],
        className = 'compare'
    )
