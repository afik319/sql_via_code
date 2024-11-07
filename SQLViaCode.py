from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import os

load_dotenv() # Load environment variables from a .env file

def get_query_from_db(query , table_to_backup):

    if table_to_backup == "":
        raise ValueError("Parameter 'table_to_backup' cannot be an empty string.")
    if table_to_backup is None:
        print("No backup will be performed as 'table_to_backup' is set to None.")

    # Retrieve database connection details from environment variables
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")
    try:
        # Create a connection to the database
        engine = create_engine(f"mssql+pyodbc://{user}:{password}@{host}/{dbname}?driver={driver}")
        with engine.connect() as conn:
            print("Connected to DB")

            # Perform backup if table_to_backup is specified
            if not table_to_backup is None:
                backup_query = f"SELECT * FROM {table_to_backup}"
                backup_df = pd.read_sql_query(backup_query, conn)
                backup_filename = f"{table_to_backup}_backup_{datetime.now().strftime('%d.%m.%Y_%H_%M_%S')}.csv"
                backup_df.to_csv(backup_filename, index=False)
                print(f"Table '{table_to_backup}' backed up successfully as {backup_filename}")

            # Execute the main query and fetch results
            output_query = conn.execute(text(query))
            rows = output_query.fetchall()
            columns_name = list(output_query.keys())
            df = pd.DataFrame(rows, columns=columns_name)
            return df

    except Exception as e:
        raise Exception(f"Error: Could not connect to the database or execute query.\nError details: {e}")