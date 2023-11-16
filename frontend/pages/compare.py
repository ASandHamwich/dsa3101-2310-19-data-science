

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

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/compare/course1=<uni_code_1>&course2=<uni_code_2>')

#Layout for each individual course information page.

def course_layout(uni_code):
    if uni_code == 'nus-dsa':
        name = "Data Science & Analytics"
        school = "National University of Singapore"
        desc = "The four-year direct Honours programme is designed to prepare graduates who are ready to acquire, manage and explore data that will inspire change around the world. Students will read courses in Mathematics, Statistics and Computer Science, and be exposed to the interplay between these three key areas in the practice of data science." 


    if uni_code == 'nus-dse':
        name = "Data Science & Economics"
        school = "National University of Singapore"
        desc = "The Data Science and Economics (DSE) cross-disciplinary programme (XDP) aims to produce students who have strong foundation knowledge in data science and economics as well as hands-on experience with empirical analysis of economic data, to analyse and interpret the local and global impact of data on individuals, organisation, society and the global economic ecosystem. The DSE curriculum incorporates inter-disciplinary learning from data science and economics, with foundations in computer science, mathematics and statistics. In addition to higher-level courses that integrate knowledge and concepts from lower-level core foundational courses, students also read courses related to the application of data science and analytics to the financial market, labour market, and other applied economic issues in education, health, housing and industrial organisation."

    if uni_code == 'ntu-dsa':
        name = "Data Science and Artificial Intelligence"
        school = "Nanyang Technological University"
        desc = "An undergraduate degree programme in Data Science and Artificial Intelligence, based on rigorous training in the synergistic fields of statistics and computer science. The programme, which is run jointly by the School of Computer Science and Engineering and the School of Physical and Mathematical Sciences, targets students who have the vision of using data science and artificial intelligence (AI) to find innovative solutions to society’s pressing challenges. The curriculum provides students with opportunities to solve real-life problems in different applications domains ranging from science and technology, healthcare, business and finance, environmental sustainability, and more."


    if uni_code == 'smu-dsa':
        name = "Data Science & Analytics (2nd Major)"
        school = "Singapore Management University"
        desc = "The DSA second major focuses on applications of statistical modelling, machine learning algorithms, computing and information technology as well as simulation and predictive approaches to solve realworld problems encountered in all private and public institutions. The curriculum of the second major adopts a hands-on pedagogy in mathematics, statistics and computer science, emphasizing practical applications related to economics, social sciences, finance, risk management, business, insurance, and more."
   
    return name, school, desc


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
    for index, char in enumerate(node_id):
        if char in "0123456789":
            prefix = node_id[:index]
            return {'data': {'id': node_id, 'label': label,'url': url}, 'classes': f"{prefix}"}

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
        
def treelayout(uni_code):
    if 'smu' in uni_code:
        layout = {
            'name': 'grid'
        }
    else:
        layout = {'name': 'breadthfirst',
                'roots': root(uni_code)}
    return layout

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

def nodepalette(uni_code):
    mod_list, full_module_data = fetch_data(uni_code)
    prefix_list = []
    for mod in mod_list:
        for index, char in enumerate(mod):
            if char in "01234956789":
                prefix = mod[:index].lower()
                break
        if prefix not in prefix_list:
            prefix_list.append(prefix)
    palette = sns.color_palette("pastel", len(prefix_list))
    hex = palette.as_hex()
    return prefix_list, hex

def treestylesheet(uni_code):
    lst, backgroundhex = nodepalette(uni_code)
    stylesheet = [
        {
            'selector': 'edge',
            'style': {'target-arrow-color': '#999999', 'target-arrow-shape': 'triangle','curve-style': 'bezier'}
        },
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-valign':'center',
                'text-halign': 'center',
                'height': '30px',
                'width': '100px',
                'shape': 'round-rectangle',
                'color':'black'
            }
        }
    ]
    for i in range(len(backgroundhex)):
        dic = {
            'selector': f".{lst[i]}",
            'style':{
                'background-color': f"{backgroundhex[i]}"
            }
        }
        stylesheet.append(dic)
    return(stylesheet)

def module_type(mod_code):
    if mod_code == 'cs':
        return('Computer Science')
    if mod_code == 'dsa':
        return('Data Science and Analytics')
    if mod_code == 'dse':
        return ('Data Science and Economics')
    if mod_code == 'ma' or mod_code=='mh':
        return('Mathematics')
    if mod_code == 'st' or mod_code=='stat':
        return ('Statistics')
    if mod_code == 'qf':
        return('Quantitative Finance')
    if mod_code == 'cz':
        return ('Computer Science (Before 21/22)')
    if mod_code == 'sc':
        return ('Computer Science (21/22 Onwards)')
    if mod_code == 'is':
        return ('Information Systems')
    if mod_code == 'cor-is':
        return ('Computational Thinking')
    if mod_code == 'econ' or mod_code == "ec":
        return ('Economics')
    if mod_code == 'mktg':
        return ('Marketing')
    if mod_code == 'opim':
        return ('Operations Management')
    if mod_code == 'cor':
        return ('Spreadsheet Modelling and Analytics')

def legend(uni_code):
    lst, backgroundhex = nodepalette(uni_code)
    output=[]
    for i in range(len(backgroundhex)):
        output.append(html.P(f"{lst[i].upper()}" ' : ' f"{module_type(lst[i])}", 
                             style={ 
                                 'background-color':f"{backgroundhex[i]}",
                                },
                            className = "coursepage--legend2"
                            ),
                        )
    return output

def key_subjects(uni_code):
    mod_list, full_module_data = fetch_data(uni_code)
    prefix_list=[]
    for mod in mod_list:
        for index, char in enumerate(mod):
            if char in "0123456789":
                prefix=mod[:index].lower()
                break
        prefix_list.append(prefix)
    unique, counts = np.unique(prefix_list, return_counts=True)
    mod_type=[]
    for mod_code in unique:
        mod_type.append(module_type(mod_code))
    df=pd.DataFrame([unique, counts, mod_type], index=['unique','Number of Modules', 'module_type']).T
    fig = px.pie(df, values='Number of Modules', color=unique,
                hover_name='module_type', 
                labels={'module_type':'Module Type', 'values':'Number of Modules', 'color':'Module Code'},
                color_discrete_sequence=px.colors.sequential.Sunset)
    return dcc.Graph(id='subject-pie', figure=fig)



    


def half_layout(uni_code):
    name, school, desc = course_layout(uni_code)

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


