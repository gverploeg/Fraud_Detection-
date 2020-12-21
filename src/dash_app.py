import dash
import pandas as pd, numpy as np
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash_daq as daq
import requests
from datetime import datetime
from stephen_pipeline  import prediction, risk, ticketTypes
from DataBaseClass import DBConnect
filepath = "/Users/americanthinker/DataScience/Projects/fraud-detection-case-study/test.db"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
                )

server = app.server

#create instantiation of database connection
exec = DBConnect()
#initiate GET request to Heroku server for JSON data packet
r = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()
#create timestamp for use as Primary Key in all database tables
stamp = datetime.now().timestamp()
#using pickled ML model create prediction from data
predicted_probability = prediction(r)[0][1]

#munge data for ease of use
datapoint = pd.DataFrame.from_dict(r, orient='index').T
org_name = datapoint['org_name'][0]

# drop compound data types for use in other sqlite tables
long_data = datapoint.drop(['ticket_types', 'previous_payouts'], axis=1)

#update with Primary key and fraud predction
values = long_data.loc[0].values.tolist()
values.insert(0, stamp)
values.insert(len(values), predicted_probability)
exec.insert_row(filepath, 'longform', 43, values)

#create ticket_type frame and then insert row in ticket_table
ticket_type_cols = ['availability', 'cost', 'event_id', 'quantity_sold', 'quantity_total']
ticket_table = ticketTypes(datapoint).loc[:, ticket_type_cols]
ticket_values = ticket_table.values.tolist()[0]
ticket_values.insert(0, stamp)
exec.insert_row(filepath, 'ticket_table', len(ticket_values), ticket_values)

#create previous_payouts frame and then insert row in payouts table
previous_payout = pd.DataFrame.from_dict(datapoint['previous_payouts'][0][0], orient='index').T
payout_values = previous_payout.values.tolist()[0]
payout_values.insert(0, stamp)
exec.insert_row(filepath, 'payouts', len(payout_values), payout_values)

#create risk assessment from risk table data
risk_table_cols = ['cost', 'availability', 'quantity_total']
risk_table = ticket_table.loc[:, risk_table_cols]
risk_assess = risk(r)

app.layout = html.Div(id='container', style=dict(fontFamily='Garamond'), children=[
    dbc.Container([
        dbc.Col(id='banner', width=12, style=dict(backgroundColor='black', textAlign='center', marginTop='20px', height='8vh'),
                children=html.H2("Fraud-Busters", style=dict(verticalTextAlign='center'))),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Col(id='headline', width=12, style=dict(textAlign='center'), children=html.H3(f"Event Name:")),
        dbc.Col(id='headline2', width=12, style=dict(textAlign='center'), children=html.H3(f"{org_name}")),
        html.Br(),
        dbc.Col(id='data-table', width=dict(size=6, offset=3), children=dash_table.DataTable(
            id='table', data=risk_table.to_dict('records'),
            columns=[{'id': c, 'name':c} for c in risk_table.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
    },
        )),
        html.Br(),
        html.Br(),
        html.Div(
            dbc.Row(justify='center',
                children=[
                    dbc.Col(width=dict(size=4, offset=3), #style=dict(backgroundColor='crimson'),
                            children=
                                daq.Gauge(
                                    id='gauge',
                                    color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                                    value=0,
                                    label=f'Fraud Prediction',
                                    max=10,
                                    min=0)
                                    ),
                    dbc.Col(id='button-col', width=3, align='center',
                            children=
                                dbc.Button("Next Prediction", id='predict-button',
                                           style=dict(fontSize=28),
                                           size='lg',
                                           active=False,
                                           color='primary',

                                           block=True, ))
                        ])),
        html.Div(id='risk',
                 children=[
                        html.H3(risk_assess, style=dict(textAlign='center')),
                        dcc.Interval(
                            id='interval-component',
                            interval=1*100, # in milliseconds
                            n_intervals=0)
                        ])
        ])
])

@app.callback(
    Output('gauge', 'value'),
    Input('predict-button', 'n_clicks')
)
def move_needle(clicks):
    if clicks is None:
        raise PreventUpdate
    elif clicks > 0:
        prob = round(predicted_probability, 1) * 10
        return prob

if __name__ == '__main__':
    app.run_server(debug=True)