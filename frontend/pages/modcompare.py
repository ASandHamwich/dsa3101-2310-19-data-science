import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/modcompare')

#Layout for each individual course information page.

para1 = 'This course is designed to be a continuation of DSA1101 Introduction to Data Science. It focuses on data science methodology and the ability to apply such methodology to practical applications. Real-world problems will be provided by both industrial and academic partners in domains such as transportation, consulting, finance, pharmaceutics, life sciences and physics.'

left = html.Div(
    children = [
        html.H1('[NUS] DSA3101'),
        html.H2('Data Science in Practice'),
        html.P(para1),
        html.H3('What You Will Learn [WIP]')
    ]
)

para2 = 'Convex optimisation is an indispensable technique in dealing with high-dimensional structured problems in data science. The course covers modelling examples; basic concepts for convex functions and sub-gradients; gradient and sub-gradient methods; accelerated proximal gradient methods; stochastic block coordinate descent methods; Lagrangian duals; splitting algorithms and implementations.'

right = html.Div(
    children = [
        html.H1('[NUS] DSA3102'),
        html.H2('Essential Data Analytics Tools: Convex Optimisation'),
        html.P(para2),
        html.H3('What You Will Learn [WIP]')
    ]
)


def layout():
    return html.Div(
        children = [
            html.Div(children = left, className = 'compare--child'),
            html.Div(children = right, className = 'compare--child')
        ],
        className = 'compare'
    )