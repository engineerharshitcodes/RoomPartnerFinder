from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.partnersController import (
    create_partner_profile,
    get_partner_profiles
)


partners_bp = Blueprint(
    "partners",
    __name__,
    url_prefix="/api/partners"
)


@partners_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile():
    return create_partner_profile()


@partners_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profiles():
    return get_partner_profiles()