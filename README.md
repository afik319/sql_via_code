### Database Query and Backup Script - Summary

This script provides the `get_query_from_db` function, designed to connect to a SQL Server database, execute a specified query, and optionally create a backup of a table as a CSV file.

#### Function Usage

- The `get_query_from_db(query, table_to_backup)` function accepts two parameters:
  - `query`: A SQL query string to execute on the database.
  - `table_to_backup`: The name of a table to back up to a CSV file. If you don't want to create a backup, set this parameter to `None`.

#### Setup Instructions

1. **Environment Variables**:
   - The script requires a `.env` file to load database credentials and connection details.
   - Required variables:
     ```plaintext
     DB_USER=
     DB_PASSWORD=
     DB_HOST=
     DB_NAME=
     DB_DRIVER=ODBC+Driver+17+for+SQL+Server
     ```
     Leave `DB_DRIVER` unchanged, and fill in the other variables with your database details.

2. **Install Dependencies**:
   - Run the following command to install all required dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

#### Example:
   ```python
   query = "SELECT * FROM your_table"
   result_df = get_query_from_db(query, "your_table_to_backup")
