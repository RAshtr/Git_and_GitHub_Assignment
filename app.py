import os
import json
import logging
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)

# Securely retrieve URI from environment
MONGO_URI = os.getenv("MONGO_URI")

client = None
if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        db = client["devops_assignment_db"]
        collection = db["submissions"]
        logging.info("MongoDB client configured successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize MongoDB client: {e}")
else:
    logging.warning("MONGO_URI is not defined in environment variables.")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for container orchestrators and monitoring."""
    return jsonify({"status": "healthy", "service": "flask-mongodb-app"}), 200

@app.route('/api', methods=['GET'])
def get_api_data():
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data.json')
        with open(data_path, 'r') as file:
            data = json.load(file)
        logging.info("Fetched /api data successfully.")
        return jsonify(data), 200
    except Exception as e:
        logging.error(f"Error loading data.json: {e}")
        return jsonify({"error": "Failed to read backend data file", "details": str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()

        if not name or not email or not course:
            logging.warning("Form validation failed: Missing fields.")
            return render_template('form.html', error="All fields are required. Please fill out the full form.")

        try:
            if client is None:
                raise ConnectionFailure("Could not connect to database backend.")
            
            client.admin.command('ping')

            submission_data = {
                "name": name,
                "email": email,
                "course": course
            }
            collection.insert_one(submission_data)
            logging.info(f"Successfully inserted submission for: {email}")
            return redirect(url_for('success_page'))

        except (ConnectionFailure, PyMongoError, Exception) as err:
            logging.error(f"Database insertion failure: {err}")
            return render_template('form.html', error=f"Database Error: {str(err)}")

    return render_template('form.html', error=None)

@app.route('/success')
def success_page():
    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

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