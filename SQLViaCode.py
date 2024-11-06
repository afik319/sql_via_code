from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

def query_db(query):

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")

    engine = create_engine(f"mssql+pyodbc://{user}:{password}@{host}/{dbname}?driver={driver}")

    print("Connected to DB")
    with engine.connect() as conn:
        output_query = conn.execute(text(query))
        rows = output_query.fetchall()
        columns_name = list(output_query.keys())
    return pd.DataFrame(rows, columns=columns_name)

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
query = "SELECT * FROM CoopApartmentBorrowers cab"
result_df = query_db(query)
print(result_df)
