import os
from typing import Tuple, Optional


import mysql.connector
from mysql.connector import Error


def _get_db_config() -> dict:
    """Load DB configuration from environment variables.

    Using env vars (with python-dotenv during local dev) keeps secrets out of
    source control and allows configuration per environment.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "mysql"),
    }


def get_connection() -> mysql.connector.connection.MySQLConnection:
    """Create and return a new MySQL connection using the above config."""
    cfg = _get_db_config()
    return mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        connection_timeout=3,
    )


def ping_database() -> Tuple[bool, Optional[str]]:
    """Execute a trivial query to confirm connectivity and credentials.

    Returns (ok, error_message_if_any).
    """
    try:
        conn = get_connection()
    except Error as exc:
        return False, str(exc)
    except Exception as exc:
        return False, str(exc)

    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        return True, None
    except Error as exc:
        return False, str(exc)
    except Exception as exc:
        return False, str(exc)
    finally:
        try:
            conn.close()
        except Exception:
            pass

# Example helpers (commented):
# def ensure_table_exists() -> None:
#     """Create the `names` table if it does not already exist.
#     Example includes an email column to store a second field.
#     """
#     conn = get_connection()
#     try:
#         cur = conn.cursor()
#         cur.execute(
#             """
#             CREATE TABLE IF NOT EXISTS names (
#                 id INT PRIMARY KEY AUTO_INCREMENT,
#                 name VARCHAR(255) NOT NULL,
#                 email VARCHAR(255) NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#             """
#         )
#         conn.commit()
#         cur.close()
#     finally:
#         conn.close()

def table_exists() -> None:
    conn=get_connection()
    try: 
        cur=conn.cursor()
        cur.execute ('''
            CREATE TABLE IF NOT EXISTS names (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL
            )
            ''')
        conn.commit()
        cur.close()
    finally: 
        conn.close()
#
# def insert_name(name: str, email: str) -> Tuple[bool, Optional[str]]:
#     """Insert a single row into `names` after ensuring the table exists.
#     This example writes both name and email.
#     """
#     try:
#         ensure_table_exists()
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO names (name, email) VALUES (%s, %s)", (name, email))
#         conn.commit()
#         cur.close()
#         conn.close()
#         return True, None
#     except Error as exc:
#         return False, str(exc)
#     except Exception as exc:
#         return False, str(exc)
def name(name: str) -> Tuple[bool, Optional[str]]:
    try:
        table_exists()
        conn=get_connection()
        cur=conn.cursor()
        cur.execute("INSERT INTO names (name) VALUES (%s)", (name,))
        conn.commit()
        cur.close()
        return True, None
    except Error as exc:
        return False, str(exc)
    except Exception as exc:
        return False, str(exc)
    finally:
        conn.close()

