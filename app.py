import json
import logging
import os
import certifi
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

load_dotenv()

app = Flask(__name__)

# Secure MongoDB Atlas connection using certifi CA bundle
MONGO_URI = os.getenv("MONGO_URI")
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client.get_database("student_assignment_db")
    collection = db.user_submissions
    logging.info("Connected to MongoDB Atlas successfully.")
except Exception as err:
    logging.error("MongoDB Atlas connection initialization failed: %s", err)
    client = None
    collection = None

# Health Check Route
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "UP", "message": "Service is healthy"}), 200

# Task 1: JSON API route reading from backend data.json file
@app.route("/api", methods=["GET"])
def get_api_data():
    try:
        data_file_path = os.path.join(os.path.dirname(__file__), "data.json")
        with open(data_file_path, "r") as file:
            items = json.load(file)
        logging.info("Read %d records from data.json", len(items))
        return jsonify(items), 200
    except FileNotFoundError:
        logging.error("data.json file not found.")
        return jsonify({"error": "Backend data file not found"}), 404
    except Exception as err:
        logging.error("Failed to read data.json: %s", err)
        return jsonify({"error": "Internal server error"}), 500

# Task 2: Home Route (Frontend Form UI)
@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

# Task 2: Form Submission Handling with Validation and Error Safety
@app.route("/submit", methods=["POST"])
def submit():
    user_name = request.form.get("name", "").strip()
    user_email = request.form.get("email", "").strip()
    user_message = request.form.get("message", "").strip()

    # Input validation: check for empty fields
    if not user_name or not user_email or not user_message:
        logging.warning("Validation failed: empty field submitted.")
        return render_template(
            "form.html",
            error="All fields are required. Please fill in your name, email, and message.",
            name=user_name,
            email=user_email,
            message=user_message,
        ), 400

    # Basic email format check
    if "@" not in user_email or "." not in user_email:
        logging.warning("Validation failed: invalid email format (%s).", user_email)
        return render_template(
            "form.html",
            error="Please enter a valid email address.",
            name=user_name,
            email=user_email,
            message=user_message,
        ), 400

    if collection is None:
        logging.error("Database unavailable during submission.")
        return render_template(
            "form.html",
            error="Database service unavailable. Please try again later.",
            name=user_name,
            email=user_email,
            message=user_message,
        ), 500

    try:
        submission_data = {
            "name": user_name,
            "email": user_email,
            "message": user_message
        }
        collection.insert_one(submission_data)
        logging.info("Inserted submission for: %s", user_email)
        # On success: render success page with user details
        return render_template("success.html", name=user_name)

    except Exception as err:
        logging.error("MongoDB insertion error: %s", err)
        # On error: display error on the same page without redirecting
        return render_template(
            "form.html",
            error="Failed to save your submission to database. Please try again.",
            name=user_name,
            email=user_email,
            message=user_message,
        ), 500

<<<<<<< Updated upstream
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
<<<<<<< HEAD

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_desc = request.form.get('itemDescription')
    
    if not item_name or not item_desc:
        return jsonify({"error": "Item Name and Description are required"}), 400
    
    if client is not None:
        todos_col = db["todos"]
        todos_col.insert_one({
            "itemName": item_name,
            "itemDescription": item_desc
        })
    
    return jsonify({
        "status": "success",
        "message": "To-Do item stored successfully in MongoDB Atlas"
    }), 201
=======
=======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
>>>>>>> Stashed changes
>>>>>>> RAshtr
