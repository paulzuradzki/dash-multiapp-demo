# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div(
    [
        dcc.Markdown('''
        ### Dash App with State
        In some cases, you might have a "form"-type pattern in your application. 
        In such a situation, you might want to read the value of the input component, but only when the user is finished entering all of his or her information in the form.
        In this example, the callback function is fired whenever any of the attributes described by the dash Input change.
        '''),
        dcc.Input(id="input-1", type="text", value="Montréal"),
        dcc.Input(id="input-2", type="text", value="Canada"),
        html.Div(id="number-output"),
        dcc.Link('Go back to home', href='/'),    
    ]
)


@app.callback(
    Output("number-output", "children"),
    Input("input-1", "value"),
    Input("input-2", "value"),
)
def update_output(input1, input2):
    return u'Input 1 is "{}" and Input 2 is "{}"'.format(input1, input2)

