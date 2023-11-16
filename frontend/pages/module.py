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
    return eval(str(requests.get(url).text))

def fetch_glossary():
    url = 'http://localhost:5001/glossary_list/'
    return eval(str(requests.get(url).text))

def conceptsBar(uni_code, mod_code):
    #Load the relevant data concepts
    data_dict = fetch_data(uni_code, mod_code)
    concepts = data_dict["key_concepts"].upper().split(", ")
    glossary_list = [fetch_glossary()[x.lower()] for x in concepts]

    #Create dataframe 
    data = {
        "concept": concepts,
        "explanation": glossary_list,
        "val": [1 for i in range(len(concepts))],
        "x": [1 for i in range(len(concepts))]
    }
    df = pd.DataFrame(data)

    fig = px.bar(
        df, x = "x", y = 'val', custom_data = "explanation",
        color = 'concept', text = 'concept', orientation="h")


    
    fig.update_traces(textfont_size = 20, textposition="inside", insidetextanchor="middle", showlegend=False, width = 0.5)
    fig.update_yaxes(showgrid = False, visible = False)
    fig.update_xaxes(showgrid = False, visible = False)
    fig.update_layout(plot_bgcolor = 'rgba(0, 0, 0, 0)')
    fig.update_layout(margin = dict(l = 0.1, r = 0.1, t = 0.1, b = 0.1, pad = 0))
    print("user_defined hovertemplate:", fig.data[0].hovertemplate)
    fig.update_traces(hovertemplate='%{customdata}')
    #print("user_defined hovertemplate:", fig.data[0].hovertemplate)


    return html.Div(
        [
            html.H3("Key Concepts:", className = 'bartitle'),
            dcc.Graph(figure = fig, className = 'conceptBar')
        ]
    )


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
            conceptsBar(uni_code, mod_code),
            html.H3("Reviews", style = {'font-family': 'Inter'}),
            dbc.Input(type = 'text', placeholder = "Leave your review here...", className = 'modreview')
        ],
        className="modlayout"
    )
