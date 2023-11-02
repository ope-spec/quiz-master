from flask import Blueprint, request, redirect, url_for, flash
from config import db_config
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

signup_bp = Blueprint('signup', __name__)

# MongoDB connection
client = MongoClient(db_config["uri"])
db = client[db_config["database"]]
users_collection = db["users"]

# signup route
@signup_bp.route('/signup', methods=['POST'])
def signup_route():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email or username already exists
    existing_user = users_collection.find_one({"$or": [{"email": email}, {"username": username}]})

    if existing_user:
        # User with the provided email or username already exists
        flash('Email or username already exists. Please sign in instead.', 'danger')
        return redirect(url_for('login.login_route'))

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)

    # Insert the new user into the 'users' collection
    new_user = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    users_collection.insert_one(new_user)

    flash('Signup successful. You can now log in.', 'success')
    return redirect(url_for('login.login_route'))
