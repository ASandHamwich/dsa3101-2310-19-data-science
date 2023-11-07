import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/course/<uni_code>')

#Layout for each individual course information page.

def course_layout(uni_code):
    if uni_code == 'nus1':
        name = "Data Science & Analytics"
        school = "National University of Singapore"
        desc = "The four-year direct Honours programme is designed to prepare graduates who are ready to acquire, manage and explore data that will inspire change around the world. Students will read courses in Mathematics, Statistics and Computer Science, and be exposed to the interplay between these three key areas in the practice of data science." 
        img_path = "/assets/nus_pic.png"

    if uni_code == 'nus2':
        name = "Data Science & Economics"
        school = "National University of Singapore"
        desc = "The Data Science and Economics (DSE) cross-disciplinary programme (XDP) aims to produce students who have strong foundation knowledge in data science and economics as well as hands-on experience with empirical analysis of economic data, to analyse and interpret the local and global impact of data on individuals, organisation, society and the global economic ecosystem. The DSE curriculum incorporates inter-disciplinary learning from data science and economics, with foundations in computer science, mathematics and statistics. In addition to higher-level courses that integrate knowledge and concepts from lower-level core foundational courses, students also read courses related to the application of data science and analytics to the financial market, labour market, and other applied economic issues in education, health, housing and industrial organisation."
        img_path = "/assets/nus_pic.png"

    if uni_code == 'ntu1':
        name = "Data Science and Artificial Intelligence"
        school = "Nanyang Technological University"
        desc = "An undergraduate degree programme in Data Science and Artificial Intelligence, based on rigorous training in the synergistic fields of statistics and computer science. The programme, which is run jointly by the School of Computer Science and Engineering and the School of Physical and Mathematical Sciences, targets students who have the vision of using data science and artificial intelligence (AI) to find innovative solutions to society’s pressing challenges. The curriculum provides students with opportunities to solve real-life problems in different applications domains ranging from science and technology, healthcare, business and finance, environmental sustainability, and more."
        img_path = "/assets/ntu_pic.jpg"

    if uni_code == 'smu1':
        name = "Data Science & Analytics (2nd Major)"
        school = "Singapore Management University"
        desc = "The DSA second major focuses on applications of statistical modelling, machine learning algorithms, computing and information technology as well as simulation and predictive approaches to solve realworld problems encountered in all private and public institutions. The curriculum of the second major adopts a hands-on pedagogy in mathematics, statistics and computer science, emphasizing practical applications related to economics, social sciences, finance, risk management, business, insurance, and more."
        img_path = '/assets/smu_pic.jpg'
    
    return name, school, desc, img_path 


def layout(uni_code):
    name, school, desc, img_path = course_layout(uni_code)

    return html.Div(
        children = [
            html.Div(
                style={'display':"inline-block",
                       'width':'750px'},
                children = [
                    html.H1(name),
                    html.H3(school),
                    html.P(desc),
                ]
            ),

            html.Div(
                style={'display':'inline-block',
                       'margin':'30px'},
                children = [
                    html.Img(src=img_path,
                             style={'height':'200px',
                                    'width':'400px'}),
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