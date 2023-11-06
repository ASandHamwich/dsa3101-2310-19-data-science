import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/compare')

#Layout for each individual course information page.

def course_layout(uni_code):
    if uni_code == 'nus1':
        name = "Data Science & Analytics"
        school = "National University of Singapore"
        desc = "placeholder text"

    if uni_code == 'nus2':
        name = "Data Science & Economics"
        school = "National University of Singapore"
        desc = "placeholder text"

    if uni_code == 'ntu1':
        name = "Data Science and Artificial Intelligence"
        school = "Nanyang Technological University"
        desc = "placeholder text"

    if uni_code == 'smu1':
        name = "Data Science & Analytics (2nd Major)"
        school = "Singapore Management University"
        desc = "placeholder text"
   
    return name, school, desc


def half_layout(uni_code):
    name, school, desc = course_layout(uni_code)

    return html.Div(
        children = [
            html.Div(
                children = [
                    html.H1(name),
                    html.H3(school),
                    html.P(desc)
                ]
            ),

            html.Div(
                children = [
                    html.Header('What you will learn')
                ]
            ),

            html.Div(
                children = [
                    html.H3('Course Tree'),
                    html.P('The course tree aims to provide an overview of the relationship between core courses in the programme.'),
                    #INSERT TREE HERE
                ]
            ),

            html.Div(
                children = [
                    html.H2('More Information')
                ]
            )
        ]
    )

left_child = half_layout("nus1")
right_child = half_layout("smu1")


layout = html.Div(
    children = [
        html.Div(children = left_child, className = 'compare--child1'),
        html.Div(children = right_child, className = 'compare--child2')
    ],
    className = 'compare'
)