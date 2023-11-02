from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db_config
import mysql.connector

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[1]
            flash('Login successful', 'success')
            connection.close()
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
        print(f"SQL Query: SELECT * FROM users WHERE email = {email} AND password = {password}")

    return render_template('login.html')
