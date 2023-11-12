import dash
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import requests
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/search=<query>')

#Idea
#Take query
#flatten all module descriptions and cycle through all
#if any, then add to list
#

def cleanQuery(query):
    final = query.replace("%20", " ")
    return final

uni_code_list = ['nus-dsa', 'nus-dse', 'ntu-dsa', 'smu-dsa']

def fetch_list_data(uni_code):
    url = f"http://localhost:5001/{uni_code}" #prereq information 
    uni = uni_code[0:3]
    full_module_data = eval(str(requests.get(url).text))[uni]["modules"] 
    mod_list = []
    for dct in full_module_data:
        mod_list.append(dct['name'])
    
    return mod_list

def fetch_mod_desc(uni_code, mod_code):
    url = f"http://localhost:5001/{uni_code}" #prereq information 
    uni = uni_code[0:3]
    full_module_data = eval(str(requests.get(url).text))[uni]["modules"] 





def page_layout(query):
    header = html.H1(f"Search Results for \"{query}\"")
    return header

def generateResult():
    return HTML.Div()


def layout(query):
    query = cleanQuery(query)
    return page_layout(query)
