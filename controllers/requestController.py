from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from utils.validator import is_valid_object_id
from config.database import db


def send_request():

    seeker_id = get_jwt_identity()
    data = request.get_json()

    room_id = data.get("room_id")

    # -------------------------
    # Validate room_id
    # -------------------------

    if not room_id:
        return jsonify({
            "message": "room_id is required"
        }), 400

    # -------------------------
    # Find available room
    # -------------------------
    if not is_valid_object_id(room_id):
        return jsonify({
            "message": "Invalid room_id"
        }), 400
    
    room = db.rooms.find_one({
        "_id": ObjectId(room_id),
        "status": "available"
    })

    if not room:
        return jsonify({
            "message": "Room not found or unavailable"
        }), 404

    # -------------------------
    # Check duplicate request
    # -------------------------

    existing_request = db.room_requests.find_one({
        "room_id": room_id,
        "seeker_id": seeker_id
    })

    if existing_request:
        return jsonify({
            "message": "Request already sent"
        }), 409

    # -------------------------
    # Create request
    # -------------------------

    room_request = {
        "room_id": room_id,
        "owner_id": room["owner_id"],
        "seeker_id": seeker_id,
        "status": "pending"
    }

    result = db.room_requests.insert_one(
        room_request
    )

    return jsonify({
        "message": "Room request sent successfully",
        "request_id": str(result.inserted_id)
    }), 201

def send_request():

    seeker_id = get_jwt_identity()

    # Convert JWT string ID to ObjectId
    if not ObjectId.is_valid(seeker_id):
        return jsonify({
            "message": "Invalid user ID"
        }), 400

    seeker_id = ObjectId(seeker_id)

    data = request.get_json()
    room_id = data.get("room_id")

    # -------------------------
    # Validate room_id
    # -------------------------

    if not room_id:
        return jsonify({
            "message": "room_id is required"
        }), 400

    if not ObjectId.is_valid(room_id):
        return jsonify({
            "message": "Invalid room_id"
        }), 400

    room_id = ObjectId(room_id)

    # -------------------------
    # Find available room
    # -------------------------

    room = db.rooms.find_one({
        "_id": room_id,
        "status": "available"
    })

    if not room:
        return jsonify({
            "message": "Room not found or unavailable"
        }), 404

    # -------------------------
    # Check duplicate request
    # -------------------------

    existing_request = db.room_requests.find_one({
        "room_id": room_id,
        "seeker_id": seeker_id
    })

    if existing_request:
        return jsonify({
            "message": "Request already sent"
        }), 409

    # -------------------------
    # Create request
    # -------------------------

    room_request = {
        "room_id": room_id,
        "owner_id": room["owner_id"],
        "seeker_id": seeker_id,
        "status": "pending"
    }

    result = db.room_requests.insert_one(
        room_request
    )

    return jsonify({
        "message": "Room request sent successfully",
        "request_id": str(result.inserted_id)
    }), 201
    
def update_request(request_id):

    owner_id = get_jwt_identity()

    if not ObjectId.is_valid(owner_id):
        return jsonify({
            "message": "Invalid user ID"
        }), 400

    owner_id = ObjectId(owner_id)

    data = request.get_json()
    status = data.get("status")

    # -------------------------
    # Validate status
    # -------------------------

    if status not in ["accepted", "rejected"]:
        return jsonify({
            "message": "Status must be accepted or rejected"
        }), 400

    # -------------------------
    # Validate request ID
    # -------------------------

    if not ObjectId.is_valid(request_id):
        return jsonify({
            "message": "Invalid request_id"
        }), 400

    request_id = ObjectId(request_id)

    # -------------------------
    # Find request
    # -------------------------

    room_request = db.room_requests.find_one({
        "_id": request_id
    })

    if not room_request:
        return jsonify({
            "message": "Request not found"
        }), 404

    # -------------------------
    # Authorization
    # -------------------------

    if room_request["owner_id"] != owner_id:
        return jsonify({
            "message": "You are not authorized to update this request"
        }), 403

    # -------------------------
    # Update status
    # -------------------------

    db.room_requests.update_one(
        {
            "_id": request_id
        },
        {
            "$set": {
                "status": status
            }
        }
    )

    return jsonify({
        "message": f"Request {status} successfully"
    }), 200
    
    
def get_sent_requests():

    seeker_id = get_jwt_identity()

    if not ObjectId.is_valid(seeker_id):
        return jsonify({
            "message": "Invalid user ID"
        }), 400

    seeker_id = ObjectId(seeker_id)

    requests = db.room_requests.find({
        "seeker_id": seeker_id
    })

    request_list = []

    for req in requests:

        req["_id"] = str(req["_id"])
        req["room_id"] = str(req["room_id"])
        req["owner_id"] = str(req["owner_id"])
        req["seeker_id"] = str(req["seeker_id"])

        request_list.append(req)

    return jsonify({
        "count": len(request_list),
        "requests": request_list
    }), 200
 
def get_received_requests():

    owner_id = get_jwt_identity()

    if not ObjectId.is_valid(owner_id):
        return jsonify({
            "message": "Invalid user ID"
        }), 400

    owner_id = ObjectId(owner_id)

    requests = db.room_requests.find({
        "owner_id": owner_id
    })

    request_list = []

    for req in requests:

        req["_id"] = str(req["_id"])
        req["room_id"] = str(req["room_id"])
        req["owner_id"] = str(req["owner_id"])
        req["seeker_id"] = str(req["seeker_id"])

        request_list.append(req)

    return jsonify({
        "count": len(request_list),
        "requests": request_list
    }), 200