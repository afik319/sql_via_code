import logging.handlers
import logging
import sys

"""
Sets up and configures a logger for the package.

The logger writes logs to both the console (DEBUG level) and a log file (INFO level).

Returns:
    logging.Logger: A configured logger instance.
"""
def setup_logger():
    # Create a logger instance with the name "sql_via_code"
    logger = logging.getLogger("sql_via_code")
    logger.setLevel(logging.DEBUG)

    # Define log message format
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # Console handler for DEBUG level logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # File handler for INFO level logs
    file_handler = logging.FileHandler('sql_via_code.log')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger

# Initialize and expose the logger
logger = setup_logger()
