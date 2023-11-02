from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db_config
import mysql.connector

csyquiz_bp = Blueprint('csyquiz', __name__)

# Define session variables and route handlers for the Cloud Computing quiz here
def get_current_question_id_csy():
    return session.get('current_question_id_csy', 1)

def get_total_questions_csy():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM csyquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_csy(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM csyquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@csyquiz_bp.route('/csyquiz', methods=['GET'])
def start_csyquiz():
    current_question_id = get_current_question_id_csy()
    question_data = fetch_question_from_database_csy(current_question_id)
    total_questions = get_total_questions_csy()

    if current_question_id <= total_questions:
        return render_template('csyQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@csyquiz_bp.route('/csyquiz', methods=['POST'])
def submit_csyanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_csy(get_current_question_id_csy())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_csy'] = get_current_question_id_csy() + 1

    if get_current_question_id_csy() > get_total_questions_csy():
        return redirect(url_for('result'))

    return redirect(url_for('start_csyquiz'))
