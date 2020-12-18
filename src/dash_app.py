import dash
import pandas as pd, numpy as np
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash_daq as daq
import requests
from datetime import datetime
from stephen_pipeline  import prediction
from DataBaseClass import DBConnect
filepath = "/Users/americanthinker/DataScience/Projects/fraud-detection-case-study/test.db"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
                )

server = app.server

exec = DBConnect()
r = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()
stamp = datetime.now().timestamp()
predicted_probability = prediction(r)[0][1]

#testcase
print(predicted_probability)
print(stamp)

#munge data for db insertion
datapoint = pd.DataFrame.from_dict(r, orient='index').T
# drop compound data types for use in other sqlite tables
long_data = datapoint.drop(['ticket_types', 'previous_payouts'], axis=1)

#update with Primary key and fraud predction
values = long_data.loc[0].values.tolist()
values.insert(0, stamp)
values.insert(len(values), predicted_probability)

#insert update
exec.insert_row(filepath, values)

datapoint = pd.DataFrame.from_dict(r, orient='index').T
features = datapoint.drop(['venue_latitude', 'org_desc', 'description'], axis=1)
sample_columns = features.iloc[:, 1:11]
org_name = features.loc[0,'org_name']
print(sample_columns.values)


app.layout = html.Div(id='container', style=dict(fontFamily='Garamond'), children=[
    dbc.Container([
        dbc.Col(id='banner', width=12, style=dict(backgroundColor='black', textAlign='center', marginTop='20px', height='8vh'),
                children=html.H2("Fraud-Busters", style=dict(verticalTextAlign='center'))),
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
