import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/module/nus/<mod_code>')

para1 = "The abundance of data being harvested from various sectors of today’s society increases the demand for skilled data science practitioners. This course introduces foundational data science concepts to prepare students for tackling real-world data analytic challenges. Major topics include basic concepts in probability and statistics, data manipulation, supervised and unsupervised learning, model validation and big data analysis, alongside special topics discussed in guest lectures delivered by practicing data scientists from government and industry. Throughout the course, students will learn fundamental R programming skills to implement and apply the data science methods in motivating realworld case studies from diverse fields."
para2 = "This course is designed to be a continuation of DSA1101 Introduction to Data Science. It focuses on data science methodology and the ability to apply such methodology to practical applications. Real-world problems will be provided by both industrial and academic partners in domains such as transportation, consulting, finance, pharmaceutics, life sciences and physics."
para3 = "Convex optimisation is an indispensable technique in dealing with high-dimensional structured problems in data science. The course covers modelling examples; basic concepts for convex functions and sub-gradients; gradient and sub-gradient methods; accelerated proximal gradient methods; stochastic block coordinate descent methods; Lagrangian duals; splitting algorithms and implementations."

def temp(mod_code):
    if mod_code == 'dsa1101':
        return html.Div(
            children = [
                html.H1('[NUS] DSA1101'),
                html.H2('Introduction to Data Science'),
                html.P(para1),
                html.H3('What You Will Learn [WIP]')
            ]
        )
    if mod_code == 'dsa3101':
        return html.Div(
            children = [
                html.H1('[NUS] DSA3101'),
                html.H2('Data Science in Practice'),
                html.P(para2),
                html.H3('What You Will Learn [WIP]')
            ]
        )
    if mod_code == 'dsa3102':
        return html.Div(
            children = [
                html.H1('[NUS] DSA3102'),
                html.H2('Essential Data Analytics Tools: Convex Optimisation'),
                html.P(para3),
                html.H3('What You Will Learn [WIP]')
            ]
        )
    
    else:
        return html.Div(
            children = [
                html.H1('PLACEHOLDER'),
                html.H2('PLACEHOLDER'),
                html.P('PLACEHOLDER'),
                html.H3('What You Will Learn [WIP]')
            ]
        )

def temp2(mod_code):
    if mod_code == 'dsa3101':
        return html.Div(
            children = [
                html.H4('Similar Modules'),
                html.Button('DSA3102', id = 'button1')
            ],
            className = 'module--col'
        )
    if mod_code == 'dsa3102':
        return html.Div(
            children = [
                html.H4('Similar Modules'),
                html.Button('DSA3101', id = 'button1')
            ],
            className = 'module--col'
        )
    else:
        return html.Div(
            children = [
                html.H4('Similar Modules'),
                html.P('No similar modules found.')
            ],
            className = 'module--col'
        )


def layout(mod_code):
    return html.Div(
        children = [
            dcc.Location(id = 'lol'),
            temp(mod_code),
            temp2(mod_code)
        ],
    className = 'module'
    )

@callback (
    Output('lol', 'pathname'), 
    Input('button1', 'n_clicks')
)

def lmao(button1):
    if button1 is not None:
        return '/modcompare'