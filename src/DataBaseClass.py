import sqlite3
from sqlite3 import Error
from datetime import datetime


class DBConnect:

    def __init__(self):
        self.name = 'python_connector'

    def create_table_(self, db_file, table_command):
        """ create a database table in a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'SQLite Version: {sqlite3.version}')
            cur = conn.cursor()
            cur.execute(table_command)
            conn.commit()

        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def insert_row(self, db_file, row_command):
        """ insert a database row in a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'SQLite Version: {sqlite3.version}')
            cur = conn.cursor()
            cur.execute("insert into longform values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row_command)
            conn.commit()

        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


if __name__ == '__main__':
    exec = DBConnect()



