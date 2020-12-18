import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df_ex = pd.read_json('example.json')

df = pd.read_json('data/data.json')

df["acct_type"] = df['acct_type'].replace('fraudster_event', 'fraudster')
df["acct_type"] = df['acct_type'].replace('fraudster_att', 'fraudster')

cols = ['acct_type', 'approx_payout_date', 'description', 
        'gts', 'has_analytics', 'listed', 'num_order', 'name',
        'payee_name', 'payout_type', 'sale_duration', 'sale_duration2',
        'org_name', 'user_type', 'venue_name', 'venue_address', 
        'currency', 'org_desc', 'country']

df1 = df.drop(cols, axis = 1)

<<<<<<< HEAD

df1['fraud'] = np.where(df['acct_type'] == 'fraudster', 1, 0)
df1['']

<<<<<<< HEAD
<<<<<<< HEAD


df1 = df1.drop(['email_domain', 'truth_col', 'has_header', 'previous_payouts', 'name'], axis = 1)


if __name__ == '__main__':
    for column in df1.columns:
        print(df1[column].head())
=======


if __name__ == '__main__':
    print(df1.info())
>>>>>>> parent of 46647a8... added my own stuff to work on chris
=======
df1 = df1.drop(['email_domain', 'truth_col', 'has_header', 'previous_payouts'], axis = 1)


if __name__ == '__main__':
    print(df1..head())
>>>>>>> parent of 8ea3153... last changes
=======

df1['fraud'] = np.where(df['acct_type'] == 'fraudster', 1, 0)
df1['']



if __name__ == '__main__':
    print(df1.info())
>>>>>>> parent of 46647a8... added my own stuff to work on chris
