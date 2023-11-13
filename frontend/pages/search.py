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


def fetch_list_data(uni_code):
    url = f"http://localhost:5001/{uni_code}" #prereq information 
    uni = uni_code[0:3]
    full_module_data = eval(str(requests.get(url).text))[uni]["modules"] 
    mod_list = []
    for dct in full_module_data:
        mod_list.append(dct['name'])
    
    return mod_list

def fetch_mod_desc(uni_code, mod_code):
    mod_code = mod_code.upper() #to ensure all uppercase
    url = f"http://localhost:5001/{uni_code}/{mod_code}"
    data_dict = eval(str(requests.get(url).text))

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

    return header, title, desc

def queryCheck(query):
    query = cleanQuery(query)

    uni_code_list = ['nus-dsa', 'ntu-dsa', 'smu-dsa']
    #IDEA: run through every school's module information
    results = [html.H1(f"Search Results for \"{query}\"")]
    for uni_code in uni_code_list:
        mod_list = fetch_list_data(uni_code)

        for mod in mod_list:
            header, title, desc = fetch_mod_desc(uni_code, mod)
            url = f"/module/{uni_code}/{mod.upper()}"
            
            if header.lower().find(query.lower()) != -1 or title.lower().find(query.lower()) != -1 or desc.lower().find(query.lower()) != -1:
                section = html.Div(
                    children = [
                        html.H1(header),
                        html.H2(title),
                        html.P(desc),
                        html.A("See More Here", href = url)
                    ]
                )
                results.append(section)

    if len(results) == 1:
        results.append(html.H2("Sorry, your search has no results. Try some other keywords!"))

    return results


def layout(query):
    results = queryCheck(query)
    return html.Div(results)
