import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_cytoscape as cyto

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/compare/course1=<uni_code_1>&course2=<uni_code_2>')

#Layout for each individual course information page.

def course_layout(uni_code):
    if uni_code == 'nus1':
        name = "Data Science & Analytics"
        school = "National University of Singapore"
        desc = "The four-year direct Honours programme is designed to prepare graduates who are ready to acquire, manage and explore data that will inspire change around the world. Students will read courses in Mathematics, Statistics and Computer Science, and be exposed to the interplay between these three key areas in the practice of data science." 


    if uni_code == 'nus2':
        name = "Data Science & Economics"
        school = "National University of Singapore"
        desc = "The Data Science and Economics (DSE) cross-disciplinary programme (XDP) aims to produce students who have strong foundation knowledge in data science and economics as well as hands-on experience with empirical analysis of economic data, to analyse and interpret the local and global impact of data on individuals, organisation, society and the global economic ecosystem. The DSE curriculum incorporates inter-disciplinary learning from data science and economics, with foundations in computer science, mathematics and statistics. In addition to higher-level courses that integrate knowledge and concepts from lower-level core foundational courses, students also read courses related to the application of data science and analytics to the financial market, labour market, and other applied economic issues in education, health, housing and industrial organisation."

    if uni_code == 'ntu1':
        name = "Data Science and Artificial Intelligence"
        school = "Nanyang Technological University"
        desc = "An undergraduate degree programme in Data Science and Artificial Intelligence, based on rigorous training in the synergistic fields of statistics and computer science. The programme, which is run jointly by the School of Computer Science and Engineering and the School of Physical and Mathematical Sciences, targets students who have the vision of using data science and artificial intelligence (AI) to find innovative solutions to society’s pressing challenges. The curriculum provides students with opportunities to solve real-life problems in different applications domains ranging from science and technology, healthcare, business and finance, environmental sustainability, and more."


    if uni_code == 'smu1':
        name = "Data Science & Analytics (2nd Major)"
        school = "Singapore Management University"
        desc = "The DSA second major focuses on applications of statistical modelling, machine learning algorithms, computing and information technology as well as simulation and predictive approaches to solve realworld problems encountered in all private and public institutions. The curriculum of the second major adopts a hands-on pedagogy in mathematics, statistics and computer science, emphasizing practical applications related to economics, social sciences, finance, risk management, business, insurance, and more."
   
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
                    cyto.Cytoscape(
                        id = 'cytoscape',
                        elements = [
                            {'data':{'id':'dsa1101', 'label': 'DSA1101'}},
                            {'data':{'id':'st2131', 'label':'ST2131'}},
                            {'data':{'id':'ma2001', 'label':'MA2001'}},
                            {'data':{'id':'dsa2101', 'label':'DSA2101'}},
                            {'data':{'id':'dsa3101', 'label':'DSA3101'}},
                            {'data':{'id':'cs2040', 'label':'CS2040'}},
                            {'data':{'id':'dsa2102', 'label':'DSA2102'}},
                            {'data':{'id':'ma2002', 'label':'MA2002'}},
                            {'data':{'id':'ma2311', 'label':'MA2311'}},
                            {'data':{'id':'st2132', 'label':'ST2132'}},
                            {'data':{'id':'cs3244', 'label':'CS3244'}},
                            {'data':{'id':'dsa3102', 'label':'DSA3102'}},
                            {'data':{'id':'st3131', 'label':'ST3131'}},
                            {'data':{'id':'dsa426x', 'label':'DSA426X'}},
                            {'data':{'id':'cs1010s', 'label':'CS1010S'}},
                            {'data':{'id':'dsa4211', 'label':'DSA4211'}},
                            {'data':{'id':'dsa4212', 'label':'DSA4212'}},
                            {'data':{'id':'dse4211', 'label':'DSE4211'}},
                            {'data':{'id':'dse4212', 'label':'DSE4212'}},
                            {'data': {'source':'dsa1101', 'target':'dsa2101'}},
                            {'data': {'source':'ma2001', 'target':'dsa2101'}},
                            {'data': {'source':'ma2001', 'target':'dsa3102'}},
                            {'data': {'source':'ma2001', 'target':'dsa4212'}},
                            {'data': {'source':'ma2001', 'target':'dsa2102'}},
                            {'data': {'source':'ma2002', 'target':'st2131'}},
                            {'data': {'source':'ma2002', 'target':'dsa2102'}},
                            {'data': {'source':'ma2002', 'target':'ma2311'}},
                            {'data': {'source':'cs1010s', 'target':'dsa3102'}},
                            {'data': {'source':'cs1010s', 'target':'cs2040'}},
                            {'data': {'source':'dsa2101', 'target':'dsa3101'}},
                            {'data': {'source':'st2131', 'target':'dsa2101'}},
                            {'data': {'source':'st2131', 'target':'st2132'}},
                            {'data': {'source':'st2131', 'target':'st3131'}},
                            {'data': {'source':'st3131', 'target':'dsa4211'}},
                            {'data': {'source':'dsa3101', 'target':'dsa426x'}},
                            {'data': {'source':'cs2040', 'target':'cs3244'}},
                            {'data': {'source':'cs3244', 'target':'dsa426x'}},
                            {'data': {'source':'st2132', 'target':'dsa3101'}},
                            {'data': {'source':'st2132', 'target':'dsa4212'}},
                            {'data': {'source':'ma2311', 'target':'dsa4212'}},
                            {'data': {'source':'dsa2102', 'target':'dse4211'}},
                            {'data': {'source':'dsa2102', 'target':'dse4212'}}
                        ],
                        layout={'name':'cose'},
                        style={'width':'600x', 'height':'400px'},
                        stylesheet = [
                            {
                                'selector':'node',
                                'style':{
                                    'content':'data(label)',
                                    'text-valign': 'center',
                                    'text-halign':'center',
                                    'height':'30px',
                                    'width':'85px',
                                    'shape':'rectangle',
                                    'background-color':'#8BB4DB'
                                }
                            },
                            {
                                'selector':'edge',
                                'style':{'target-arrow-color':'#999999', 'target-arrow-shape':'triangle', 'curve-style':'bezier'}
                            }
                        ]
                        panningEnabled=False,
                        userPanningEnabled=False,
                        minZoom=1,
                        maxZoom=1
                    )
                ]
            ),

            html.Div(
                children = [
                    html.H2('More Information'),
                    #temporary fake links, replace soon
                    html.H3('NUSMods: for more NUS modules',
                            style = {'text-decoration':'underline'}),
                    html.H3('NUS bus app',
                            style = {'text-decoration':'underline'}),
                    html.H3('NUS College of Humanities and Sciences: Common curriculum and study plan',
                            style = {'text-decoration':'underline'})
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
