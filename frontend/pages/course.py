import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_cytoscape as cyto
import regex as re
import requests
import seaborn as sns
import numpy as np
import pandas as pd

from fetchFunction import *
from courseFunction import *

import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template = '/course/<uni_code>')

#Layout for each individual course information page.

def course_links(uni_code):
    if uni_code == 'nus-dsa':
        return html.Div(
            children=[
                html.H2('More Information', className='coursepage--desc'),
                html.H4(
                    html.A(
                        'NUS Official Website: Major in Data Science & Analytics', 
                        href='https://www.stat.nus.edu.sg/prospective-students/undergraduate-programme/data-science-and-analytics/',
                        target='_blank'
                    ), 
                    className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NUSMods: For More NUS Modules', 
                        href='https://nusmods.com/', 
                        target='_blank'
                    ),
                    className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NUS College of Humanities and Sciences: Common Curriculum',
                        href='https://chs.nus.edu.sg/programmes/common-curriculum/',
                        target='_blank'
                    ), 
                    className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NUS Bus App: For NUS Bus Timings and Routes',
                        href='https://play.google.com/store/apps/details?id=nus.ais.mobile.android.shuttlebus&hl=en&gl=US&pli=1',
                        target='_blank'
                    ), 
                    className='coursepage--link'
                )
            ]
        )

    if uni_code == 'nus-dse':
        return html.Div(
            children=[
                html.H2('More Information', className='coursepage--desc'),
                html.H4(
                    html.A(
                        'NUS Official Website: Major in Data Science & Economics', 
                        href='https://www.stat.nus.edu.sg/prospective-students/undergraduate-programme/data-science-and-economics/',
                        target='_blank'
                    ), 
                    className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NUSMods: For More NUS Modules', 
                        href='https://nusmods.com/', 
                        target='_blank'
                    ),
                    className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NUS College of Humanities and Sciences: Common Curriculum',
                        href='https://chs.nus.edu.sg/programmes/common-curriculum/',
                        target='_blank'
                    ), 
                    className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NUS Bus App: For NUS Bus Timings and Routes',
                        href='https://play.google.com/store/apps/details?id=nus.ais.mobile.android.shuttlebus&hl=en&gl=US&pli=1',
                        target='_blank'
                    ), 
                    className='coursepage--link'
                )
            ]
        )

    if uni_code == 'ntu-dsa':
        return html.Div(
            children=[
                html.H2('More Information', className='coursepage--desc'),
                html.H4(
                    html.A(
                        "NTU Official Website: Bachelor of Science in Data Science and Artificial Intelligence",
                        href='https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-science-in-data-science-artificial-intelligence',
                        target='_blank'
                    ),
                        className='coursepage--link'
                ),
                html.H4(
                    html.A(
                        'NTU Content of Courses: For More NTU Modules',
                        href='https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main',
                        target='_blank'
                    ),
                        className='coursepage--link'

                ),
                html.H4(
                    html.A(
                        'Nanyang Mods: For Reviews on NTU Modules',
                        href='https://www.nanyangmods.com/',
                        target='_blank'
                    ),
                        className='coursepage--link'

                ),
                html.H4(
                    html.A(
                        'NTU Omnibus: For NTU Bus Timings and Routes',
                        href='https://play.google.com/store/apps/details?id=sg.edu.ntu.apps.ntuomnibus&hl=en&gl=US',
                        target='_blank'
                    ),
                        className='coursepage--link'

                )
            ]
        )

    if uni_code == 'smu-dsa':
        return html.Div(
            children=[
                html.H2('More Information', className='coursepage--desc'),
                html.H4(
                    html.A(
                        'SMU Official Website: 2nd Major in Data Science and Analytics',
                        href='https://economics.smu.edu.sg/bachelor-science-economics/curriculum/2nd-major-data-science-and-analytics',
                        target='_blank'
                    ),
                        className='coursepage--link'

                ),
                html.H4(
                    html.A(
                        'SMU Student Life: For Clubs and CCAs',
                        href='https://vivace.smu.edu.sg/',
                        target='_blank'
                    ),
                        className='coursepage--link'

                ),
                html.H4(
                    html.A(
                        'SMU School Publication: The Blue and Gold',
                        href='https://theblueandgold.sg/about',
                        target='_blank'
                    ),
                        className='coursepage--link'
                )
            ]
        )


# Cytoscape Format
# LIST
    # DICTIONARY OF DATA
        # DICTIONARY OF ID, LABEL, AND URL
        # + 
        # DICTIONARY OF SOURCE + TARGET


###
def layout(uni_code):
    name, school, desc, img_path = course_layout(uni_code)

    return html.Div(
        className="coursepage",
        children=[
            html.Div(
                children=[
                    html.H1(name, className = "coursepage--name"),
                    html.H3(school, className = "coursepage--school"),
                    html.P(desc, className = "coursepage--desc")
                ],
                className = "coursepage--courseinfo"
            ),

            html.Div( # Adjusted margin-top to reduce the gap 
                className = "coursepage--schimg",
                children=[
                    html.Img(src=img_path, className = "coursepage--courseimg"),
                ]
            ),

            html.Div(
                className='header-section',
                children=[
                    html.H3('What You Will Learn', className = "coursepage--desc"),
                ]
            ),

            key_subjects(uni_code),

            html.Div(
                children = [
                    html.H4('Course Tree', className = "coursepage--school"),
                    html.P('The course tree aims to provide an overview of the relationship between core courses in the programme.', className = "coursepage--desc"),
                    html.H4('Legend', className = "coursepage--desc"),
                    html.P('Module A → Module B : A needs to be taken before B can be taken', className = "coursepage--legend1")
                ]
            ),

            html.Div(
                children = legend(uni_code)
            ),

            html.Div(
                style={'margin-bottom': '10px'},  
                children=[
                    dcc.Location(id='location'),
                    # INSERT TREE HERE
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=generate_content(uni_code),
                        layout = treelayout(uni_code),
                        #style={'width': '1200px', 'height': '800px'},
                        style={'width': '100%', 'height': '100vh'},
                        minZoom=0.5,
                        maxZoom=1.5,
                        stylesheet=treestylesheet(uni_code)
                    )
                ]
            ),
            course_links(uni_code)
        ]
    )


@callback(
    Output("location", "href"),
    Input("cytoscape", "tapNodeData"),
    prevent_initial_call=True,
)
def navigate_to_url(node_data):
    return f"{node_data['url']}"
