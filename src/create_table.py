import sqlite3
from sqlite3 import Error
from datetime import datetime
import pandas as pd
import requests
from DataBaseClass import DBConnect

filepath = "/Users/americanthinker/DataScience/Projects/fraud-detection-case-study/test.db"

table_schema_main = "(id real,\
                 approx_payout_date real,\
                 body_length integer,\
                 channels integer,\
                 country text,\
                 currency text,\
                 delivery_method real,\
                 description text,\
                 email_domain text,\
                 event_created integer,\
                 event_end integer,\
                 event_published integer,\
                 event_start integer,\
                 fb_published real,\
                 gts real,\
                 has_analytics real,\
                 has_header real,\
                 has_logo real,\
                 listed text,\
                 name text,\
                 name_length integer,\
                 num_order integer,\
                 num_payouts integer,\
                 object_id integer,\
                 org_desc text,\
                 org_facebook real,\
                 org_name text,\
                 org_twitter real,\
                 payee_name text,\
                 payout_type text,\
                 sale_duration real,\
                 sale_duration2 real,\
                 show_map integer,\
                 user_age integer,\
                 user_created integer,\
                 user_type integer,\
                 venue_address text,\
                 venue_country text,\
                 venue_latitude text,\
                 venue_longitude text,\
                 venue_name text,\
                 venue_state text,\
                 fraud_prediction real)"

table_schema_tickets = "(id real,\
                         availability integer,\
                         cost real,\
                         event_id integer,\
                         quantity_sold integer,\
                         quantity_total integer)"

table_schema_payouts = "(id real primary key,\
                         address text,\
                         amount real,\
                         country text,\
                         created date,\
                         event integer,\
                         name text,\
                         state text,\
                         uid integer,\
                         zip_code integer)"

if __name__ == '__main__':
    exec = DBConnect()
    exec.create_table_(filepath, 'longform', table_schema_main)
    exec.create_table_(filepath, 'ticket_table', table_schema_tickets)
    exec.create_table_(filepath, 'payouts', table_schema_payouts)
