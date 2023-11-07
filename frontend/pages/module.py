import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/module/nus/dsa1101')

para = "The abundance of data being harvested from various sectors of today’s society increases the demand for skilled data science practitioners. This course introduces foundational data science concepts to prepare students for tackling real-world data analytic challenges. Major topics include basic concepts in probability and statistics, data manipulation, supervised and unsupervised learning, model validation and big data analysis, alongside special topics discussed in guest lectures delivered by practicing data scientists from government and industry. Throughout the course, students will learn fundamental R programming skills to implement and apply the data science methods in motivating realworld case studies from diverse fields."

layout = html.Div(
    children = [
        html.H1('[NUS] DSA1101'),
        html.H2('Introduction to Data Science'),
        html.P(para),
        html.H3('What You Will Learn [WIP]')
    ]
)