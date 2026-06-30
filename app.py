import os
from os import listdir
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["DocuTrustDB"]
users_collection = db["users"]


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({
            "email": email,
            "password": password
        })

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Email or Password!"

    return render_template("login.html")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = {
            "username": username,
            "email": email,
            "password": password
        }

        users_collection.insert_one(user)
        return "User Registered Successfully!"

    return render_template("signup.html")
 # Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["document"]

        if file:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

    files = listdir(app.config["UPLOAD_FOLDER"])

    return render_template("upload.html", files=files)
@app.route("/logout")
def logout():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)