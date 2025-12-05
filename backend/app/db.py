import os
from typing import Tuple, Optional, Dict, Any, List


import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection

def _get_db_config() -> Dict[str, Any]:
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


def get_connection() -> MySQLConnection:
    """Create and return a new MySQL connection using the above config."""
    cfg = _get_db_config()
    conn = mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        connection_timeout=3,
    )
    # Ensure we return a MySQLConnection, even if it's pooled (though here it's direct)
    return conn  # type: ignore


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

def create_user(first: str, last: str, profile: str) -> Tuple[bool, Optional[str]]:
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


def get_all_users() -> List[Dict[str, Any]]:
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM User")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows  # type: ignore
    except Exception:
        return []


def update_user(user_id: int, first: str, last: str, profile: str) -> Tuple[bool, Optional[str]]:
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


def delete_user(user_id: int) -> Tuple[bool, Optional[str]]:
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

def create_review(user_id: int, media_id: int, rating: int, text: str, status: str) -> Tuple[bool, Optional[str]]:
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


def update_review(review_id: int, rating: int, text: str, status: str) -> Tuple[bool, Optional[str]]:
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


def delete_review(review_id: int) -> Tuple[bool, Optional[str]]:
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

# Search Functionality

def search_database(query: str, category: str, sort: str) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        
        sql = ""
        params = []
        search_term = f"%{query}%"

        if category == 'media':
            sql = """
                SELECT 
                    m.MediaName, 
                    m.MediaType, 
                    m.ReleaseYear, 
                    g.GenreName, 
                    p.PlatformName, 
                    ROUND(AVG(r.Rating), 2) as AvgRating,
                    COUNT(r.ReviewId) as ReviewCount
                FROM Media m
                LEFT JOIN Genre g ON m.GenreId = g.GenreId
                LEFT JOIN Platform p ON m.PlatformId = p.PlatformId
                LEFT JOIN Review r ON m.MediaId = r.MediaId
                WHERE m.MediaName LIKE %s
                GROUP BY m.MediaId
            """
            params = [search_term]
            
            if sort == 'az':
                sql += " ORDER BY m.MediaName ASC"
            elif sort == 'za':
                sql += " ORDER BY m.MediaName DESC"
            elif sort == 'rating_desc':
                sql += " ORDER BY AvgRating DESC"
            elif sort == 'rating_asc':
                sql += " ORDER BY AvgRating ASC"
            elif sort == 'year_desc':
                sql += " ORDER BY m.ReleaseYear DESC"
            elif sort == 'year_asc':
                sql += " ORDER BY m.ReleaseYear ASC"

        elif category == 'user':
            sql = """
                SELECT 
                    u.FirstName, 
                    u.LastName, 
                    u.ProfileName,
                    COUNT(r.ReviewId) as ReviewCount
                FROM User u
                LEFT JOIN Review r ON u.UserId = r.UserId
                WHERE u.FirstName LIKE %s OR u.LastName LIKE %s OR u.ProfileName LIKE %s
                GROUP BY u.UserId
            """
            params = [search_term, search_term, search_term]
            
            if sort == 'az':
                sql += " ORDER BY u.LastName ASC, u.FirstName ASC"
            elif sort == 'za':
                sql += " ORDER BY u.LastName DESC, u.FirstName DESC"
            elif sort == 'count_desc':
                sql += " ORDER BY ReviewCount DESC"
            elif sort == 'count_asc':
                sql += " ORDER BY ReviewCount ASC"

        elif category == 'genre':
            sql = """
                SELECT 
                    g.GenreName,
                    COUNT(m.MediaId) as MediaCount,
                    ROUND(AVG(r.Rating), 2) as AvgRating
                FROM Genre g
                LEFT JOIN Media m ON g.GenreId = m.GenreId
                LEFT JOIN Review r ON m.MediaId = r.MediaId
                WHERE g.GenreName LIKE %s
                GROUP BY g.GenreId
            """
            params = [search_term]
            
            if sort == 'az':
                sql += " ORDER BY g.GenreName ASC"
            elif sort == 'za':
                sql += " ORDER BY g.GenreName DESC"
            elif sort == 'rating_desc':
                sql += " ORDER BY AvgRating DESC"
            elif sort == 'rating_asc':
                sql += " ORDER BY AvgRating ASC"
            elif sort == 'count_desc':
                sql += " ORDER BY MediaCount DESC"
            elif sort == 'count_asc':
                sql += " ORDER BY MediaCount ASC"

        else:
            return False, "Invalid category", None

        cur.execute(sql, tuple(params))
        rows = cur.fetchall() or []
        cur.close()
        return True, None, rows

    except Error as exc:
        return False, str(exc), None
    finally:
        if conn:
            conn.close()


