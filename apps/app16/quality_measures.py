import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import apps.app16.make_figure as make_figure
from app import app

layout = html.Div([
    dcc.Markdown('''
    ### Plotly Dropdown Demo
    #### HEDIS Quality Measures
    
    This chart is built using Plotly and Plotly [dropdowns](https://plotly.com/python/dropdowns/) to update the layout. 
    Alternatively, we could use the [dash.core_component.Dropdown](https://dash.plotly.com/dash-core-components/dropdown) component which is a distinct from Plotly dropdowns/buttons.
    Dash builds on top of Plotly while also offering interactive "Dash core components" for web apps.

    *Mock data*
    '''),
    html.Div(id='page-0-content'),
    dcc.Graph(figure=make_figure.fig),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    ])