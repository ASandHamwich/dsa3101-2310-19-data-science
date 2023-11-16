import dash
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import requests
import dash_bootstrap_components as dbc


#For search
def fetch_data():
    url = "http://localhost:5001/nus-ntu-smu/all-modules/"
    data_dict = eval(str(requests.get(url).text))

    return data_dict


#for module
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


#for course
def fetch_data(uni_code):
    url = f"http://localhost:5001/{uni_code}" #prereq information 
    uni = uni_code[0:3]
    full_module_data = eval(str(requests.get(url).text))[uni]["modules"] # returns a list of dictionaries for all mods
    # Note that some prereqs are not part of the core curriculum; those will be left out of the final graph.

    # Fetch list of mods that will show up in the tree itself; i.e. the mods that are directly related to data science
    mod_list = []
    for dct in full_module_data:
        mod_list.append(dct['name'])
    
    return mod_list, full_module_data

def fetch_all():
    url = 'http://localhost:5001/nus-ntu-smu/all-modules/'
    return eval(str(requests.get(url).text))


