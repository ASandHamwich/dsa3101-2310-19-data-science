import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/module/<uni_code>/<mod_code>')

def fetch_data(uni_code, mod_code):
    mod_code = mod_code.upper() #to ensure all uppercase
    url = f"http://localhost:5001/{uni_code}/{mod_code}"
    return eval(str(requests.get(url).text))

def page_layout(uni_code, mod_code):
    data_dict = fetch_data(uni_code, mod_code)
    #Note: All unis have different keys.
    if(uni_code.startswith("nus")):
        header = "[NUS] " + data_dict["NUS Module Code"]
        title = data_dict["NUS Module Title"]
        desc = data_dict["NUS Module Description"]
    
    if(uni_code.startswith("ntu")):
        header = "[NTU] " + data_dict["Course Code"]
        title = data_dict["Course Name"]
        desc = data_dict["Course Description"]
    
    if(uni_code.startswith("smu")):
        header = "[SMU] " + data_dict["Module Code"]
        title = data_dict["Module Name"]
        desc = data_dict["Module Description"]

    
    page = html.Div(
        children = [
            html.Div(
                className = 'modInfo',
                children = [
                    html.H1(header, className = 'modInfo--header'),
                    html.H2(title, className = 'modInfo--title'),
                    html.P(desc, className = 'modInfo--desc')
                ]
            ),
            html.Div("INTENDED FEATURE: BUILD RELATED MODS BAR") # i havent bothered to do the border for this yet
        ],
        className = "module"
    )
    return page

def layout(uni_code, mod_code):
    return html.Div(
        children = [
            page_layout(uni_code, mod_code)
        ],
    className = 'module'
    )
