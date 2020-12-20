import sqlite3
from sqlite3 import Error

class DBConnect:

    def __init__(self):
        self.name = 'python_connector'

    def create_table_(self, db_file, table_name, table_schema):
        """
        **Create a database table in a SQLite database**
        db_file --> str, filepath to db
        table_name --> str, name of newly created table
        table_schema --> str, predefined table schema
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'SQLite Version: {sqlite3.version}')
            cur = conn.cursor()
            cur.execute("create table if not exists" + " " + table_name + " " + table_schema)
            conn.commit()

        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def insert_row(self, db_file, table_name, num_cols, values):
        """
        ** Insert a row of values into a SQLite database **
        db_file --> str, filepath to db
        table_name --> str, name of table for insertion
        num_cols --> int, number of columns
        values --> list, list of values
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'SQLite Version: {sqlite3.version}')
            cur = conn.cursor()
            cur.execute("insert into" + " " + table_name + " values (" + "?," * (num_cols - 1) + "?)", values)
            conn.commit()

        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()



