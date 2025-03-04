!/usr/bin/env python3
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["french_course"]
users_collection = db["users"]

# User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")  # In production, hash passwords using bcrypt
    plan = data.get("plan")

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    user = {
        "email": email,
        "password": password,
        "plan": plan,
        "subscription_status": "active"
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email, "password": password})
    if user:
        return jsonify({"message": "Login successful", "plan": user["plan"]}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Check Subscription Status
@app.route("/check-subscription", methods=["POST"])
def check_subscription():
    data = request.json
    email = data.get("email")

    user = users_collection.find_one({"email": email})
    if user and user["subscription_status"] == "active":
        return jsonify({"message": "Subscription active", "plan": user["plan"]}), 200
    else:
        return jsonify({"error": "Subscription inactive or user not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
