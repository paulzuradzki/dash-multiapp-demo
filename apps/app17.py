import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import seaborn as sns

df = sns.load_dataset('titanic')

layout = html.Div([
    dcc.Markdown('''
    # DataTable - Height
    ### Basic
    Dataset: 
    ```python
    import seaborn as sns    
    df = sns.load_dataset('titanic')
    ```  
    
    '''),
    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.head().to_dict('records'),),
    html.Br(),

    dcc.Markdown('### Setting Table Height with Pagination'),
    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        page_size=10),
    html.Br(),

    dcc.Markdown('### Setting Table Height with Vertical Scroll'),
    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        page_action='none',
                        style_table={'height': '300px', 'overflowY': 'auto'}),
    html.Br(),

    dcc.Markdown('### Vertical Scroll With Pagination'),
    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        page_size=20,  # we have less data in this example, so setting to 20
                        style_table={'height': '300px', 'overflowY': 'auto'}),
    html.Br(),

    dcc.Markdown('''
    ### Vertical Scroll With Fixed Headers (a.k.a. Freeze Panes) and Fixing Column Width
    '''),
    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        fixed_rows={'headers': True},
                        style_table={'height': 400},  # defaults to 500
                        style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95}
                        ),
    html.Br(),

    dcc.Markdown('''
    ### Vertical Scroll with Virtualization
    The browser has difficulty rendering thousands of rows in a table.
    By rendering rows on the fly as you scroll, virtualization works around rendering performance issues inherent with the web browser.
    All of the data for your table will still be sent over the network to the browser, so if you are displaying more than 10,000-100,000 rows you may consider using backend pagination to reduce the volume of data that is transferred over the network and associated memory usage.
    '''),
    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        virtualization=True,
                        fixed_rows={'headers': True},
                        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
                        style_table={'height': 300}),  # default is 500
    html.Br(),

])

