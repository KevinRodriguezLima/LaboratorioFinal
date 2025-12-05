from flask import Blueprint, request, jsonify
from hashing.sha1 import sha1
from hashing.md4 import md4
from hashing.md5 import md5

hash_bp = Blueprint("hash_bp", __name__, url_prefix="/api")


@hash_bp.route("/hash", methods=["POST"])
def hash_route():
    data = request.get_json()

    msg = data.get("message", "")
    algorithm = data.get("algorithm", "SHA1").upper()

    if algorithm == "SHA1":
        result = sha1(msg)
    elif algorithm == "MD4":
        result = md4(msg)
    elif algorithm == "MD5":
        result = md5(msg)
    else:
        result = f"[SERVIDOR] El algoritmo {algorithm} aun no esta implementado."

    return jsonify({
        "algorithm": algorithm,
        "message": msg,
        "hash": result
    })
