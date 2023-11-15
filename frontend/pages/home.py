import dash
from dash import html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

def course_layout(uni_code): # thinking of implementing this so as to reduce hardcoding
    if uni_code == 'nus-dsa':
        name = "Data Science & Analytics"
        school = "NUS"
        img_path = "/assets/nus_logo.png"

    if uni_code == 'nus-dse':
        name = "Data Science & Economics"
        school = "NUS"
        img_path = "/assets/nus_logo.png"

    if uni_code == 'ntu-dsa':
        name = "Data Science and Artificial Intelligence"
        school = "NTU"
        img_path = "/assets/ntu_logo.jpg"

    if uni_code == 'smu-dsa':
        name = "Data Science & Analytics (2nd Major)"
        school = "SMU"
        img_path = '/assets/smu_logo.jpg'

    return name, school, img_path

def buttonFormat(name, id, image_url, img_style=None):
    return html.Div(
        children=[
            html.Img(src=image_url, className='checkbox-image', style=img_style),
            dbc.Checkbox(id=f'checkbox_{id}', className='course--add'),
            html.Button(name, id=id, className='course--link')
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
                buttonFormat('NUS: Data Science and Analytics', 'nus-dsa', '/assets/nus_logo.png', 
                    img_style={'width': '150px', 'height': '80px', 'margin-left': '30px', 'margin-top': '30px'}),
                buttonFormat('NUS: Data Science and Economics', 'nus-dse', '/assets/nus_logo.png', 
                    img_style={'width': '150px', 'height': '80px', 'margin-left': '30px', 'margin-top': '30px'}),
                buttonFormat('NTU: Data Science and Artificial Intelligence', 'ntu-dsa', '/assets/ntu_logo.png', 
                    img_style={'width': '170px', 'height': '75px', 'margin-left': '30px', 'margin-top': '30px'}),
                buttonFormat('SMU: Data Science and Analytics (2nd Major)', 'smu-dsa', '/assets/smu_logo.png', 
                    img_style={'width': '160px', 'height': '85px', 'margin-left': '30px', 'margin-top': '20px'})
            ],
            className='course'
        ),

        html.Div(
            html.Button('Compare', id='comp', style={
                'background-color': '#F9CA84', 'border-color': '#F9CA84', 'font-size': '25px',
                'border-radius': '10px', 'margin': '0px 20px 20px 20px', 'color': '#591414', 'font-weight':'bold'
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
                if not cb_dict[key]:
                    continue
                else:
                    checkbox.append(key)
                    print(cb_dict[key])

            if len(checkbox) == 2:
                return f'/compare/course1={checkbox[0]}&course2={checkbox[1]}'

    else:
        return None
