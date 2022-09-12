import sqlite3
import pandas as pd


class database_conn:
    
    def __init__(self) -> None:
        pass
    

    def create_connection(self, db_file):
        """ Function that create a database connection to the SQLite database specified by db_file
        Args:
            db_file: database file
        Return:
            conn: connection object
        """
        conn = None

        try:
            conn = sqlite3.connect(db_file)
            return conn
        
        except:
            print('Please check database file name')

        return conn


    def get_data(self, conn, table):
        """ Function that connects to a SQLite database and extracts data from a specified table
        Args:
            conn: connection object
            table -> str: table name as a string
        Return:
            data: dataframe
        """       
        try:
            data = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            
        except:
            print('Please check if table exists.')

        return data


    def load_data(self, conn, data, table_name):
        """ Function that writes cleaned data to a table in SQLite database
        Args:
            conn: connection object
            data -> str: clean data
        Return:
            None: Only print successful load into table
        """
        try:
            data.to_sql(name = table_name, con = conn, if_exists='replace', index=False)
            print(f'Data loaded successfully to {table_name} table')

        except:
            print('Please check connection to database')




