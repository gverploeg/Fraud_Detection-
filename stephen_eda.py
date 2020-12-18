import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_json('example.json')

cols = ['org_name', 'venue_latitude', 'venue_longitude', 'event_published', 'user_created', 
        'venue_name', 'currency', 'org_desc', 'event_created', 'event_start', 'payee_name', 'payout_type',
        'sale_duration2', 'sale_duration', 'approx_payout_date', 'listed', 'gts', 'num_order', 'venue_state',
        'event_end', 'description', 'object_id', 'country', 'venue_country', 
        'has_analytics', 'venue_address', 'num_payouts']




df1 = df.drop(cols, axis = 1)

df1['yahoo'] = np.where(df1['email_domain'].str.contains('yahoo'), 1 ,0)
df1['is_fr'] = np.where(df1['email_domain'].str.contains('fr'), 1 ,0)
df1['is_org'] = np.where(df1['email_domain'].str.contains('.org'), 1 ,0)

df1['truth_col'] = df1['previous_payouts'].apply(lambda x: x)
df1['prev_payouts0'] = np.where(df1['truth_col'] == 0, 1, 0)

df1['has_header_0.0'] = np.where(df1['has_header'] == 0.0, 1, 0)
df1['has_header_1.0'] = np.where(df1['has_header'] == 1.0, 1, 0)
df1['has_header_NaN'] = np.where(df1['has_header'].isnull() == True, 1, 0)

df1['del_method_0.0'] = np.where(df1['delivery_method'] == 0.0, 1, 0)
df1['del_method_1.0'] = np.where(df1['delivery_method'] == 1.0, 1, 0)
df1['del_metho_NaN'] = np.where(df1['delivery_method'].isnull() == True, 1, 0)
df1['del_method_3.0'] = np.where(df1['delivery_method'] == 3.0, 1, 0)

df1 = df1.drop(['email_domain', 'truth_col', 'has_header', 'previous_payouts'], axis = 1)


if __name__ == '__main__':
    print(df1..head())