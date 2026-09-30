from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from config.database import db


def create_room():

    owner_id = get_jwt_identity()
    data = request.get_json()

    # -------------------------
    # Required fields
    # -------------------------

    city = data.get("city")
    area = data.get("area")
    rent = data.get("rent")
    room_type = data.get("room_type")

    if not city or not area or not rent or not room_type:
        return jsonify({
            "message": "City, area, rent and room_type are required"
        }), 400

    # -------------------------
    # Create room document
    # -------------------------

    room = {
        "owner_id": owner_id,

        "location": {
            "city": city,
            "area": area
        },

        "budget": {
            "rent": rent
        },

        "room": {
            "type": room_type,
            "sharing": data.get(
                "sharing",
                "no_preference"
            ),
            "furnished": data.get(
                "furnished",
                "no_preference"
            )
        },

        "lifestyle": {
            "food": data.get(
                "food",
                "no_preference"
            ),
            "smoking": data.get(
                "smoking",
                "no_preference"
            ),
            "drinking": data.get(
                "drinking",
                "no_preference"
            )
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

        "guests": data.get(
            "guests",
            "no_preference"
        ),

        "pets": data.get(
            "pets",
            "no_preference"
        ),

        "facilities": data.get(
            "facilities",
            {}
        ),

        "partner_preference": {
            "gender": data.get(
                "preferred_gender",
                "no_preference"
            ),
            "age_min": data.get("age_min"),
            "age_max": data.get("age_max"),
            "food": data.get(
                "preferred_food",
                "no_preference"
            ),
            "smoking": data.get(
                "preferred_smoking",
                "no_preference"
            ),
            "drinking": data.get(
                "preferred_drinking",
                "no_preference"
            )
        },

        "status": "available"
    }

    # -------------------------
    # Save to MongoDB
    # -------------------------

    result = db.rooms.insert_one(room)

    return jsonify({
        "message": "Room created successfully",
        "room_id": str(result.inserted_id)
    }), 201


def get_rooms():

    # -------------------------
    # Read query parameters
    # -------------------------

    city = request.args.get("city")
    area = request.args.get("area")
    min_rent = request.args.get("min_rent")
    max_rent = request.args.get("max_rent")

    # Only available rooms
    query = {
        "status": "available"
    }

    # -------------------------
    # Location filters
    # -------------------------

    if city:
        query["location.city"] = city

    if area:
        query["location.area"] = area

    # -------------------------
    # Rent filters
    # -------------------------

    if min_rent or max_rent:

        query["budget.rent"] = {}

        if min_rent:
            query["budget.rent"]["$gte"] = int(min_rent)

        if max_rent:
            query["budget.rent"]["$lte"] = int(max_rent)

    # -------------------------
    # Query MongoDB
    # -------------------------

    rooms = db.rooms.find(query)

    room_list = []

    for room in rooms:

        room["_id"] = str(room["_id"])

        room_list.append(room)

    # -------------------------
    # Response
    # -------------------------

    return jsonify({
        "count": len(room_list),
        "rooms": room_list
    }), 200