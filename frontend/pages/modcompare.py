import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/modcompare/<uni1>&<mod1>/<uni2>&<mod2>')

#Layout for each individual course information page.

def fetch_data(uni_code, mod_code):
    mod_code = mod_code.upper() #to ensure all uppercase
    url = f"http://backend-1:5001/{uni_code}/{mod_code}"
    return eval(str(requests.get(url).text))

def endindex(uni_code, mod_code):
    data_dict = fetch_data(uni_code, mod_code)
    desc = data_dict["module_description"]
    count = 0
    index = -1
    for i, char in enumerate(desc):
        if char == '.':
            count += 1
            if count == 3:
                index = i
                break
    return index

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

    concepts = data_dict["key_concepts"].upper()
    concepts = concepts.replace(",", " | ")

    link = html.A(
        children = [html.H5("See More Here")], 
        href = f"http://backend-1:5001/module/{uni_code}/{mod_code}",
        className = 'modInfo--desc'
    )
    
    page = html.Div(
        children = [
            html.Div(
                className = 'modInfo',
                children = [
                    html.H1(header, className = 'modInfo--header'),
                    html.H2(title, className = 'modInfo--title'),
                    html.P(desc[:endindex(uni_code, mod_code)+1], className = 'modInfo--desc'),
                    html.Details([
                        html.Summary("Read More"),
                        html.P(desc[endindex(uni_code, mod_code)+1:], className = 'modInfo--desc')
                    ]),
                    html.H3("Key Concepts:", className = 'bartitle'),
                    html.H4(concepts, className = 'conceptBar'),
                    link
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
