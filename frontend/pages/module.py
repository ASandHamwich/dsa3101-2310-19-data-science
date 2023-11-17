import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

import dash_bootstrap_components as dbc

from fetchFunction import *
from moduleFunction import *

dash.register_page(__name__, path_template = '/module/<uni_code>/<mod_code>')



def sidebar(concepts, data_dict, uni_code, mod_code):

    full_dict = fetch_all()
    concepts = data_dict["key_concepts"].split(", ")
    
    #IDEA: To use sets to give a comparison. List the top 5 mods that are overlapping; top 5 should be from other unis.

    uni_code_list = ['nus-dsa', 'nus-dse', 'ntu', 'smu']

    ranking = [] #to store results

    for uni in uni_code_list:
        if uni.startswith(uni_code[:3]):
            continue

        uni_mods = full_dict[uni]
        
        for mod in uni_mods:
            header = mod["Module Code"]
            title = mod["Module Name"]
            concepts_compare = mod["Key Concepts"].split(", ")

            check = set(concepts).intersection(concepts_compare)

            if len(check) < 2:
                continue

            if str(ranking).find(header) != -1:
                continue
            
            else:
                modinfo = (len(check),[header, title, uni])
                ranking.append(modinfo)
    
    ranking = sorted(ranking, reverse= True)
    #Pick the top 5 matches.
    final_ranking = ranking[:5]
    
    concept_children = [html.P("RELATED MODS IN OTHER COURSES")]
    for i in final_ranking:
        data = i[1]
        uni_code_2 = data[2]
        if uni_code_2.startswith("ntu") or uni_code_2.startswith("smu"):
            uni_code_2 = uni_code_2 + "-dsa"
        res = html.A(
            f"{data[2].upper()} {data[0]}", 
            href = f'/modcompare/{uni_code}&{mod_code}/{uni_code_2}&{data[0]}',
            className = "relatedmods"
        )
        concept_children.append(res)

    if len(concepts) > 1:
        return html.Div(concept_children, className = 'mod_sidebar')
    else:
        return html.Div("NO RELATED MODS FOUND", className = 'mod_sidebar')

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
            sidebar(concepts, data_dict, uni_code, mod_code)
        ],
        className = "module"
    )
    return page

def layout(uni_code, mod_code):
    return html.Div(
        children = [
            page_layout(uni_code, mod_code),
            conceptsBar(uni_code, mod_code, "conceptsbar"),
            html.H3("Reviews", style = {'font-family': 'Inter'}),
            dbc.Input(type = 'text', placeholder = "Leave your review here...", className = 'modreview')
        ],
        className="modlayout"
    )

