from flask import Blueprint, jsonify, request
from typing import Dict, Any
from .db import ping_database
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
    delete_review,
    create_full_media_entry,
    search_database
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
        ok, err, data = get_top_rated_media()
        if not ok:
            logger.error(f"/top-rated-media failed: {err}")
            return jsonify({"error": "Query failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/top-rated-media failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/top-users-completed")
def top_users_completed():
    """Top 5 users who completed the most media."""
    try:
        ok, err, data = get_top_users_completed()
        if not ok:
            logger.error(f"/top-users-completed failed: {err}")
            return jsonify({"error": "Query failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/top-users-completed failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/top-media-completions")
def top_media_completions():
    """Top 5 media with the most completions."""
    try:
        ok, err, data = get_top_media_completed()
        if not ok:
            logger.error(f"/top-media-completions failed: {err}")
            return jsonify({"error": "Query failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/top-media-completions failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/avg-rating-genre")
def avg_rating_genre():
    """Average rating per genre."""
    try:
        ok, err, data = get_avg_rating_per_genre()
        if not ok:
            logger.error(f"/avg-rating-genre failed: {err}")
            return jsonify({"error": "Query failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/avg-rating-genre failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/users-rated-high")
def users_rated_high():
    """Users who rated at least one media above 4 (per your SQL)."""
    try:
        ok, err, data = get_users_rating_above()
        if not ok:
            logger.error(f"/users-rated-high failed: {err}")
            return jsonify({"error": "Query failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/users-rated-high failed: {exc}")
        return jsonify({"error": "Query failed"}), 500

@api_bp.get("/low-rated-recent")
def low_rated_recent():
    """10 most recent low-rated media (rating ≤ 3)."""
    try:
        ok, err, data = get_recent_low_rated()
        if not ok:
            logger.error(f"/low-rated-recent failed: {err}")
            return jsonify({"error": "Query failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/low-rated-recent failed: {exc}")
        return jsonify({"error": "Query failed"}), 500
    

@api_bp.get("/search")
def api_search():
    """Search endpoint for Media, Users, and Genres."""
    query = request.args.get("q", "")
    category = request.args.get("category", "media")
    sort = request.args.get("sort", "az")

    try:
        ok, err, data = search_database(query, category, sort)
        if not ok:
            logger.error(f"/search failed: {err}")
            return jsonify({"error": err or "Search failed"}), 500
        return jsonify(data)
    except Exception as exc:
        logger.error(f"/search failed: {exc}")
        return jsonify({"error": "Search failed"}), 500


@api_bp.post("/media-entries")
def api_create_media_entry():
    """Create a full media entry (User, Media, Review, etc.)."""
    data: Dict[str, Any] = request.get_json(silent=True) or {}  # type: ignore
    
    # Basic validation
    required = ["firstname", "lastname", "profilename", "mediatype", "medianame", "releaseyear", "genre", "platform", "rating", "status"]
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing field: {field}"}), 400

    ok, err = create_full_media_entry(data)
    if not ok:
        logger.error(f"Create media entry failed: {err}")
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"}), 201


# USER CRUD ROUTES


@api_bp.post("/users/create")
def api_create_user():
    """Create a new user."""
    data: Dict[str, Any] = request.get_json(silent=True) or {}  # type: ignore

    first = data.get("FirstName")
    last = data.get("LastName")
    profile = data.get("ProfileName")

    if not first or not last or not profile:
        return jsonify({"error": "Missing fields"}), 400

    ok, err = create_user(str(first), str(last), str(profile))
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
def api_update_user(user_id: int):
    """Update an existing user."""
    data: Dict[str, Any] = request.get_json(silent=True) or {}  # type: ignore

    first = data.get("FirstName")
    last = data.get("LastName")
    profile = data.get("ProfileName")

    if not first or not last or not profile:
        return jsonify({"error": "Missing fields"}), 400

    ok, err = update_user(user_id, str(first), str(last), str(profile))
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})


@api_bp.delete("/users/<int:user_id>")
def api_delete_user(user_id: int):
    """Delete a user."""
    ok, err = delete_user(user_id)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})


# REVIEW CRUD ROUTES


@api_bp.post("/reviews/create")
def api_create_review():
    """Create a review."""
    data: Dict[str, Any] = request.get_json(silent=True) or {}  # type: ignore

    user_id = data.get("UserId")
    media_id = data.get("MediaId")
    rating = data.get("Rating")
    text = data.get("ReviewText")
    status = data.get("Status")

    if not user_id or not media_id or rating is None or not status:
        return jsonify({"error": "Required fields missing"}), 400

    ok, err = create_review(int(user_id), int(media_id), int(rating), str(text) if text else "", str(status))
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"}), 201


@api_bp.put("/reviews/<int:review_id>")
def api_update_review(review_id: int):
    """Update a review."""
    data: Dict[str, Any] = request.get_json(silent=True) or {}  # type: ignore

    rating = data.get("Rating")
    text = data.get("ReviewText")
    status = data.get("Status")

    if rating is None or not status:
        return jsonify({"error": "Missing required fields"}), 400

    ok, err = update_review(review_id, int(rating), str(text) if text else "", str(status))
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})


@api_bp.delete("/reviews/<int:review_id>")
def api_delete_review(review_id: int):
    """Delete a review."""
    ok, err = delete_review(review_id)
    if not ok:
        return jsonify({"error": err}), 500

    return jsonify({"status": "ok"})
