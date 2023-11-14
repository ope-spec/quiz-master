from flask import Blueprint, render_template, request
from flask import jsonify, session, redirect, url_for
import mysql.connector
from config import db_config


result_history_bp = Blueprint('result_history', __name__)


@result_history_bp.route('/result_history/<int:user_id>')
def result_history(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT qr.quiz_date, qr.score, qr.quiz_identifier " \
            "FROM quiz_results qr " \
            "WHERE qr.user_id = %s " \
            "ORDER BY qr.quiz_date DESC"
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    return render_template('result_history.html', results=results)
