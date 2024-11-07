
# Database Query and Backup Script

This Python script provides a function, `get_query_from_db`, that connects to a SQL Server database, executes a specified SQL query, and optionally creates a backup of a specified table. The connection details are retrieved from environment variables specified in a `.env` file.

## Prerequisites

- Python 3.x
- Required Python packages (install via pip):
  ```bash
  pip install sqlalchemy pandas python-dotenv pyodbc
  ```

## Environment Variables

To use this script, you need to create a `.env` file in the same directory as the script and define the following environment variables:

```env
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_DRIVER=ODBC+Driver+17+for+SQL+Server
```

- **DB_USER**: Database username
- **DB_PASSWORD**: Database password
- **DB_HOST**: Host address of the database
- **DB_NAME**: Name of the database
- **DB_DRIVER**: ODBC driver for SQL Server (use "ODBC Driver 17 for SQL Server" for standard SQL Server connections)

## Function Details

### `get_query_from_db(query, table_to_backup)`

This function connects to the database and executes a SQL query. Optionally, it backs up a specified table to a CSV file.

- **Parameters**:
  - `query` (str): The SQL query to be executed.
  - `table_to_backup` (str or None): Name of the table to back up. If `None`, no backup is performed. If an empty string, an error is raised.

- **Returns**:
  - `pd.DataFrame`: A pandas DataFrame containing the query results.

- **Exceptions**:
  - Raises an `Exception` if there's an issue connecting to the database or executing the query.
  - Raises a `ValueError` if `table_to_backup` is an empty string.

- **Backup**:
  - If `table_to_backup` is provided, a backup of the table will be created in the form of a CSV file named `<table_name>_backup_<date_time>.csv`, saved in the same directory as the script.

## Example Usage

```python
# Import the function
from your_script_file import get_query_from_db

# Define your query
query = "SELECT * FROM your_table"

# Run the function with backup
result_df = get_query_from_db(query, "your_table_to_backup")

# Run the function without backup
result_df = get_query_from_db(query, None)
```

## Notes

1. Ensure that the database connection details in `.env` are correct.
2. The function will attempt to create a backup if `table_to_backup` is provided and not empty.
3. The backup file will be created with a timestamp in the filename to avoid overwriting existing backups.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
