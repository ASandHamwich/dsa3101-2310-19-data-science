import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_cytoscape as cyto

import requests

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/course/<uni_code>')

#Layout for each individual course information page.

def course_layout(uni_code):
    if uni_code == 'nus-dsa':
        name = "Data Science & Analytics"
        school = "National University of Singapore"
        desc = "The four-year direct Honours programme is designed to prepare graduates who are ready to acquire, manage and explore data that will inspire change around the world. Students will read courses in Mathematics, Statistics and Computer Science, and be exposed to the interplay between these three key areas in the practice of data science." 
        img_path = "/assets/nus_pic.png"

    if uni_code == 'nus-dse':
        name = "Data Science & Economics"
        school = "National University of Singapore"
        desc = "The Data Science and Economics (DSE) cross-disciplinary programme (XDP) aims to produce students who have strong foundation knowledge in data science and economics as well as hands-on experience with empirical analysis of economic data, to analyse and interpret the local and global impact of data on individuals, organisation, society and the global economic ecosystem. The DSE curriculum incorporates inter-disciplinary learning from data science and economics, with foundations in computer science, mathematics and statistics. In addition to higher-level courses that integrate knowledge and concepts from lower-level core foundational courses, students also read courses related to the application of data science and analytics to the financial market, labour market, and other applied economic issues in education, health, housing and industrial organisation."
        img_path = "/assets/nus_pic.png"

    if uni_code == 'ntu-dsa':
        name = "Data Science and Artificial Intelligence"
        school = "Nanyang Technological University"
        desc = "An undergraduate degree programme in Data Science and Artificial Intelligence, based on rigorous training in the synergistic fields of statistics and computer science. The programme, which is run jointly by the School of Computer Science and Engineering and the School of Physical and Mathematical Sciences, targets students who have the vision of using data science and artificial intelligence (AI) to find innovative solutions to society’s pressing challenges. The curriculum provides students with opportunities to solve real-life problems in different applications domains ranging from science and technology, healthcare, business and finance, environmental sustainability, and more."
        img_path = "/assets/ntu_pic.jpg"

    if uni_code == 'smu-dsa':
        name = "Data Science & Analytics (2nd Major)"
        school = "Singapore Management University"
        desc = "The DSA second major focuses on applications of statistical modelling, machine learning algorithms, computing and information technology as well as simulation and predictive approaches to solve realworld problems encountered in all private and public institutions. The curriculum of the second major adopts a hands-on pedagogy in mathematics, statistics and computer science, emphasizing practical applications related to economics, social sciences, finance, risk management, business, insurance, and more."
        img_path = '/assets/smu_pic.jpg'
    
    return name, school, desc, img_path 

# Cytoscape Format
# LIST
    # DICTIONARY OF DATA
        # DICTIONARY OF ID, LABEL, AND URL
        # + 
        # DICTIONARY OF SOURCE + TARGET


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


def node_dict(module, uni_code):
    node_id = module.lower()
    label = module.upper()
    url = f'/module/{uni_code}/{node_id}'
    return {'data': {'id': node_id, 'label': label, 'url': url}}

def edge_dict(source, target):
    source = source.lower()
    target = target.lower()
    return {'data': {'source': source, 'target': target}}


def flattenCheck(mod_list, curr_data):
    prereq_str = str(curr_data["pre-requisites"])
    #print("CHECKPOINT 2")
    #print(prereq_str)
    source_list = []

    for mod in mod_list:
        if prereq_str.find(mod) != -1:
            source_list.append(mod)
    
    #print('CHECKPOINT 3')
    #print(source_list)
    return source_list

def root(uni_code):
    mod_list, full_module_data = fetch_data(uni_code)
    is_root = True
    root_list = ''
    for index in range(len(mod_list)):
        mod = mod_list[index]
        module_data = full_module_data[index]
        source_list = flattenCheck(mod_list, module_data)
        if not source_list:
            if root_list == '':
                root_list += f'[id = "{mod.lower()}"]'
            else:
                root_list += f', [id = "{mod.lower()}"]'
    return(root_list)
        


