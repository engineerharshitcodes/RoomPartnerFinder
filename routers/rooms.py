from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.roomController import (
    create_room,
    get_rooms
)


rooms_bp = Blueprint(
    "rooms",
    __name__,
    url_prefix="/api/rooms"
)


@rooms_bp.route("/", methods=["POST"])
@jwt_required()
def create_room_route():
    return create_room()


@rooms_bp.route("/", methods=["GET"])
@jwt_required()
def get_rooms_route():
    return get_rooms()