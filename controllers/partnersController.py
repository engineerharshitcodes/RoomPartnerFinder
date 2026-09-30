from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from config.database import db


def create_partner_profile():

    user_id = get_jwt_identity()
    data = request.get_json()

    # -------------------------
    # Basic information
    # -------------------------

    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    occupation = data.get("occupation")

    # -------------------------
    # Location & Budget
    # -------------------------

    city = data.get("city")
    area = data.get("area")
    min_budget = data.get("min_budget")
    max_budget = data.get("max_budget")

    # -------------------------
    # Required fields
    # -------------------------

    if not all([
        name,
        age,
        gender,
        occupation,
        city,
        area,
        min_budget,
        max_budget
    ]):
        return jsonify({
            "message": "Required fields are missing"
        }), 400

    # -------------------------
    # Create partner profile
    # -------------------------

    profile = {

        "user_id": user_id,

        "basic": {
            "name": name,
            "age": age,
            "gender": gender,
            "occupation": occupation
        },

        "location": {
            "city": city,
            "area": area
        },

        "budget": {
            "min": min_budget,
            "max": max_budget
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
            ),
            "sleep_time": data.get("sleep_time"),
            "wake_time": data.get("wake_time")
        },

        "routine": {
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

        "room": {
            "type": data.get("room_type"),
            "sharing": data.get(
                "sharing",
                "no_preference"
            ),
            "furnished": data.get(
                "furnished",
                "no_preference"
            )
        },

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

        "matching_weights": {
            "budget": data.get(
                "weight_budget",
                5
            ),
            "location": data.get(
                "weight_location",
                5
            ),
            "food": data.get(
                "weight_food",
                3
            ),
            "smoking": data.get(
                "weight_smoking",
                5
            ),
            "drinking": data.get(
                "weight_drinking",
                3
            ),
            "cleanliness": data.get(
                "weight_cleanliness",
                5
            ),
            "sleep": data.get(
                "weight_sleep",
                5
            ),
            "privacy": data.get(
                "weight_privacy",
                4
            ),
            "social": data.get(
                "weight_social",
                3
            ),
            "noise": data.get(
                "weight_noise",
                3
            )
        }
    }

    # -------------------------
    # Save profile
    # -------------------------

    result = db.partner_profiles.insert_one(profile)

    return jsonify({
        "message": "Partner profile created successfully",
        "profile_id": str(result.inserted_id)
    }), 201


def get_partner_profiles():

    # -------------------------
    # Query parameters
    # -------------------------

    city = request.args.get("city")
    area = request.args.get("area")
    min_budget = request.args.get("min_budget")
    max_budget = request.args.get("max_budget")

    query = {}

    # -------------------------
    # Location filtering
    # -------------------------

    if city:
        query["location.city"] = city

    if area:
        query["location.area"] = area

    # -------------------------
    # Budget filtering
    # -------------------------

    if min_budget:
        query["budget.max"] = {
            "$gte": int(min_budget)
        }

    if max_budget:
        query["budget.min"] = {
            "$lte": int(max_budget)
        }

    # -------------------------
    # Find profiles
    # -------------------------

    profiles = db.partner_profiles.find(query)

    profile_list = []

    for profile in profiles:

        profile["_id"] = str(profile["_id"])

        profile_list.append(profile)

    return jsonify({
        "count": len(profile_list),
        "profiles": profile_list
    }), 200