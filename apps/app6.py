import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

layout = html.Div([
    dcc.Markdown('''
    # Basic Dash Callbacks
    We showed how the app.layout describes what the app looks like and is a hierarchical tree of components. 
    The `dash_html_components` library provides classes for all of the HTML tags, and the keyword arguments describe the HTML attributes like style, className, and id. 
    The `dash_core_components` library generates higher-level components like controls and graphs.
    Here we show Dash apps using callback functions: Python functions that are automatically called by Dash whenever an input component's property changes.
    '''),
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
