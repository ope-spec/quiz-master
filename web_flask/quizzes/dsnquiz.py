from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector
from config import db_config

dsnquiz_bp = Blueprint('dsnquiz', __name__)

def get_current_question_id_dsn():
    return session.get('current_question_id_dsn', 1)

def get_total_questions_dsn():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM dsnquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_dsn(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dsnquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@dsnquiz_bp.route('/dsnquiz', methods=['GET', 'POST'])
def start_dsnquiz():
    current_question_id = get_current_question_id_dsn()
    question_data = fetch_question_from_database_dsn(current_question_id)
    total_questions = get_total_questions_dsn()

    if current_question_id <= total_questions:
        return render_template('dsnQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))


submit_dsnanswer = Blueprint('submit_dsnanswer', __name__)

@submit_dsnanswer.route('/dsnquiz', methods=['POST'])
def submit_dsnanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_dsn(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_dsn'] = get_current_question_id_dsn() + 1

    if get_current_question_id_dsn() > get_total_questions_dsn():
        return redirect(url_for('result'))

    return redirect(url_for('start_dsnquiz'))
