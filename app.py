import json
import os
import certifi
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.get_database("assignment_db")
submissions_collection = db.user_submissions
todo_collection = db.todo_items

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/api", methods=["GET"])
def get_api():
    try:
        with open("data.json", "r") as f:
            return jsonify(json.load(f)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    
    submissions_collection.insert_one({
        "name": name,
        "email": email,
        "message": message
    })
    return render_template("success.html", name=name)

@app.route("/todo", methods=["GET"])
def todo_page():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_id = request.form.get("itemID")
    item_uuid = request.form.get("itemUUID")
    item_hash = request.form.get("itemHash")
    item_name = request.form.get("itemName")
    item_desc = request.form.get("itemDescription")

    todo_doc = {
        "itemID": item_id,
        "itemUUID": item_uuid,
        "itemHash": item_hash,
        "itemName": item_name,
        "itemDescription": item_desc
    }
    todo_collection.insert_one(todo_doc)
    return render_template("success.html", name=item_name)

# app.run MUST be at the very end
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)