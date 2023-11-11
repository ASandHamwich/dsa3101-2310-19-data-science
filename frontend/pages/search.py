import dash
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import requests
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/search=<query>')

def cleanQuery(query):
    final = query.replace("%20", " ")
    return final

def page_layout(query):
    header = html.H1(f"Search Results for \"{query}\"")

    return header


def layout(query):
    query = cleanQuery(query)
    return page_layout(query)
