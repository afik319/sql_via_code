### Database Query and Backup Script - Summary

This script provides the `get_query_from_db` function, designed to connect to a SQL Server database, execute a specified query, and optionally create a backup of a table as a CSV file.

#### Setup Instructions:

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
     Ensure that `DB_DRIVER` specifies the SQL Server ODBC driver.

2. **Install Dependencies**:
   - Run the following command to install all required dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Function Usage**:
   - Use the `get_query_from_db(query, table_to_backup)` function to execute a query on the specified database. If a table name is provided for `table_to_backup`, the script will back up that table to a CSV file in the current directory.

#### Example:
   ```python
   result_df = get_query_from_db("SELECT * FROM your_table", "your_table_to_backup")
