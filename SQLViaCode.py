from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

def get_query_from_db(query):

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")
    try:
        engine = create_engine(f"mssql+pyodbc://{user}:{password}@{host}/{dbname}?driver={driver}")
        with engine.connect() as conn:
            print("Connected to DB")
    except Exception as e:
        print("Error: Could not connect to the database. Please check if the username, password, host, or database name are correct.")
        print("Error details:", e)
        return None

    try:
        with engine.connect() as conn:
            output_query = conn.execute(text(query))
            rows = output_query.fetchall()
            columns_name = list(output_query.keys())
        return pd.DataFrame(rows, columns=columns_name)
    except Exception as e:
        print("Error executing query")
        print("Error details:", e)
        return None