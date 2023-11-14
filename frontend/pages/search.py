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

def descShorten(desc):
    # Only leaves the first sentence in the description.
    sentenceEndIndex = desc.find(".")
    if sentenceEndIndex != len(desc) + 1 and sentenceEndIndex != -1:
        shortDesc = desc[0: sentenceEndIndex + 1]
        shortDesc += " ..."
        return shortDesc
    else:
        return desc

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

    if(uni_code.startswith("nus-dsa")):
        header = "[NUS] (DSA) " + data_dict["module_code"]
    
    if(uni_code.startswith("nus-dse")):
        header = "[NUS] (DSE) " + data_dict["module_code"]
    
    if(uni_code.startswith("ntu")):
        header = "[NTU] " + data_dict["module_code"]

    if(uni_code.startswith("smu")):
        header = "[SMU] " + data_dict["module_code"]

    title = data_dict["module_name"]
    desc = data_dict["module_description"]

    return header, title, desc


def queryCheck(query):
    query = cleanQuery(query)

    uni_code_list = ['nus-dsa', 'nus-dse', 'ntu-dsa', 'smu-dsa']
    #IDEA: run through every school's module information
    results = [html.H1(f"Search Results for \"{query}\"", className = 'searchpage--header')]
    for uni_code in uni_code_list:
        mod_list = fetch_list_data(uni_code)

        for mod in mod_list:
            header, title, desc = fetch_mod_desc(uni_code, mod)
            url = f"/module/{uni_code}/{mod.upper()}"
            
            if header.lower().find(query.lower()) != -1 or title.lower().find(query.lower()) != -1 or desc.lower().find(query.lower()) != -1:
                section = html.Div(
                    children = [
                        html.H1(header, className = 'searchpage--header'),
                        html.H2(title, className = 'searchpage--title'),
                        html.P(descShorten(desc), className = 'searchpage--desc'),
                        html.A("See More Here", href = url, className = 'searchpage--link'),
                        html.Br()
                    ],
                    className = 'searchpage--result'
                )
                results.append(section)

    if len(results) == 1:
        results.append(html.H2("Sorry, your search has no results. Try some other keywords!", className = 'searchpage--desc'))

    return results

# def fetch_data():
#     url = "http://localhost:5001/nus-ntu-smu/all-modules/"


def layout(query):
    results = queryCheck(query)
    return html.Div(results, className = 'searchpage')
