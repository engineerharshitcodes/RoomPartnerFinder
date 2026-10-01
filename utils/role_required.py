from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId

from config.database import db


def role_required(required_role):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            user_id = get_jwt_identity()

            if not ObjectId.is_valid(user_id):
                return jsonify({
                    "message": "Invalid user ID"
                }), 400

            user = db.users.find_one({
                "_id": ObjectId(user_id)
            })

            if not user:
                return jsonify({
                    "message": "User not found"
                }), 404

            if user["role"] != required_role:
                return jsonify({
                    "message": "Access denied"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator