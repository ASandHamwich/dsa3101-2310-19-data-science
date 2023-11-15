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

def fetch_all():
    url = 'http://localhost:5001/nus-ntu-smu/all-modules/'


def sidebar(concepts):
    if not concepts:
        return None
    else:
        return html.Div("No Related Mods", className = 'mod_sidebar')

def page_layout(uni_code, mod_code):
    data_dict = fetch_data(uni_code, mod_code)
    #Note: All unis have different keys.

    if(uni_code.startswith("nus")):
        header = "[NUS] " + data_dict["module_code"]
    
    if(uni_code.startswith("ntu")):
        header = "[NTU] " + data_dict["module_code"]

    if(uni_code.startswith("smu")):
        header = "[SMU] " + data_dict["module_code"]

    title = data_dict["module_name"]
    desc = data_dict["module_description"]

    concepts = data_dict["key_concepts"]
    
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
            sidebar(concepts)
        ],
        className = "module"
    )
    return page

def layout(uni_code, mod_code):
    return html.Div(
        children = [
            page_layout(uni_code, mod_code),
            dbc.Input(type = 'text', placeholder = "Leave your review here...", className = 'modreview')
        ],
        style = {'padding-left': '45px', 'padding-right': '45px'}
    )
