from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from config import db_config

wdquiz_bp = Blueprint('wdquiz', __name__)

def get_current_question_id_wd():
    return session.get('current_question_id_wd', 1)

def get_total_questions_wd():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM wdquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_wd(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wdquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@wdquiz_bp.route('/wdquiz', methods=['GET'])
def start_wdquiz():
    session['current_question_id_wd'] = 1
    current_question_id = get_current_question_id_wd()
    question_data = fetch_question_from_database_wd(current_question_id)
    total_questions = get_total_questions_wd()

    if current_question_id <= total_questions:
        return render_template('wdQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result.result'))

@wdquiz_bp.route('/submit_wdanswer', methods=['POST'])
def submit_wdanswer():
    user_answer = request.args.get('answer')
    correct_option = fetch_question_from_database_wd(get_current_question_id_wd())[6]
    current_question_id = get_current_question_id_wd()
    correct_option = fetch_question_from_database_wd(current_question_id)[6]

    print(f'User Answer: {user_answer}')
    print(f'Correct Option: {correct_option}')

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_wd'] = get_current_question_id_wd() + 1

    if get_current_question_id_wd() > get_total_questions_wd():
        return redirect(url_for('result.result'))

    next_question_data = fetch_question_from_database_wd(get_current_question_id_wd())
    return render_template('wdQuiz.html', question=next_question_data[1], options=next_question_data[2:6])
    #return jsonify({'question': next_question_data[1], 'options': next_question_data[2:6]})
