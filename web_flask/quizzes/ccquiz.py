from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector
from config import db_config

ccquiz_bp = Blueprint('ccquiz', __name__)

def get_db_connection():
    return mysql.connector.connect(**db_config)

def fetch_question_from_database_cc(question_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ccquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

def get_total_questions_cc():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM ccquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def get_current_question_id_cc():
    return session.get('current_question_id_cc', 1)

@ccquiz_bp.route('/cloud-computing', methods=['GET', 'POST'])
def start_ccquiz():
    current_question_id = int(request.args.get('question_id', 1))
    question_data = fetch_question_from_database_cc(current_question_id)
    total_questions = get_total_questions_cc()

    if current_question_id <= total_questions:
        return render_template('ccQuiz.html', question=question_data[1], options=question_data[2:6], question_id=current_question_id)

    return redirect(url_for('result'))

submit_ccanswer = Blueprint('submit_ccanswer', __name__)

@submit_ccanswer.route('/cloud-computing', methods=['POST'])
def submit_ccanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_cc(get_current_question_id_cc())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    current_question_id = get_current_question_id_cc() + 1

    if current_question_id > get_total_questions_cc():
        return redirect(url_for('result'))

    return redirect(url_for('start_ccquiz', question_id=current_question_id))
