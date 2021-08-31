import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app0, app1, app2, app3, app4, app5, app6, app7, app8, app9, app10 \
                ,app11, app12, app13, app14, app15, app17
from apps.app16 import quality_measures

server = app.server

# the following code is repetitive in case we decide to implement a different URL pattern (ex: app IDs don't have to be numbered)
index_page = html.Div([
    dcc.Markdown('''
    ### Home - Dash Proof of Concept

    [App 0](/apps/app0)  
    [App 1](/apps/app1)  
    [App 2](/apps/app2)  
    [App 3](/apps/app3)  
    [App 4](/apps/app4)  
    [App 5](/apps/app5)  
    [App 6](/apps/app6)  
    [App 7](/apps/app7)  
    [App 8](/apps/app8)  
    [App 9](/apps/app9)  
    [App 10](/apps/app10)  
    [App 11](/apps/app11)  
    [App 12](/apps/app12)  
    [App 13](/apps/app13)      
    [App 14](/apps/app14)  
    [App 15](/apps/app15)  
    [App 16 - Quality Measures](/apps/app16/quality_measures)  
    [App 17](/apps/app17)  
    '''),
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
               '/apps/app16/quality_measures': quality_measures.layout,
               '/apps/app17': app17.layout,
               }

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    try:
        return path_lookup[pathname]
    except KeyError:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=False, host='localhost', port=8000)