def generate_edge(mod_list, curr_data, uni_code, mod):

    source_list = flattenCheck(mod_list, curr_data)
    result = []

    for source in source_list:
        result.append(edge_dict(source, mod))

    return result



def generate_content(uni_code):
    mod_list, full_module_data = fetch_data(uni_code)

    content = []
    
    # Add all the Node data in first.
    for index in range(len(mod_list)):
        mod = mod_list[index]

        # Node data
        node_data = node_dict(mod, uni_code)
        content.append(node_data)
    
    #Add all the edge data in.
    for index in range(len(mod_list)):
        mod = mod_list[index]
        curr_data = full_module_data[index]
        #print("CHECKPOINT 1")
        #print(curr_data)

        # Edge data
        edge_list = generate_edge(mod_list, curr_data, uni_code, mod)
        content.extend(edge_list)

    return content


def layout(uni_code):
    name, school, desc, img_path = course_layout(uni_code)

    return html.Div(
        style={
            'padding': '10px',
        },
        children=[
            html.Div(
                style={'display': "inline-block", 'width': '750px'},
                children=[
                    html.H1(name),
                    html.H3(school),
                    html.P(desc)
                ]
            ),

            html.Div(
                style={'display': 'inline-block', 'margin': '10px 30px 0 30px'},  # Adjusted margin-top to reduce the gap
                children=[
                    html.Img(src=img_path, style={'height': '200px', 'width': '400px'}),
                ]
            ),

            html.Div(
                className='header-section',
                children=[
                    html.Header('What you will learn'),
                ]
            ),

            html.Div(
                style={'margin-bottom': '10px'},  # Added margin-bottom to reduce the gap
                children=[
                    html.H3('Course Tree'),
                    html.P('The course tree aims to provide an overview of the relationship between core courses in the programme.'),
                    # INSERT TREE HERE
                    dcc.Location(id='location'),
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=generate_content(uni_code),
                        layout={'name': 'breadthfirst',
                                'roots': root(uni_code)},
                        #style={'width': '1200px', 'height': '800px'},
                        style={'width': '100%', 'height': '100vh'},
                        minZoom=0.5,
                        maxZoom=1.5,
                        stylesheet=[
                            {
                                'selector': 'node',
                                'style': {
                                    'content': 'data(label)',
                                    'text-valign': 'center',
                                    'text-halign': 'center',
                                    'height': '30px',
                                    'width': '85px',
                                    'shape': 'rectangle',
                                    'background-color': '#8BB4DB'
                                }
                            },
                            {
                                'selector': 'edge',
                                'style': {'target-arrow-color': '#999999', 'target-arrow-shape': 'triangle',
                                          'curve-style': 'bezier'}
                            }
                        ]
                    )
                ]
            ),
            html.Div(
                children=[
                    html.H2('More Information'),
                    html.H4(html.A('NUS Official Website: Major in Data Science & Analytics',
                                   href='https://www.stat.nus.edu.sg/prospective-students/undergraduate-programme/data-science-and-analytics/',
                                   target='_blank'), style={'text-decoration': 'underline'}),
                    html.H4(html.A('NUSMods: for more NUS modules', href='https://nusmods.com/', target='_blank'),
                            style={'text-decoration': 'underline'}),
                    html.H4(html.A('NUS College of Humanities and Sciences: Common Curriculum',
                                   href='https://chs.nus.edu.sg/programmes/common-curriculum/',
                                   target='_blank'), style={'text-decoration': 'underline'}),
                    html.H4(html.A('NUS bus app: for NUS bus timings and routes',
                                   href='https://play.google.com/store/apps/details?id=nus.ais.mobile.android.shuttlebus&hl=en&gl=US&pli=1',
                                   target='_blank'), style={'text-decoration': 'underline'})
                ]
            )
        ]
    )


@callback(
    Output("location", "href"),
    Input("cytoscape", "tapNodeData"),
    prevent_initial_call=True,
)
def navigate_to_url(node_data):
    return f"{node_data['url']}"
