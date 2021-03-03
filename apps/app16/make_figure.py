import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def _pivot_plot_data(df=None, column=None):
    """Helper function to convert single numeric column with groupings to pivoted/wide format that is more suitable for Plotly.
    """
    pivoted = pd.pivot_table(data=df,\
                   index=['run_month'], columns=['measure_name'], values=[column]).reset_index()
    pivoted.columns = ['_'.join(col).rstrip('_') for col in pivoted.columns.values]
    renamed_cols = dict([(col, col.split('_')[-1]) for col in pivoted.columns if col!='run_month'])
    pivoted = pivoted.rename(columns=renamed_cols)
    pivoted = pivoted.set_index('run_month')
    return pivoted

# data processing
measure_data = pd.read_csv(r'apps/app16/plan_report.csv')
measure_data['run_month'] = measure_data['run_date'].astype(str)
measure_data = measure_data.query("pipeline_name.str.contains('Lag Run HEDIS 2020')")

measure_data['close_rate'] = measure_data['numerator'] / measure_data['denominator']
measure_data['closed_gaps'] = measure_data['numerator']
measure_data['open_gaps'] = measure_data['denominator'] - measure_data['numerator']

# The following dataframes look pivoted like this in order to work with Plotly dropdown. Each measure gets a column with the metric as a value (ex: open gaps, closed gaps, compliance rate)
    # | run_month   |   HEDIS 2020: Adherence to Antipsychotic Medications for Individuals With Schizophrenia |   HEDIS 2020: Adolescent Well-Care Visits |   HEDIS 2020: Adult Access to Preventive or Ambulatory Health Services |   HEDIS 2020: Adult BMI Assessment |   ....                                                    |
    # |:------------|----------------------------------------------------------------------------------------:|------------------------------------------:|-----------------------------------------------------------------------:|-----------------------------------:|----------------------------------------------------------:|
    # | 2020-04-19  |                                                                                      38 |                                         7 |                                                                   1581 |                               1348 |                                                        54 |
    # | 2020-05-09  |                                                                                      62 |                                         7 |                                                                    930 |                               1318 |                                                        59 |
    # | 2020-06-09  |                                                                                      66 |                                         7 |                                                                    862 |                               1312 |                                                        57 |
    # | 2020-07-09  |                                                                                      81 |                                         6 |                                                                    664 |                               1290 |                                                        56 |
    # | 2020-08-13  |                                                                                      81 |                                         6 |                                                                    620 |                               1286 |                                                        56 |
    
open_gaps = _pivot_plot_data(df=measure_data, column='open_gaps')
closed_gaps = _pivot_plot_data(df=measure_data, column='closed_gaps')
rates = _pivot_plot_data(df=measure_data, column='close_rate')

open_gaps = _pivot_plot_data(df=measure_data, column='open_gaps')
closed_gaps = _pivot_plot_data(df=measure_data, column='closed_gaps')
rates = _pivot_plot_data(df=measure_data, column='close_rate')

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(name='Close Rate',
                        x=rates.index,
                        y=rates[rates.columns[0]],
                        visible=True,
                        line={'color': '#F36F25'}),
            secondary_y=True
            )

fig.add_trace(go.Bar(name='Closed', 
                    x=rates.index, 
                    y=closed_gaps[closed_gaps.columns[0]])
            )

fig.add_trace(go.Bar(name='Open', 
                    x=rates.index, 
                    y=open_gaps[open_gaps.columns[0]])
            )

updatemenu = []
buttons = []

# button with one option for each dataframe
# _df can be any of the 3 tables as long as they have the same column names
# references:
    # https://plotly.com/javascript/plotlyjs-function-reference/#plotlyrestyle
    # https://stackoverflow.com/questions/61898599/plotly-how-to-update-figure-with-multiple-dependent-traces-using-updatemenus

_df = rates
for col in _df.columns:
    buttons.append(dict(method='restyle',
                        label=col.replace('HEDIS 2020: ', ''),
                        visible=True,
                        args=[{'y':[_df[col], closed_gaps[col], open_gaps[col]],
                            'x':[_df.index],
                            'type': ['scatter', 'bar', 'bar']},[0,1,2]                             ]
                        )
                )

# some adjustments to the updatemenus
updatemenu = []
your_menu = dict()
updatemenu.append(your_menu)
updatemenu[0]['buttons'] = buttons
updatemenu[0]['direction'] = 'down'
updatemenu[0]['showactive'] = True
updatemenu[0]['x'] = 2
updatemenu[0]['y'] = 1.18

# FORMATTING
fig.update_layout(title='HEDIS 2020 Monthly Care Gap Closures',
                xaxis_title='Rules Run Year Month',
                yaxis_title='Open/Closed Care Gaps',
                yaxis2_title='Close Rate %',
                colorway=['#23BDC3', '#555559'], # custom colors: turquoise, grey 
                barmode='stack',
                xaxis_tickangle=-45,
                xaxis_ticktext=rates.index,
                width=1000,
                height=400,
                autosize=True,
                margin=dict(t=100, b=0, l=0, r=0),
                updatemenus=updatemenu
                )