# app.py
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

# Serve styles.css as an external file
app.css.append_css({"external_url": "/assets/app.css"})

# Top header
header = html.Div(
    className='header',
    children=[
        dcc.Link(
            id="header",
            children=[
                html.Img(src='/assets/logo.png', className="logo")
            ],
            href='/'
        )
    ]
)

search_bar = html.Div(
    children=[
        dcc.Location(id='search_nav'),
        html.Div(
            children=[
                html.Img(src='/assets/glass_logo.png', className='magnifying-glass-icon'),
                dcc.Input(
                    id='search',
                    type='text',
                    placeholder='Search Concepts, Modules here...',
                    size='70',
                ),
            ],
            id='search-bar-container'
        ),
    ]
)

app.layout = html.Div(
    [
        header,
        search_bar,
        dash.page_container
    ]
)

@app.callback(
    Output("search_nav", "pathname"),
    [Input("search", "value"), Input("search", "n_submit")],
    prevent_initial_call=True
)
def searchFunction(query, submit):
    if submit == 1:
        return f'/search={query}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
