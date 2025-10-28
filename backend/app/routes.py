from flask import Blueprint, jsonify, request
from .db import ping_database, name, fetch_names
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
"""Examples
@api_bp.post("/names")
def create_name():
    data = request.get_json(silent=True) or {}
    person_name = (data.get("name") or "").strip()
    if not person_name:
        return jsonify({"status": "error", "error": "name needed"}), 400
    ok, error = name(person_name)
    if not ok:
        return jsonify({"status": "error", "error": error or "insert failed"}),500
    return jsonify({"status": "ok"})

@api_bp.get("/names")
def list_names():
    ok, error, rows = fetch_names()
    if not ok:
        return jsonify({"status": "error", "error": error or "fetch failed"}), 500
    return jsonify({"status": "ok", "items": rows})
"""