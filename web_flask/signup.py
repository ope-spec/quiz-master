from flask import Blueprint, request, redirect, url_for, flash
import mysql.connector
from config import db_config

signup_bp = Blueprint('signup', __name__)

# signup route
@signup_bp.route('/signup', methods=['POST'])
def signup_route():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Check if the email or username already exists
    cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, username))
    existing_user = cursor.fetchone()

    if existing_user:
        # User with the provided email or username already exists
        flash('Email or username already exists. Please sign in instead.', 'danger')
        return redirect(url_for('login.login_route'))
    else:
        # Insert the new user into the 'users' table
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        connection.commit()
        flash('Signup successful. You can now log in.', 'success')
        return redirect(url_for('login.login_route'))
