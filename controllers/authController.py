from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity
)
import bcrypt
from bson import ObjectId

from config.database import db


def register_user():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Validate required fields
    if not name or not email or not password or not role:
        return jsonify({
            "message": "All fields are required"
        }), 400

    # Validate role
    if role not in ["room_owner", "partner_seeker"]:
        return jsonify({
            "message": "Invalid role"
        }), 400

    # Check whether email already exists
    existing_user = db.users.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 409

    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # Create user document
    user = {
        "name": name,
        "email": email,
        "password": hashed_password.decode("utf-8"),
        "role": role
    }

    # Save user
    result = db.users.insert_one(user)

    return jsonify({
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "role": role
    }), 201


def login_user():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Validate fields
    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    # Find user
    user = db.users.find_one({
        "email": email
    })

    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    # Check password
    password_correct = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    if not password_correct:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    # Create JWT
    token = create_access_token(
        identity=str(user["_id"])
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


def get_user_profile():

    user_id = get_jwt_identity()

    user = db.users.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }), 200