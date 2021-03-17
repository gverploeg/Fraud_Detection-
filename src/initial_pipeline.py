import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import pickle

pickle_off = open('bestRfModel.pkl', 'rb')
model = pickle.load(pickle_off)
request = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()
cols = ['org_name', 'venue_latitude', 'venue_longitude', 'event_published', 'user_created', 
        'venue_name', 'currency', 'org_desc', 'event_created', 'event_start', 'payee_name', 'payout_type',
        'sale_duration2', 'sale_duration', 'approx_payout_date', 'listed', 'gts', 'num_order', 'venue_state',
        'event_end', 'description', 'object_id', 'country', 'venue_country', 
        'has_analytics', 'venue_address', 'num_payouts', 'name', 'event_id',
        'quantity_sold', 'ticket_types']

def loadData(request):
    datapoint = pd.DataFrame.from_dict(request, orient='index').T
    return datapoint

def ticketTypes(df):
    frame_list = []
    for x in df.ticket_types.values:
        frame_list.append(pd.DataFrame(x))
    ticket_types = pd.concat(frame_list)
    combined_tkt = ticket_types.groupby(['event_id']).agg({'cost':'mean', 'availability':'mean',
                                                        'quantity_total':'mean', 'quantity_sold':'mean'})
    event_id = []
    for idx, row in df.iterrows():
        if len(row['ticket_types']) == 0:
            event_id.append(0)
        else:
            eid = row['ticket_types'][0]['event_id']
            event_id.append(eid)
    df['event_id'] = event_id
    df = pd.merge(df, combined_tkt, on='event_id', how='left')
    return df

def dropCol(datapoint, cols):
    return datapoint.drop(cols, axis = 1 )

def createDummies(df):
    df['yahoo'] = np.where(df['email_domain'].str.contains('yahoo'), 1 ,0)
    df['is_org'] = np.where(df['email_domain'].str.contains('.org'), 1 ,0)
    df['is_fr'] = np.where(df['email_domain'].str.contains('.fr'), 1 ,0)
    df['truth_col'] = df['previous_payouts'].apply(lambda x: x)
    df['prev_payouts0'] = np.where(df['truth_col'] == 0, 1, 0)
    df['has_header_1.0'] = np.where(df['has_header'] == 1.0, 1, 0)
    df['has_header_0.0'] = np.where(df['has_header'] == 0.0, 1, 0)
    df['has_header_NaN'] = np.where(df['has_header'].isnull == True, 1, 0)
    df['del_method_3.0'] = np.where(df['delivery_method'] == 3.0, 1, 0)
    df['del_method_1.0'] = np.where(df['delivery_method'] == 1.0, 1, 0)
    df['del_method_0.0'] = np.where(df['delivery_method'] == 1.0, 1, 0)
    df['del_method_NaN'] = np.where(df['delivery_method'].isnull == True, 1, 0)
    df = df.drop(['email_domain', 'truth_col', 'has_header', 'previous_payouts', 'delivery_method'], axis = 1)
    return df

def modelData(request):
    datapoint = pd.DataFrame.from_dict(request, orient='index').T
    datapoint = ticketTypes(datapoint)
    datapoint = dropCol(datapoint, cols)
    datapoint = createDummies(datapoint)
    return datapoint

def prediction(request):
    df = modelData(request)
    return model.predict_proba(df.values)

def risk_table_short(request):
    df = modelData(request)
    short_df = df.loc[:, 'cost':'quantity_total']
    return short_df

def risk(request):
    df = modelData(request)
    if df.cost.values[0] <= 25:
        return('Low Risk')
    elif df.cost.values[0] >= 25.01 and df.cost.values[0] < 100:
        return('Medium Risk')
    else:
        return('High Risk')

if __name__ == '__main__':
    print(modelData(request).cost.values)
    print(risk(request))

