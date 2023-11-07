from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from config import db_config

csyquiz_bp = Blueprint('csyquiz', __name__)

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
    session['current_question_id_csy'] = 1
    current_question_id = get_current_question_id_csy()
    question_data = fetch_question_from_database_csy(current_question_id)
    total_questions = get_total_questions_csy()

    if current_question_id <= total_questions:
        return render_template('csyQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result.result', quiz='Cybersecurity'))

@csyquiz_bp.route('/submit_csyanswer', methods=['POST'])
def submit_csyanswer():
    user_answer = request.args.get('answer')
    current_question_id = get_current_question_id_csy()
    question_data = fetch_question_from_database_csy(current_question_id)
    correct_option_index = question_data[6] - 1  # Adjust for 0-based indexing
    options = question_data[2:6]
    correct_option = options[correct_option_index]

    print(f'User Answer: {user_answer}')
    print(f'Correct Option: {correct_option}')

    if user_answer == str(correct_option_index + 1):  # Compare user's answer to the correct option index
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_csy'] = get_current_question_id_csy() + 1

    total_questions = get_total_questions_csy()
    if get_current_question_id_csy() > total_questions:
        return redirect(url_for('result.result', quiz='Cybersecurity'))

    next_question_data = fetch_question_from_database_csy(get_current_question_id_csy())
    return render_template('csyQuiz.html', question=next_question_data[1], options=next_question_data[2:6])
