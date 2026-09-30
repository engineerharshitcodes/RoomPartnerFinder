from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.matchingController import find_matching_rooms


matching_bp = Blueprint(
    "matching",
    __name__,
    url_prefix="/api/matching"
)


@matching_bp.route("/rooms", methods=["GET"])
@jwt_required()
def matching_rooms():
    return find_matching_rooms()