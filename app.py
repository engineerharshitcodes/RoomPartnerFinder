from flask import Flask, jsonify
from flask_cors import CORS
from config.database import db
from routers.auth import auth_bp
from flask_jwt_extended import JWTManager
from routers.rooms import rooms_bp
from routers.matching import matching_bp
from routers.partners import partners_bp
from routers.requests import requests_bp
from config.indexes import create_indexes


app = Flask(__name__)
create_indexes()

CORS(app)

app.config["JWT_SECRET_KEY"] = "change_this_later"
jwt = JWTManager(app)

# Register authentication routes
app.register_blueprint(auth_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(partners_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(requests_bp)

@app.route("/")
def home():
    return jsonify({
        "message": "Room Partner Finder API is running",
        "database": "MongoDB"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)