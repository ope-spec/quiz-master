from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import db_config
from pymongo import MongoClient
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__)

# MongoDB connection
client = MongoClient(db_config["uri"])
db = client[db_config["database"]]
users_collection = db["users"]

# Define the login route
@login_bp.route('/', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session['username'] = user["username"]
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
            print(f"MongoDB Query: Find user with email = {email}")

    return render_template('login.html')
