import dash
from dash import html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/home')

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
        desc = "The DSA second major focuses on applications of statistical modelling, machine learning algorithms, computing and information technology as well as simulation and predictive approaches to solve real-world problems encountered in all private and public institutions. The curriculum of the second major adopts a hands-on pedagogy in mathematics, statistics and computer science, emphasizing practical applications related to economics, social sciences, finance, risk management, business, insurance, and more."
        img_path = '/assets/smu_pic.jpg'

    return name, school, desc, img_path

def buttonFormat(name, id, image_url):
    return html.Div(
        children=[
            html.Img(src=image_url, className='checkbox-image', style={'width': '150px', 'height': '75px', 'margin-left': '30px', 'margin-top': '15px'}),
            dbc.Checkbox(id=f'checkbox_{id}', className='course--add',style={'margin-top': '100px'}),
            html.Button(name, id=id, className='course--link', style={'margin-top': '0px'})
        ],
        className='course--rect'
    )

layout = html.Div(
    children=[
        html.Div(
            children=html.P('Course credit conversion for the universities: 4MC (NUS) = 3AU (NTU) = 2CU(SMU)', className='info--text'),
            className='info'
        ),

        html.Div(
            children=[
                dcc.Location(id='url'),
                buttonFormat('NUS: Data Science and Analytics', 'nus-dsa', '/assets/nus_logo.png'),
                buttonFormat('NUS: Data Science and Economics', 'nus-dse', '/assets/nus_logo.png'),
                buttonFormat('NTU: Data Science and Artificial Intelligence', 'ntu-dsa', '/assets/nus_logo.png'),
                buttonFormat('SMU: Data Science and Analytics (2nd Major)', 'smu-dsa', '/assets/nus_logo.png')
            ],
            className='course'
        ),

        html.Div(
            html.Button('Compare', id='comp', style={
                'background-color': '#F9CA84', 'border-color': '#F9CA84', 'font-size': '25px',
                'border-radius': '10px', 'margin': '20px'
            }),
            style={'display': 'flex', 'margin': '20px', 'justifyContent': 'center'}
        ),

        html.Br()
    ],
    style={'background-color': 'white'}
)

@callback(
    Output('url', 'pathname'), [
        Input('nus-dsa', 'n_clicks'),
        Input('nus-dse', 'n_clicks'),
        Input('ntu-dsa', 'n_clicks'),
        Input('smu-dsa', 'n_clicks'),
        Input('comp', 'n_clicks'),
        Input('checkbox_nus-dsa', 'value'),
        Input('checkbox_nus-dse', 'value'),
        Input('checkbox_ntu-dsa', 'value'),
        Input('checkbox_smu-dsa', 'value')
    ]
)
def buttonPress(nus1_clicks, nus2_clicks, ntu1_clicks, smu1_clicks, comp, checkbox_nus1, checkbox_nus2, checkbox_ntu1,
                checkbox_smu1):
    if nus1_clicks is not None:
        return '/course/nus-dsa'
    if nus2_clicks is not None:
        return '/course/nus-dse'
    if ntu1_clicks is not None:
        return '/course/ntu-dsa'
    if smu1_clicks is not None:
        return '/course/smu-dsa'

    # Checkbox
    if comp is not None:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'comp' in changed_id:

            checkbox = []
            cb_dict = {'nus-dsa': checkbox_nus1, 'nus-dse': checkbox_nus2, 'ntu-dsa': checkbox_ntu1,
                       'smu-dsa': checkbox_smu1}
            for key in cb_dict:
                if cb_dict[key] is None:
                    continue
                else:
                    checkbox.append(key)

            if len(checkbox) == 2:
                return f'/compare/course1={checkbox[0]}&course2={checkbox[1]}'

    else:
        return None

