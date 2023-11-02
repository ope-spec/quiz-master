from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from config import db_config

ccquiz_bp = Blueprint('ccquiz', __name__)

def get_current_question_id_cc():
    return session.get('current_question_id_cc', 1)

def get_total_questions_cc():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM ccquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_cc(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ccquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@ccquiz_bp.route('/ccquiz', methods=['GET'])
def start_ccquiz():
    session['current_question_id_cc'] = 1
    current_question_id = get_current_question_id_cc()
    question_data = fetch_question_from_database_cc(current_question_id)
    total_questions = get_total_questions_cc()

    if current_question_id <= total_questions:
        return render_template('ccQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result.result'))

@ccquiz_bp.route('/submit_ccanswer', methods=['POST'])
def submit_ccanswer():
    user_answer = request.args.get('answer')
    correct_option = fetch_question_from_database_cc(get_current_question_id_cc())[6]
    current_question_id = get_current_question_id_cc()
    correct_option = fetch_question_from_database_cc(current_question_id)[6]

    print(f'User Answer: {user_answer}')
    print(f'Correct Option: {correct_option}')

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_cc'] = get_current_question_id_cc() + 1

    if get_current_question_id_cc() > get_total_questions_cc():
        return redirect(url_for('result.result'))

    next_question_data = fetch_question_from_database_cc(get_current_question_id_cc())
    return render_template('ccQuiz.html', question=next_question_data[1], options=next_question_data[2:6])
    #return jsonify({'question': next_question_data[1], 'options': next_question_data[2:6]})
