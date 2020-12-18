import dash
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_core_components  as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash_daq as daq
import requests
import plotly.graph_objects as go
import plotly.express as px

# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.DARKLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
                )

server = app.server

#Remove this line in production (only for testing purposes)
predicted_probability = round(np.random.uniform(), 3)

r = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()

datapoint = pd.DataFrame.from_dict(r, orient='index').T
features = datapoint.drop(['venue_latitude', 'org_desc', 'description'], axis=1)
sample_columns = features.iloc[:, 1:11]
org_name = features.loc[0,'org_name']
print(sample_columns.values)


app.layout = html.Div(id='container', children=[
    dbc.Container([
        dbc.Col(id='banner', width=12, style=dict(backgroundColor='black', textAlign='center', marginTop='20px', height='10vh'),
                children=html.Label("Company Name and Logo")),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Col(id='headline', width=12, style=dict(textAlign='center'), children=html.H3(f"Example Data Point:")),
        dbc.Col(id='headline2', width=12, style=dict(textAlign='center'), children=html.H3(f"{org_name}")),
        html.Br(),
        dbc.Col(id='data-table', width=12, children=dash_table.DataTable(
            id='table', data=sample_columns.to_dict('records'),
            columns=[{'id': c, 'name':c} for c in sample_columns.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
    },
        )),
        html.Br(),
        html.Br(),
        html.Div(id='prob-data', children=predicted_probability, style=dict(display='none')),
        html.Div(daq.Gauge(id='gauge',
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
            value=2,
            label=f'Fraud Prediction',
            max=10,
            min=0)
        )
    ])
])

@app.callback(
    Output('gauge', 'value'),
    Input('prob-data', 'children')

)
def move_needle(prob):
    prob = round(prob, 1) * 10
    print(prob)
    if prob == None:
        raise PreventUpdate
    else:
        return prob

if __name__ == '__main__':
    app.run_server(debug=True)
    print(predicted_probability)