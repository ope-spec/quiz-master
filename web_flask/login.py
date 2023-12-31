from flask import Blueprint, render_template, request
from flask import redirect, url_for, flash, session
import mysql.connector
from config import db_config

login_bp = Blueprint('login', __name__)


# Define the login route
@login_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[1]
            session['user_id'] = user[0]
            connection.close()
            return redirect(url_for('quiz_master'))

        else:
            flash('Login failed. Please check your credentials.', 'danger')
        print(f"SQL Query: SELECT * FROM users "
              f"WHERE email = {email} AND password = {password}")

    return render_template('login.html')
