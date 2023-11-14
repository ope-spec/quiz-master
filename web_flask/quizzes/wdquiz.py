from flask import Blueprint, render_template, request
from flask import jsonify, session, redirect, url_for
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


def fetch_from_db_wd(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wdquiz_questions WHERE id = %s",
                   (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data


@wdquiz_bp.route('/wdquiz', methods=['GET'])
def start_wdquiz():
    session['correct_answers'] = 0
    session['current_question_id_wd'] = 1
    current_question_id = get_current_question_id_wd()
    question_data = fetch_from_db_wd(current_question_id)
    total_questions = get_total_questions_wd()

    if current_question_id <= total_questions:
        return render_template('wdQuiz.html',
                               question=question_data[1],
                               options=question_data[2:6])

    return redirect(url_for('result.result', quiz='Web Development'))


@wdquiz_bp.route('/submit_wdanswer', methods=['POST'])
def submit_wdanswer():
    session['correct_answers'] = session.get('correct_answers', 0)
    user_answer = request.form.get('answer')
    current_question_id = get_current_question_id_wd()
    question_data = fetch_from_db_wd(current_question_id)
    correct_option_index = question_data[6]
    options = question_data[2:6]
    correct_option = options[correct_option_index - 1]

    print(f'User Answer: {user_answer}')
    print(f'Correct Option Index: {correct_option_index}')

    if user_answer is not None and user_answer == str(correct_option_index):
        session['correct_answers'] += 1
        print(f'Count of correct answers so far: {session["correct_answers"]}')

    session['current_question_id_wd'] = current_question_id + 1

    total_questions = get_total_questions_wd()
    if current_question_id >= total_questions:
        return redirect(url_for('result.result', quiz='Web Development'))

    next_question_data = fetch_from_db_wd(get_current_question_id_wd())
    return render_template('wdQuiz.html',
                           question=next_question_data[1],
                           options=next_question_data[2:6])
