import sqlite3
from sqlite3 import Error
from datetime import datetime
import pandas as pd
import requests
from DataBaseClass import DBConnect

filepath = "/Users/americanthinker/DataScience/Projects/fraud-detection-case-study/test.db"


if __name__ == '__main__':
    exec = DBConnect()
    r = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()
    datapoint = pd.DataFrame.from_dict(r, orient='index').T
    long_data = datapoint.drop(['ticket_types', 'previous_payouts'], axis=1)
    values = long_data.loc[0].values.tolist()
    stamp = datetime.now().timestamp()
    values.insert(0, stamp)
    exec.insert_row(filepath, values)