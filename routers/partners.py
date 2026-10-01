from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.partnersController import (
    create_partner_profile,
    get_partner_profiles
)
from utils.role_required import role_required

partners_bp = Blueprint(
    "partners",
    __name__,
    url_prefix="/api/partners"
)


@partners_bp.route("/profile", methods=["POST"])
@jwt_required()
@role_required("partner_seeker")
def create_profile():
    return create_partner_profile()


@partners_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profiles():
    return get_partner_profiles()