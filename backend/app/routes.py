from flask import Blueprint, jsonify, request
from .db import ping_database, get_connection
from .db import (
    get_top_rated_media,
    get_top_users_completed,
    get_top_media_completed,
    get_avg_rating_per_genre,
    get_users_rating_above,
    get_recent_low_rated,
    create_user,
    get_all_users,
    update_user,
    delete_user,
    create_review,
    update_review,
    delete_review
)
import logging

api_bp = Blueprint("api", __name__)

# Configure a logger for error reporting
logger = logging.getLogger(__name__)

@api_bp.get("/health")
def api_health():
    """Lightweight health endpoint for API layer monitoring."""
    return jsonify({"status": "ok", "service": "api"})

@api_bp.get("/db/ping")
def db_ping():
    """Verifies DB connectivity/credentials with a trivial SELECT."""
    ok, error = ping_database()
    if not ok and error:
        # Log the detailed error internally, avoid exposing sensitive info to client
        logger.error("DB ping failed: %s", error)
    return jsonify({
        "status": "ok" if ok else "error",
        "error": None if ok else "Database connection failed",
    })
@api_bp.get("/users")
def get_users():
    """Return all users from the User table."""
    try:
        from .db import get_connection  # safe lazy import

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM User")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(rows)

    except Exception as exc:
        logger.error(f"/users failed: {exc}")
        return jsonify({"error": "Failed to fetch users"}), 500

@api_bp.get("/top-rated-media")
def top_rated_media():
    """Top 5 highest-rated media overall by type."""
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                Media.MediaType,
                Media.MediaName,
                ROUND(AVG(Review.Rating), 2) AS AvgRating
            FROM Review
            JOIN Media ON Review.MediaId = Media.MediaId
            GROUP BY Media.MediaId, Media.MediaType
            ORDER BY AvgRating DESC
            LIMIT 5;
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/top-rated-media failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/top-users-completed")
def top_users_completed():
    """Top 5 users who completed the most media."""
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
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
            LIMIT 5 OFFSET 0;
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/top-users-completed failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/top-media-completions")
def top_media_completions():
    """Top 5 media with the most completions."""
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                m.MediaName, 
                COUNT(*) AS user_completions
            FROM Media AS m
            JOIN Review AS r ON m.MediaId = r.MediaId
            WHERE r.Status = 'Completed'
            GROUP BY m.MediaId, m.MediaName
            HAVING user_completions > 5
            ORDER BY user_completions DESC
            LIMIT 5 OFFSET 0;
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/top-media-completions failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/avg-rating-genre")
def avg_rating_genre():
    """Average rating per genre."""
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                AVG(r.Rating) AS avg_rating, 
                g.GenreName
            FROM Review AS r
            JOIN Media AS m ON r.MediaId = m.MediaId
            JOIN Genre AS g ON m.GenreId = g.GenreId
            GROUP BY g.GenreName;
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/avg-rating-genre failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/users-rated-high")
def users_rated_high():
    """Users who rated at least one media above 4 (per your SQL)."""
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                UserId, 
                FirstName, 
                LastName, 
                ProfileName
            FROM User
            WHERE UserId IN (
                SELECT UserId
                FROM Review
                WHERE Rating >= 4
            );
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/users-rated-high failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/low-rated-recent")
def low_rated_recent():
    """10 most recent low-rated media (rating ≤ 3)."""
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                Media.MediaName,
                Media.MediaType,
                Media.ReleaseYear,
                Review.Rating
            FROM Review
            JOIN Media ON Review.MediaId = Media.MediaId
            WHERE Review.Rating <= 3
            ORDER BY Media.ReleaseYear DESC
            LIMIT 10;
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/low-rated-recent failed: {exc}")
        return jsonify({"error": "Query failed"}), 500
    

# USER CRUD ROUTES


@api_bp.post("/users/create")
def api_create_user():
    """Create a new user."""
    data = request.get_json(silent=True) or {}

    first = data.get("FirstName")
    last = data.get("LastName")
    profile = data.get("ProfileName")

    if not first or not last or not profile:
        return jsonify({"error": "Missing fields"}), 400

    ok, err = create_user(first, last, profile)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"}), 201


@api_bp.get("/users/all")
def api_get_all_users():
    """Get all users."""
    try:
        rows = get_all_users()
        return jsonify(rows)
    except Exception as exc:
        logger.error(f"/users/all failed: {exc}")
        return jsonify({"error": "Failed to fetch users"}), 500


@api_bp.put("/users/<int:user_id>")
def api_update_user(user_id):
    """Update an existing user."""
    data = request.get_json(silent=True) or {}

    first = data.get("FirstName")
    last = data.get("LastName")
    profile = data.get("ProfileName")

    if not first or not last or not profile:
        return jsonify({"error": "Missing fields"}), 400

    ok, err = update_user(user_id, first, last, profile)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})


@api_bp.delete("/users/<int:user_id>")
def api_delete_user(user_id):
    """Delete a user."""
    ok, err = delete_user(user_id)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})


# REVIEW CRUD ROUTES


@api_bp.post("/reviews/create")
def api_create_review():
    """Create a review."""
    data = request.get_json(silent=True) or {}

    user_id = data.get("UserId")
    media_id = data.get("MediaId")
    rating = data.get("Rating")
    text = data.get("ReviewText")
    status = data.get("Status")

    if not user_id or not media_id or rating is None or not status:
        return jsonify({"error": "Required fields missing"}), 400

    ok, err = create_review(user_id, media_id, rating, text, status)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"}), 201


@api_bp.put("/reviews/<int:review_id>")
def api_update_review(review_id):
    """Update a review."""
    data = request.get_json(silent=True) or {}

    rating = data.get("Rating")
    text = data.get("ReviewText")
    status = data.get("Status")

    if rating is None or not status:
        return jsonify({"error": "Missing required fields"}), 400

    ok, err = update_review(review_id, rating, text, status)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})


@api_bp.delete("/reviews/<int:review_id>")
def api_delete_review(review_id):
    """Delete a review."""
    ok, err = delete_review(review_id)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})
