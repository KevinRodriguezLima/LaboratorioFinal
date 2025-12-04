from flask import Blueprint, request, jsonify
from hashing.sha1 import sha1

hash_bp = Blueprint("hash_bp", __name__, url_prefix="/api")

@hash_bp.route("/hash", methods=["POST"])
def hash_route():
    data = request.get_json()

    msg = data.get("message", "")
    algorithm = data.get("algorithm", "SHA1").upper()

    if algorithm == "SHA1":
        result = sha1(msg)
    else:
        # Aquí luego tus compañeros implementan MD5, SHA256, etc.
        result = f"[SERVIDOR] El algoritmo {algorithm} aún no está implementado."

    return jsonify({
        "algorithm": algorithm,
        "message": msg,
        "hash": result
    })
