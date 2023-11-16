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


def fetch_data():
    url = "http://backend-1:5001/nus-ntu-smu/all-modules/"
    data_dict = eval(str(requests.get(url).text))

    return data_dict

def queryCheck(query):
    data_dict = fetch_data()
    query = cleanQuery(query)
    uni_code_list = ['nus-dsa', 'nus-dse', 'ntu', 'smu']
    
    results = [html.H1(f"Search Results for \"{query}\"", className = 'searchpage--header')]

    for uni_code in uni_code_list:
        uni_mods = data_dict[uni_code]
        
        for mod in uni_mods:
            header = mod["Module Code"]
            title = mod["Module Name"]
            desc = mod["Module Description"]
            concepts = mod["Key Concepts"]

            if header.lower().find(query.lower()) != -1 or title.lower().find(query.lower()) != -1 or desc.lower().find(query.lower()) != -1 or concepts.find(query.lower()) != -1:
                if uni_code == "ntu" or uni_code == "smu":
                    url = f"/module/{uni_code}-dsa/{header.upper()}"
                else:
                    url = f"/module/{uni_code}/{header.upper()}"
                
                header = f"[{uni_code.upper()}] {header}"
                
                section = html.Div(
                    children = [
                        html.H1(header, className = 'searchpage--header'),
                        html.H2(title, className = 'searchpage--title'),
                        html.P(descShorten(desc), className = 'searchpage--desc'),
                        html.A("See More Here", href = url, className = 'searchpage--link'),
                        html.P("   "),
                        html.Hr()
                    ],
                    className = 'searchpage--result'
                )
                results.append(section)

    if len(results) == 1:
        results.append(html.H2("Sorry, your search has no results. Try some other keywords!", className = 'searchpage--desc'))

    return results





def layout(query):
    results = queryCheck(query)
    return html.Div(results, className = 'searchpage')
