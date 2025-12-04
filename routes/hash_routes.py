from flask import Blueprint, request, jsonify
from hashing.sha1_manual import sha1_manual

hash_bp = Blueprint("hash_bp", __name__, url_prefix="/api")

@hash_bp.route("/sha1", methods=["POST"])
def sha1_route():
    data = request.get_json()
    msg = data.get("message", "")
    result = sha1_manual(msg)

    return jsonify({
        "algorithm": "SHA-1 (manual)",
        "message": msg,
        "hash": result
    })
