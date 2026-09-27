from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config.database import db
from utils.matching import (
    categorical_match,
    numerical_similarity,
    sleep_similarity,
    preference_match
)

matching_bp = Blueprint(
    "matching",
    __name__,
    url_prefix="/api/matching"
)


@matching_bp.route("/rooms", methods=["GET"])
@jwt_required()
def find_matching_rooms():

    user_id = get_jwt_identity()

    # -------------------------
    # Find logged-in seeker's profile
    # -------------------------

    seeker = db.partner_profiles.find_one({
        "user_id": user_id
    })

    if not seeker:
        return jsonify({
            "message": "Partner profile not found"
        }), 404

    # -------------------------
    # Basic filtering
    # -------------------------

    city = seeker["location"]["city"]
    area = seeker["location"]["area"]

    min_budget = seeker["budget"]["min"]
    max_budget = seeker["budget"]["max"]

    rooms = db.rooms.find({
        "status": "available",
        "location.city": city,
        "budget.rent": {
            "$gte": min_budget,
            "$lte": max_budget
        }
    })

    matches = []

    # -------------------------
    # Calculate compatibility
    # -------------------------

    for room in rooms:

        owner_lifestyle = room.get("lifestyle", {})
        owner_personality = room.get("personality", {})

        seeker_lifestyle = seeker.get("lifestyle", {})
        seeker_personality = seeker.get("personality", {})

        # -------------------------
        # Lifestyle matching
        # -------------------------

        food_score = categorical_match(
            seeker_lifestyle.get("food"),
            owner_lifestyle.get("food")
        )

        smoking_score = categorical_match(
            seeker_lifestyle.get("smoking"),
            owner_lifestyle.get("smoking")
        )

        drinking_score = categorical_match(
            seeker_lifestyle.get("drinking"),
            owner_lifestyle.get("drinking")
        )

        # -------------------------
        # Personality matching
        # -------------------------

        cleanliness_score = numerical_similarity(
            seeker_personality.get("cleanliness"),
            owner_personality.get("cleanliness")
        )

        social_score = numerical_similarity(
            seeker_personality.get("social_level"),
            owner_personality.get("social_level")
        )

        noise_score = numerical_similarity(
            seeker_personality.get("noise_tolerance"),
            owner_personality.get("noise_tolerance")
        )

        privacy_score = numerical_similarity(
            seeker_personality.get("privacy"),
            owner_personality.get("privacy")
        )

        # -------------------------
        # Sleep matching
        # -------------------------

        sleep_score = sleep_similarity(
            seeker_lifestyle.get("sleep_time"),
            owner_lifestyle.get("sleep_time")
        )

        # -------------------------
        # Guest and Pet matching
        # -------------------------

        guest_score = preference_match(
            seeker.get("guests"),
            room.get("guests")
        )

        pet_score = preference_match(
            seeker.get("pets"),
            room.get("pets")
        )

        # -------------------------
        # Matching weights
        # -------------------------

        weights = seeker.get("matching_weights", {})

        # -------------------------
        # Calculate weighted score
        # -------------------------

        weighted_score = (
            food_score * weights.get("food", 3)
            + smoking_score * weights.get("smoking", 5)
            + drinking_score * weights.get("drinking", 3)

            + cleanliness_score * weights.get("cleanliness", 5)
            + social_score * weights.get("social", 3)
            + noise_score * weights.get("noise", 3)
            + privacy_score * weights.get("privacy", 4)

            + sleep_score * weights.get("sleep", 5)

            + guest_score * 3
            + pet_score * 3
        )

        # -------------------------
        # Total possible weight
        # -------------------------

        total_weight = (
            weights.get("food", 3)
            + weights.get("smoking", 5)
            + weights.get("drinking", 3)

            + weights.get("cleanliness", 5)
            + weights.get("social", 3)
            + weights.get("noise", 3)
            + weights.get("privacy", 4)

            + weights.get("sleep", 5)

            + 3    # guests
            + 3    # pets
        )

        # -------------------------
        # Convert to percentage
        # -------------------------

        compatibility_score = round(
            (weighted_score / total_weight) * 100,
            2
        )

        # -------------------------
        # Convert MongoDB ObjectId
        # -------------------------

        room["_id"] = str(room["_id"])

        # -------------------------
        # Store match
        # -------------------------

        matches.append({
            "room": room,
            "compatibility_score": compatibility_score
        })

    # -------------------------
    # Highest compatibility first
    # -------------------------

    matches.sort(
        key=lambda x: x["compatibility_score"],
        reverse=True
    )

    return jsonify({
        "count": len(matches),
        "matches": matches
    }), 200