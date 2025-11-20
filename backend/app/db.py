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
        "database": os.getenv("DB_NAME", "mediawatchlist"),
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


# Group 1 — Top 5 highest rated

def get_top_rated_media(limit: int = 5):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT 
                Media.MediaType,
                Media.MediaName,
                ROUND(AVG(Review.Rating), 2) AS AvgRating
            FROM Review
            JOIN Media ON Review.MediaId = Media.MediaId
            GROUP BY Media.MediaId, Media.MediaType
            ORDER BY AvgRating DESC
            LIMIT %s;
        """

        cur.execute(query, (limit,))
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()



# Group 2 — Users w/ most completions

def get_top_users_completed(limit: int = 5):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT 
                u.FirstName, 
                u.LastName, 
                COUNT(*) AS media_done
            FROM User AS u
            JOIN Review AS r ON u.UserId = r.UserId
            WHERE r.Status = 'Completed'
            GROUP BY u.UserId, u.FirstName, u.LastName
            HAVING media_done > 5
            ORDER BY media_done DESC
            LIMIT %s OFFSET 0;
        """

        cur.execute(query, (limit,))
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()


# Group 2 — Media w/ most completions

def get_top_media_completed(limit: int = 5):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT 
                m.MediaName, 
                COUNT(*) AS user_completions
            FROM Media AS m
            JOIN Review AS r ON m.MediaId = r.MediaId
            WHERE r.Status = 'Completed'
            GROUP BY m.MediaId, m.MediaName
            HAVING user_completions > 5
            ORDER BY user_completions DESC
            LIMIT %s OFFSET 0;
        """

        cur.execute(query, (limit,))
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()



# Group 2 — Average rating per genre

def get_avg_rating_per_genre():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT 
                AVG(r.Rating) AS avg_rating, 
                g.GenreName
            FROM Review AS r
            JOIN Media AS m ON r.MediaId = m.MediaId
            JOIN Genre AS g ON m.GenreId = g.GenreId
            GROUP BY g.GenreName;
        """

        cur.execute(query)
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()



# Group 3 — Users who rated above threshold

def get_users_rating_above(min_rating: int = 4):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT 
                UserId, 
                FirstName, 
                LastName, 
                ProfileName
            FROM User
            WHERE UserId IN (
                SELECT UserId
                FROM Review
                WHERE Rating >= %s
            );
        """

        cur.execute(query, (min_rating,))
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()



# Group 3 — 10 most recent low-rated media

def get_recent_low_rated(limit: int = 10):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT 
                Media.MediaName,
                Media.MediaType,
                Media.ReleaseYear,
                Review.Rating
            FROM Review
            JOIN Media ON Review.MediaId = Media.MediaId
            WHERE Review.Rating <= 3
            ORDER BY Media.ReleaseYear DESC
            LIMIT %s;
        """

        cur.execute(query, (limit,))
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()

#User CRUD

def create_user(first, last, profile):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO User (FirstName, LastName, ProfileName) VALUES (%s, %s, %s)",
            (first, last, profile),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def get_all_users():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM User")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception:
        return []


def update_user(user_id, first, last, profile):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE User
            SET FirstName=%s, LastName=%s, ProfileName=%s
            WHERE UserId=%s
        """, (first, last, profile, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def delete_user(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM User WHERE UserId=%s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)



# Review CRUD

def create_review(user_id, media_id, rating, text, status):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, media_id, rating, text, status))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def update_review(review_id, rating, text, status):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Review
            SET Rating=%s, ReviewText=%s, Status=%s
            WHERE ReviewId=%s
        """, (rating, text, status, review_id))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def delete_review(review_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Review WHERE ReviewId=%s", (review_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)
"""Examples
def table_exists() -> None:
    conn=get_connection()
    try: 
        cur=conn.cursor()
        cur.execute ('''
            CREATE TABLE IF NOT EXISTS names (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        conn.commit()
        cur.close()
    finally: 
        conn.close()

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


def fetch_names() -> Tuple[bool, Optional[str], Optional[list]]:
    '''Return a list of rows as dicts: [{id, name, created_at}, ...].'''
    conn = None
    try:
        table_exists()
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, name, created_at FROM names ORDER BY id DESC")
        rows = cur.fetchall() or []
        # Ensure created_at is JSON-serializable for the API response
        for row in rows:
            ca = row.get("created_at")
            if ca is not None and hasattr(ca, "isoformat"):
                row["created_at"] = ca.isoformat()
        cur.close()
        return True, None, rows
    except Error as exc:
        return False, str(exc), None
    except Exception as exc:
        return False, str(exc), None
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass
"""
