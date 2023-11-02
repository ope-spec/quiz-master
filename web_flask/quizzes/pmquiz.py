from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector
from config import db_config

pmquiz_bp = Blueprint('pmquiz', __name__)

def get_current_question_id_pm():
    return session.get('current_question_id_pm', 1)

def get_total_questions_pm():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM pmquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_pm(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pmquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@pmquiz_bp.route('/pmquiz', methods=['GET', 'POST'])
def start_pmquiz():
    current_question_id = get_current_question_id_pm()
    question_data = fetch_question_from_database_pm(current_question_id)
    total_questions = get_total_questions_pm()

    if current_question_id <= total_questions:
        return render_template('pmQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))


submit_pmanswer = Blueprint('submit_pmanswer', __name__)

@submit_pmanswer.route('/pmquiz', methods=['POST'])
def submit_pmanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_pm(get_current_question_id_pm())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_pm'] = get_current_question_id_pm() + 1

    if get_current_question_id_pm() > get_total_questions_pm():
        return redirect(url_for('result'))

    return redirect(url_for('start_pmquiz'))
