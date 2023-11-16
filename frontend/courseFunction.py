import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_cytoscape as cyto
import regex as re
import requests
import seaborn as sns
import numpy as np
import pandas as pd

import dash_bootstrap_components as dbc

def key_concepts(uni_code):
    full_dict = fetch_all()
    all_key_concepts = []
    # For NTU/SMU: 
    if not uni_code.startswith("nus"):
        uni_code = uni_code[:3]
    uni_mods=full_dict[uni_code]
    for mod in uni_mods:
        key_concepts=mod["Key Concepts"].split(", ")
        all_key_concepts.extend(key_concepts)
    unique, counts = np.unique(all_key_concepts, return_counts=True)
    df=pd.DataFrame([unique, counts], index=['unique','counts']).T
    fig = px.pie(df, values=counts, color=unique, hover_name=unique, labels=unique)
    return dcc.Graph(id='concept-pie', figure=fig)

def key_subjects(uni_code):
    mod_list, full_module_data = fetch_data(uni_code)
    prefix_list=[]
    for mod in mod_list:
        for index, char in enumerate(mod):
            if char in "0123456789":
                prefix=mod[:index].lower()
                break
        prefix_list.append(prefix)
    unique, counts = np.unique(prefix_list, return_counts=True)
    mod_type=[]
    for mod_code in unique:
        mod_type.append(module_type(mod_code))
    df=pd.DataFrame([unique, counts, mod_type], index=['unique','counts', 'module_type']).T
    fig = px.pie(df, values=counts, names='module_type', color=unique, 
                 hover_name='module_type', 
                 labels={'module_type':'Module Type', 'values':'Number of Modules', 'color':'Module Code'},
                 color_discrete_sequence=px.colors.sequential.Sunset)
    return dcc.Graph(id='subject-pie', figure=fig)