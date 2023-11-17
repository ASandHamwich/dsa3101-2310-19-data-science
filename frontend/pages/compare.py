from pydoc import classname
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_cytoscape as cyto
import requests
import regex as re
import seaborn as sns
import numpy as np
import pandas as pd

from fetchFunction import *
from courseFunction import *

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/compare/course1=<uni_code_1>&course2=<uni_code_2>')

#Layout for each individual course information page.
    

####
def half_layout(uni_code):
    name, school, desc, img = course_layout(uni_code) #img not used here

    return html.Div(
        className="coursepage",
        children=[
            html.Div(
                children=[
                    html.H1(name, className = "coursepage--name"),
                    html.H3(school, className = "coursepage--school"),
                    html.P(desc, className = "coursepage--desc")
                ]
            ),

            html.Div(
                children=[
                    html.H4('What you will learn', className = "coursepage--desc")
                ]
            ),
            key_subjects(uni_code),
            html.Div(
                children=[
                    html.H3('Course Tree',className = "coursepage--school"),
                    html.P('The course tree aims to provide an overview of the relationship between core courses in the programme.',className = "coursepage--desc"),
                    html.H4('Legend', className = "coursepage--desc"),
                    html.P('Module A → Module B : A needs to be taken before B can be taken', className = "coursepage--legend1"),
                ]
            ),
            html.Div(
                children=legend(uni_code)
            ),
            html.Div(
                className='course-tree-container',
                children=[
                    # INSERT TREE HERE
                    cyto.Cytoscape(
                        # id='cytoscape',
                        id='cytoscape-layout-4',
                        elements= generate_content(uni_code),
                        layout=treelayout(uni_code),
                        style={'width': '100%', 'height': '100vh'},
                        minZoom=0.5,
                        maxZoom=2,
                        stylesheet=treestylesheet(uni_code)
                    )
                ]
            )
        ]
    )

def layout(uni_code_1, uni_code_2):
    return html.Div(
        children = [
            html.Div(children = half_layout(uni_code_1), className = 'compare--child'),
            html.Div(children = half_layout(uni_code_2), className = 'compare--child')
        ],
        className = 'compare'
    )


