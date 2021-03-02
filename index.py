import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app0, app1, app2, app3, app4, app5, app6, app7, app8, app9, app10, app11, app12, app13, app14, app15

# the following code is repetitive in case we decide to implement a different URL pattern (ex: app IDs don't have to be numbered)
index_page = html.Div([
    html.H3('Home'),
    dcc.Link('App 0', href='/apps/app0'),
    html.Br(),
    dcc.Link('App 1', href='/apps/app1'),
    html.Br(),
    dcc.Link('App 2', href='/apps/app2'),
    html.Br(),
    dcc.Link('App 3', href='/apps/app3'),
    html.Br(),
    dcc.Link('App 4', href='/apps/app4'),
    html.Br(),
    dcc.Link('App 5', href='/apps/app5'),
    html.Br(),
    dcc.Link('App 6', href='/apps/app6'),
    html.Br(),
    dcc.Link('App 7', href='/apps/app7'),
    html.Br(),
    dcc.Link('App 8', href='/apps/app8'),
    html.Br(),
    dcc.Link('App 9', href='/apps/app9'),
    html.Br(),
    dcc.Link('App 10', href='/apps/app10'),
    html.Br(),
    dcc.Link('App 11', href='/apps/app11'),
    html.Br(),
    dcc.Link('App 12', href='/apps/app12'),
    html.Br(),
    dcc.Link('App 13', href='/apps/app13'),
    html.Br(),
    dcc.Link('App 14', href='/apps/app14'),
    html.Br(),
    dcc.Link('App 15', href='/apps/app15'),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

path_lookup = {'/apps/app0': app0.layout,
               '/apps/app1': app1.layout,
               '/apps/app2': app2.layout,
               '/apps/app3': app3.layout,
               '/apps/app4': app4.layout,
               '/apps/app5': app5.layout,
               '/apps/app6': app6.layout,
               '/apps/app7': app7.layout,
               '/apps/app8': app8.layout,
               '/apps/app9': app9.layout,
               '/apps/app10': app10.layout,
               '/apps/app11': app11.layout,
               '/apps/app12': app12.layout,
               '/apps/app13': app13.layout,
               '/apps/app14': app14.layout,
               '/apps/app15': app15.layout,
               }

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    try:
        return path_lookup[pathname]
    except KeyError:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)