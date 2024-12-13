from .engine_manager import EngineManager
from .logger_config import logger
from datetime import datetime
from sqlalchemy import text
import pandas as pd
import sqlalchemy
import aiofiles
import inspect
import asyncio
import os

engine_manager = EngineManager()

"""
    Converts SQLAlchemy query results into a pandas DataFrame.

    Args:
        query_output (ResultProxy): SQLAlchemy query output.

    Returns:
        pd.DataFrame: DataFrame containing the query results.
    """
async def format_to_df(query_output):
    try:
        # Handle fetchall() for async or sync databases
        if inspect.iscoroutinefunction(query_output.fetchall):
            rows = await query_output.fetchall()
        else:
            rows = query_output.fetchall()

        # Handle keys() for async or sync databases
        if inspect.iscoroutinefunction(query_output.keys):
            columns_name = await query_output.keys()
        else:
            columns_name = query_output.keys()

        # Return DataFrame
        return pd.DataFrame(rows, columns=columns_name)

    except Exception as e:
        logger.error(f"Error converting query output to DataFrame: {e}")
        raise

"""Executes a SQL query and optionally backs up a specified table.

Args:
    query (str): The SQL query string to execute.
    table_to_backup (str or None): The name of the table to back up. Pass `None` to skip backup.
    env_file_name (str, optional): Path to the `.env` file with database credentials. Defaults to `None`.
    params (dict, optional): Parameters to pass to the query.

Returns:
    pd.DataFrame: DataFrame containing the query results.

Raises:
    ValueError: If a database error occurs during query execution.
"""
async def get_query_from_db(query , table_to_backup , env_file_name = None , params = None):
    conn = None
    try:
        conn = await engine_manager.connect_db(env_file_name)
        await backup_table(table_to_backup, conn)
        query_output = await conn.execute(text(query) , params)
        return await format_to_df(query_output)
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"Failed to execute query:\n{e}")
        raise ValueError("An error occurred while executing the query. Please check your query syntax or database connection.") from e
    finally:
        if conn:
            await conn.close()

"""Executes a stored procedure and optionally backs up a specified table.

Args:
    procedure_name (str): The name of the stored procedure to execute.
    table_to_backup (str or None): The name of the table to back up. Pass `None` to skip backup.
    env_file_name (str, optional): Path to the `.env` file with database credentials. Defaults to `None`.
    params (dict, optional): Parameters to pass to the stored procedure.

Returns:
    pd.DataFrame: DataFrame containing the procedure's output.

Raises:
    ValueError: If a database error occurs during procedure execution.
"""
async def exec_procedure_from_db(procedure_name , table_to_backup , env_file_name = None , params = None):
    conn = None
    try:
        conn = await engine_manager.connect_db(env_file_name)
        await backup_table(table_to_backup, conn)
        params_string = build_procedure_param_string(params)
        procedure_output = await conn.execute(text(f"EXEC {procedure_name} {params_string}"), params)
        return await format_to_df(procedure_output)
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"Failed to execute procedure:\n{e}")
        raise ValueError("An error occurred while executing the procedure. Please check your procedure syntax or database connection.") from e
    finally:
        if conn:
            await conn.close()

"""Builds a formatted string for stored procedure parameters.

Args:
    params (dict): Dictionary containing parameter keys and values.

Returns:
    str: A formatted string for procedure parameters.
"""

def build_procedure_param_string(params):
    if not params: # No parameters to process
        return ""
    return ", ".join([f"@{key} = :{key}" for key in params.keys()]) # Build the parameter string


"""Backs up a table's data to a Markdown file.

Args:
    table_to_backup (str or None): The name of the table to back up. Pass `None` to skip backup.
    conn (AsyncConnection): An active database connection.

Raises:
    ValueError: If `table_to_backup` is an empty string.
    Exception: If an error occurs during the backup process.
"""
async def backup_table(table_to_backup , conn):
    if table_to_backup == "":
        raise ValueError("Parameter 'table_to_backup' cannot be an empty string.")
    if table_to_backup is None:
        logger.info("No backup will be performed as 'table_to_backup' is set to None.")
    else:
        backup_dir_name = "tables_backup"
        os.makedirs(backup_dir_name, exist_ok=True)

        backup_query = f"SELECT * FROM {table_to_backup}"
        result = await conn.execute(text(backup_query))
        rows, columns = await asyncio.gather(
            result.fetchall(),
            result.keys()
        )
        backup_df = pd.DataFrame(rows, columns=columns)
        backup_filename = os.path.join(backup_dir_name, f"{table_to_backup}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md")

        try:
            async with aiofiles.open(backup_filename, 'w') as file:
                await file.write(backup_df.to_markdown(index=False))
            logger.info(f"Table '{table_to_backup}' backed up successfully as {backup_filename}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise

"""Reads an SQL query from a file.

Args:
    file_path (str): Path to the file containing the SQL query.

Returns:
    str: The content of the file as a query string.

Raises:
    FileNotFoundError: If the file does not exist.
    ValueError: If the file is empty.
    IOError: If there is an issue reading the file.
"""
def get_query_from_file (file_path: str) -> str:
    """
    Reads an SQL query from a file.

    Args:
        file_path (str): Path to the file containing the SQL query.

    Returns:
        str: The content of the file as a query string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an issue reading the file.
    """
    if not os.path.exists(file_path):
        error_message = f"File '{file_path}' not found."
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            query = file.read().strip()
            if not query:
                error_message = f"The file '{file_path}' is empty."
                logger.error(error_message)
                raise ValueError(error_message)
            return query
    except ValueError:  # Handle explicit empty file exception
        raise
    except Exception as e:
        logger.error(f"Failed to read query from file '{file_path}': {e}")
        raise IOError(f"Failed to read query from file '{file_path}': {e}")



