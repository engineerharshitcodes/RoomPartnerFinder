from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.request_controller import (
    send_request,
    update_request,
    get_sent_requests,
    get_received_requests
)


requests_bp = Blueprint(
    "requests",
    __name__,
    url_prefix="/api/requests"
)


@requests_bp.route("/", methods=["POST"])
@jwt_required()
def send_room_request():
    return send_request()


@requests_bp.route("/<request_id>", methods=["PUT"])
@jwt_required()
def update_room_request(request_id):
    return update_request(request_id)


@requests_bp.route("/sent", methods=["GET"])
@jwt_required()
def sent_requests():
    return get_sent_requests()


@requests_bp.route("/received", methods=["GET"])
@jwt_required()
def received_requests():
    return get_received_requests()