from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.authController import (
    register_user,
    login_user,
    get_user_profile
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user()


@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user()


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    return get_user_profile()