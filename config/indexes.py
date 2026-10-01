from config.database import db


def create_indexes():

    # -------------------------
    # Users
    # -------------------------

    db.users.create_index(
        "email",
        unique=True
    )

    # -------------------------
    # Partner Profiles
    # -------------------------

    db.partner_profiles.create_index(
        "user_id",
        unique=True
    )

    # -------------------------
    # Rooms
    # -------------------------

    db.rooms.create_index(
        "owner_id"
    )

    db.rooms.create_index(
        "status"
    )

    db.rooms.create_index(
        "location.city"
    )

    # -------------------------
    # Room Requests
    # -------------------------

    db.room_requests.create_index(
        "seeker_id"
    )

    db.room_requests.create_index(
        "owner_id"
    )

    db.room_requests.create_index(
        "room_id"
    )

    print("MongoDB indexes created successfully")