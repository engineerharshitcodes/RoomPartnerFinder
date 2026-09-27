from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config.database import db

rooms_bp = Blueprint(
    "rooms",
    __name__,
    url_prefix="/api/rooms"
)

@rooms_bp.route("/", methods=["POST"])
@jwt_required()
def create_room():

    user_id = get_jwt_identity()
    data = request.get_json()

    # Basic room information
    city = data.get("city")
    area = data.get("area")
    rent = data.get("rent")
    room_type = data.get("room_type")

    # Validate required fields
    if not city or not area or not rent or not room_type:
        return jsonify({
            "message": "City, area, rent and room_type are required"
        }), 400

    # Complete room document
    room = {
        "owner_id": user_id,

        "location": {
            "city": city,
            "area": area
        },

        "budget": {
            "rent": rent
        },

        "room": {
            "type": room_type,
            "sharing": data.get("sharing", "no_preference"),
            "furnished": data.get("furnished", "no_preference")
        },

        "lifestyle": {
            "food": data.get("food", "no_preference"),
            "smoking": data.get("smoking", "no_preference"),
            "drinking": data.get("drinking", "no_preference")
        },

        "routine": {
            "sleep_time": data.get("sleep_time"),
            "wake_time": data.get("wake_time"),
            "schedule": data.get("schedule"),
            "work_timing": data.get("work_timing")
        },

        "personality": {
            "cleanliness": data.get("cleanliness"),
            "social_level": data.get("social_level"),
            "noise_tolerance": data.get("noise_tolerance"),
            "privacy": data.get("privacy")
        },

        "guests": data.get("guests", "no_preference"),

        "pets": data.get("pets", "no_preference"),

        "facilities": data.get("facilities", {}),

        "partner_preference": {
            "gender": data.get("preferred_gender", "no_preference"),
            "age_min": data.get("age_min"),
            "age_max": data.get("age_max")
        },

        "status": "available"
    }

    result = db.rooms.insert_one(room)

    return jsonify({
        "message": "Room created successfully",
        "room_id": str(result.inserted_id)
    }), 201
    
    
@rooms_bp.route("/", methods=["GET"])
@jwt_required()
def get_rooms():

    # Get filters from URL
    city = request.args.get("city")
    area = request.args.get("area")
    min_rent = request.args.get("min_rent")
    max_rent = request.args.get("max_rent")

    # Start with available rooms
    query = {
        "status": "available"
    }

    # City filter
    if city:
        query["location.city"] = city

    # Area filter
    if area:
        query["location.area"] = area

    # Rent filter
    if min_rent or max_rent:

        query["budget.rent"] = {}

        if min_rent:
            query["budget.rent"]["$gte"] = int(min_rent)

        if max_rent:
            query["budget.rent"]["$lte"] = int(max_rent)

    # Search MongoDB
    rooms = db.rooms.find(query)

    room_list = []

    for room in rooms:
        room["_id"] = str(room["_id"])
        room_list.append(room)

    return jsonify({
        "count": len(room_list),
        "rooms": room_list
    }), 200