from flask import Blueprint, request, jsonify
import bcrypt
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from config.database import db

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    # Get JSON data sent by the client
    data = request.get_json()

    # Get values from JSON
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Basic validation
    if not name or not email or not password or not role:
        return jsonify({
            "message": "All fields are required"
        }), 400

    # Check role
    if role not in ["room_owner", "partner_seeker"]:
        return jsonify({
            "message": "Invalid role"
        }), 400

    # Check if email already exists
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

    # Insert into MongoDB
    result = db.users.insert_one(user)

    return jsonify({
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "role": role
    }), 201
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Check required fields
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

    # Create JWT token
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