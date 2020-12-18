import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from stephen_pipeline import request
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report, precision_recall_curve, auc
from sklearn.ensemble import RandomForestClassifier
import pickle



pickle_off = open('bestRfModel.pkl', 'rb')
model = pickle.load(pickle_off)

# request = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()
df = pd.read_csv('data/final_features_with_Grant.csv')

# cols = ['org_name', 'venue_latitude', 'venue_longitude', 'event_published', 'user_created', 
#         'venue_name', 'currency', 'org_desc', 'event_created', 'event_start', 'payee_name', 'payout_type',
#         'sale_duration2', 'sale_duration', 'approx_payout_date', 'listed', 'gts', 'num_order', 'venue_state',
#         'event_end', 'description', 'object_id', 'country', 'venue_country', 
#         'has_analytics', 'venue_address', 'num_payouts', 'org_twitter', 'has_logo', 'name', 'show_map', 'acct_type',
#         'event_id', 'availability', 'quantity_sold', 'ticket_types']

# df["acct_type"] = df['acct_type'].replace('fraudster_event', 'fraudster')
# df["acct_type"] = df['acct_type'].replace('fraudster_att', 'fraudster')
# df['fraud'] = np.where(df['acct_type'] == 'fraudster', 1, 0)

# frame_list = []
# for x in df.ticket_types.values:
#     frame_list.append(pd.DataFrame(x))
# ticket_types = pd.concat(frame_list)
# combined_tkt = combined_tkt = ticket_types.groupby(['event_id']).agg({'cost':'mean', 'availability':'mean',                                 
#                                                     'quantity_total':'mean', 'quantity_sold':'mean'})
# event_id = []
# for idx, row in df.iterrows():
#     if len(row['ticket_types']) == 0:
#         event_id.append(0)
#     else:
#         eid = row['ticket_types'][0]['event_id']
#         event_id.append(eid)
# df['event_id'] = event_id
# df = pd.merge(df, combined_tkt, on='event_id', how='left')


# df1 = df.drop(cols, axis = 1)


# df1['yahoo'] = np.where(df1['email_domain'].str.contains('yahoo'), 1 ,0)
# df1['is_org'] = np.where(df1['email_domain'].str.contains('.org'), 1 ,0)

# df1['truth_col'] = df1['previous_payouts'].apply(lambda x: x)
# df1['prev_payouts0'] = np.where(df1['truth_col'] == 0, 1, 0)

# df1['has_header_1.0'] = np.where(df1['has_header'] == 1.0, 1, 0)
# df1['org_facebook'] = df1['org_facebook'].fillna(0)

# df1['del_method_3.0'] = np.where(df1['delivery_method'] == 3.0, 1, 0)



# df1 = df1.drop(['email_domain', 'truth_col', 'has_header', 'previous_payouts', 'delivery_method', 'cost', 'quantity_total'], axis = 1)

# labels = np.array(df1['fraud'])
# features = np.array(df1.drop('fraud', axis = 1))

# Random Forest with Reduced Features
# df1_train, df1_test = train_test_split(df1, random_state=42, stratify=df1.fraud)
# Non_fraud = df1_train[(df1_train['fraud'] == 0)]
# Fraud = df1_train[(df1_train['fraud'] == 1)]
# Non_fraud_samp = Non_fraud.sample(n=len(Fraud))
# df1_train_ = pd.concat([Fraud, Non_fraud_samp], axis=0)
# X_train = df1_train_[['body_length', 'channels', 'fb_published', 'name_length',
#        'org_facebook', 'user_age', 'user_type',
#                 'prev_payouts0', 'has_header_1.0',
#         'yahoo', 'is_org',
#         'del_method_3.0']]
# y_train = df1_train_['fraud'].values
# X_test = df1_test[['body_length', 'channels', 'fb_published', 'name_length',
#        'org_facebook', 'user_age', 'user_type',
#                 'prev_payouts0', 'has_header_1.0',
#         'yahoo', 'is_org',
#         'del_method_3.0']]
# y_test = df1_test['fraud'].values
# fr_classify = RandomForestClassifier(bootstrap=False, max_depth=100, max_features='sqrt',
#                        n_estimators=500, n_jobs=-1, verbose=1)
# fr_classify.fit(X_train, y_train)
# y_pred = fr_classify.predict(X_test)



if __name__ == '__main__':
    
    print(df.columns)