def create_full_media_entry(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Orchestrates the creation of User, Genre, Platform, Media, and Review
    in a single transaction (or reuses existing ones).
    """
    conn = None
    try:
        conn = get_connection()
        conn.start_transaction()  # Explicitly start transaction for ACID compliance

        def fetch_value(sql, params):
            cur = conn.cursor(buffered=True)
            try:
                cur.execute(sql, params)
                rows = cur.fetchall()
                return rows[0][0] if rows else None
            except Exception:
                # If fetchall fails or returns nothing, ensure we close cleanly
                return None
            finally:
                cur.close()

        def insert_record(sql, params):
            cur = conn.cursor(buffered=True)
            try:
                cur.execute(sql, params)
                # Some drivers/configurations might have issues with fetchall after insert
                # We can try to consume results if any exist, but ignore errors
                try:
                    cur.fetchall()
                except Exception:
                    pass
                return cur.lastrowid
            finally:
                cur.close()

        def execute_stmt(sql, params):
            cur = conn.cursor(buffered=True)
            try:
                cur.execute(sql, params)
                try:
                    cur.fetchall()
                except Exception:
                    pass
            finally:
                cur.close()

        # 1. Ensure User
        # Use FOR UPDATE to lock rows and ensure Isolation (prevent race conditions)
        user_id = fetch_value("SELECT UserId FROM User WHERE ProfileName = %s FOR UPDATE", (data['profilename'],))
        if not user_id:
            user_id = insert_record(
                "INSERT INTO User (FirstName, LastName, ProfileName) VALUES (%s, %s, %s)",
                (data['firstname'], data['lastname'], data['profilename'])
            )

        # 2. Ensure Genre
        genre_id = fetch_value("SELECT GenreId FROM Genre WHERE GenreName = %s FOR UPDATE", (data['genre'],))
        if not genre_id:
            genre_id = insert_record("INSERT INTO Genre (GenreName) VALUES (%s)", (data['genre'],))

        # 3. Ensure Platform
        platform_id = fetch_value("SELECT PlatformId FROM Platform WHERE PlatformName = %s FOR UPDATE", (data['platform'],))
        if not platform_id:
            platform_id = insert_record("INSERT INTO Platform (PlatformName) VALUES (%s)", (data['platform'],))

        # 4. Ensure Media
        media_id = fetch_value("""
            SELECT MediaId FROM Media 
            WHERE MediaName = %s AND MediaType = %s AND ReleaseYear = %s FOR UPDATE
        """, (data['medianame'], data['mediatype'], data['releaseyear']))
        
        if not media_id:
            media_id = insert_record("""
                INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data['medianame'], 
                data['mediatype'], 
                data['releaseyear'], 
                genre_id, 
                platform_id, 
                data.get('description', '')
            ))

        # 5. Create or Update Review
        review_id = fetch_value("SELECT ReviewId FROM Review WHERE UserId = %s AND MediaId = %s FOR UPDATE", (user_id, media_id))
        
        if review_id:
            # Update existing review
            execute_stmt("""
                UPDATE Review 
                SET Rating = %s, ReviewText = %s, Status = %s
                WHERE ReviewId = %s
            """, (data['rating'], data.get('ratingtext', ''), data['status'], review_id))
        else:
            # Insert new review
            execute_stmt("""
                INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, media_id, data['rating'], data.get('ratingtext', ''), data['status']))

        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn:
            conn.close()
