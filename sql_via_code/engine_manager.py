from sqlalchemy.ext.asyncio import create_async_engine
from .logger_config import logger
from dotenv import dotenv_values
from threading import Lock
import sqlalchemy

class EngineManager:
    """
        Manages database engine creation and connections for various database types.

        Attributes:
            REQUIRED_FIELDS (dict): Specifies required fields for each supported database type.
        """

    REQUIRED_FIELDS = {
        "sqlite": ["NAME"],
        "postgresql": ["USER", "PASSWORD", "HOST", "NAME"],
        "mysql": ["USER", "PASSWORD", "HOST", "NAME"],
        "mssql": ["USER", "PASSWORD", "HOST", "NAME", "DRIVER"],
        "oracle": ["USER", "PASSWORD", "HOST", "NAME"],
    }

    def __init__(self):
        """
        Initializes the EngineManager instance.

        Creates a dictionary to store database engines and a thread lock for thread safety.
        """
        self._engines = {}
        self._lock = Lock()

    """
    Creates or retrieves a database engine based on the provided environment configuration.

    Args:
        env_file_name (str, optional): Path to the `.env` file containing database credentials. Defaults to `.env`.

    Returns:
        AsyncEngine: A SQLAlchemy asynchronous engine instance.

    Raises:
        KeyError: If the `DB_TYPE` is missing in the `.env` file.
        ValueError: If the database type is unsupported.
        Exception: If engine creation fails.
    """
    def get_engine(self, env_file_name = None):
        env_file = env_file_name or ".env"
        if env_file not in self._engines:
            with self._lock:
                if env_file not in self._engines:
                    env = dotenv_values(env_file)

                    db_type = env.get("DB_TYPE")
                    if not db_type:
                        error_message = "Missing required environment variable: DB_TYPE"
                        logger.error(error_message)
                        raise KeyError(error_message)
                    try:
                        connection_string = self._build_connection_string(db_type, env)
                        logger.info(f"Creating engine for {db_type}...")
                        self._engines[env_file] = create_async_engine(connection_string)
                    except KeyError as e:
                        logger.error(f"Error: {e}")
                        raise
                    except Exception as e:
                        logger.error(f"Failed to create engine: {e}")
                        raise
        return self._engines[env_file]

    """
    Connects to the database engine asynchronously.

    Args:
        env_file_name (str, optional): Path to the `.env` file. Defaults to `.env`.

    Returns:
        AsyncConnection: An active database connection.

    Raises:
        OperationalError: If there is a database connectivity issue.
        ProgrammingError: If there is a configuration or query issue.
        Exception: For unexpected errors.
    """
    async def connect_db(self, env_file_name = None):
        engine = self.get_engine(env_file_name)
        try:
            conn = await engine.connect()
            return conn
        except sqlalchemy.exc.OperationalError as e:
            logger.error(f"Operational Error: {e}")
            raise
        except sqlalchemy.exc.ProgrammingError as e:
            logger.error(f"Programming Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise

    """
    Builds a connection string based on the database type and environment variables.

    Args:
        db_type (str): The database type (e.g., sqlite, postgresql, mysql, mssql, oracle).
        env (dict): A dictionary of environment variables.

    Returns:
        str: A valid SQLAlchemy database connection string.

    Raises:
        ValueError: If the database type is unsupported.
        KeyError: If required fields are missing.
    """
    def _build_connection_string(self, db_type, env):
        db_type = db_type.lower()
        if db_type not in self.REQUIRED_FIELDS:
            error_message = f"Unsupported database type: {db_type}. Supported types are: {', '.join(self.REQUIRED_FIELDS.keys())}"
            logger.error(error_message)
            raise ValueError(error_message)
        self._check_required_fields(env, db_type)

        connection_func_name = f"_{db_type}_connection"
        connection_func = getattr(self, connection_func_name, None)

        if callable(connection_func):
            return connection_func(env)
        else:
            error_message = f"Connection function for {db_type} is not implemented."
            logger.error(error_message)
            raise NotImplementedError(error_message)

    """
    Validates that all required fields for the given database type are present and non-empty.

    Args:
        env (dict): Environment variables.
        db_type (str): The database type being validated.

    Raises:
        KeyError: If any required field is missing or empty.
    """
    def _check_required_fields(self, env, db_type):
        """ בודקת שדות חובה לפי סוג מסד הנתונים """
        for field in self.REQUIRED_FIELDS[db_type]:
            if not env.get(field) or not env[field].strip():
                error_message = f"Missing or empty required field: {field} for {db_type.capitalize()}"
                logger.error(error_message)
                raise KeyError(error_message)

    """
    Builds a connection string for SQLite.
    """
    def _sqlite_connection(self, env):
        """ בונה מחרוזת חיבור ל-SQLite """
        self._check_required_fields(env, "sqlite")
        return f"sqlite+aiosqlite:///{env['NAME']}"

    """
    Builds a connection string for PostgreSQL.
    """
    def _postgresql_connection(self, env):
        """ בונה מחרוזת חיבור ל-PostgreSQL """
        self._check_required_fields(env, "postgresql")
        return f"postgresql+asyncpg://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}"

    """
    Builds a connection string for MySQL.
    """
    def _mysql_connection(self, env):
        """ בונה מחרוזת חיבור ל-MySQL """
        self._check_required_fields(env, "mysql")
        return f"mysql+aiomysql://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}"

    """
    Builds a connection string for MSSQL.
    """
    def _mssql_connection(self, env):
        """ בונה מחרוזת חיבור ל-MSSQL """
        self._check_required_fields(env, "mssql")
        return f"mssql+pyodbc://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}?driver={env['DRIVER']}"

    """
    Builds a connection string for Oracle.
    """
    def _oracle_connection(self, env):
        """ בונה מחרוזת חיבור ל-Oracle """
        self._check_required_fields(env, "oracle")
        return f"oracle+oracledb://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}"
