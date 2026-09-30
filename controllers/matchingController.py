from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from config.database import db
from utils.matching import (
    categorical_match,
    numerical_similarity,
    sleep_similarity,
    preference_match,
    age_match,
    gender_match
)


def find_matching_rooms():

    user_id = get_jwt_identity()

    # -------------------------
    # Find seeker's profile
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
    # Process each room
    # -------------------------

    for room in rooms:

        owner_lifestyle = room.get("lifestyle", {})
        owner_personality = room.get("personality", {})

        seeker_lifestyle = seeker.get("lifestyle", {})
        seeker_personality = seeker.get("personality", {})

        owner_partner_preference = room.get(
            "partner_preference",
            {}
        )

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
        # Guest / Pet matching
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
        # Owner's preferences
        # -------------------------

        seeker_age = seeker["basic"]["age"]
        seeker_gender = seeker["basic"]["gender"]

        gender_score = gender_match(
            seeker_gender,
            owner_partner_preference.get(
                "gender",
                "no_preference"
            )
        )

        age_score = age_match(
            seeker_age,
            owner_partner_preference.get("age_min"),
            owner_partner_preference.get("age_max")
        )

        preferred_food_score = categorical_match(
            seeker_lifestyle.get("food"),
            owner_partner_preference.get(
                "food",
                "no_preference"
            )
        )

        preferred_smoking_score = categorical_match(
            seeker_lifestyle.get("smoking"),
            owner_partner_preference.get(
                "smoking",
                "no_preference"
            )
        )

        preferred_drinking_score = categorical_match(
            seeker_lifestyle.get("drinking"),
            owner_partner_preference.get(
                "drinking",
                "no_preference"
            )
        )

        # -------------------------
        # Matching weights
        # -------------------------

        weights = seeker.get(
            "matching_weights",
            {}
        )

        # -------------------------
        # Weighted score
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

            + gender_score * 4
            + age_score * 3
            + preferred_food_score * 3
            + preferred_smoking_score * 5
            + preferred_drinking_score * 3
        )

        # -------------------------
        # Total weight
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

            + 3      # guests
            + 3      # pets

            + 4      # gender
            + 3      # age
            + 3      # food preference
            + 5      # smoking preference
            + 3      # drinking preference
        )

        # -------------------------
        # Compatibility percentage
        # -------------------------

        compatibility_score = round(
            (weighted_score / total_weight) * 100,
            2
        )

        # Convert ObjectId to string
        room["_id"] = str(room["_id"])

        matches.append({
            "room": room,
            "compatibility_score": compatibility_score
        })

    # -------------------------
    # Sort highest score first
    # -------------------------

    matches.sort(
        key=lambda x: x["compatibility_score"],
        reverse=True
    )

    return jsonify({
        "count": len(matches),
        "matches": matches
    }), 200