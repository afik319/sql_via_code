from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
from os import getenv as env
import pandas as pd

# Load environment variables from a .env file
load_dotenv()

def get_query_from_db(query , table_to_backup):
    try:
        # Create a connection to the database
        engine = create_engine(f"mssql+pyodbc://{env('USER')}:{env('PASSWORD')}@{env('HOST')}/{env('NAME')}?driver={env('DRIVER')}")
        with engine.connect() as conn:
            print("Connected to DB")
            backup_table(table_to_backup , conn) # Optional table backup
            output_query = conn.execute(text(query))
            rows = output_query.fetchall()
            columns_name = list(output_query.keys())
            return pd.DataFrame(rows, columns=columns_name)
    except Exception as e:
        raise Exception(f"Error: Could not connect to the database or execute query.\nError details: {e}")

def backup_table(table_to_backup , conn):
    if table_to_backup == "":
        raise ValueError("Parameter 'table_to_backup' cannot be an empty string.")
    if table_to_backup is None:
        print("No backup will be performed as 'table_to_backup' is set to None.")
    else:
        backup_query = f"SELECT * FROM {table_to_backup}"
        backup_df = pd.read_sql_query(backup_query, conn)
        backup_filename = f"{table_to_backup}_backup_{datetime.now().strftime('%d.%m.%Y_%H_%M_%S')}.csv"
        backup_df.to_csv(backup_filename, index=False)
        print(f"Table '{table_to_backup}' backed up successfully as {backup_filename}")