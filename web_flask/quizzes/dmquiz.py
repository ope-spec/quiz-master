from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from config import db_config

dmquiz_bp = Blueprint('dmquiz', __name__)

def get_current_question_id_dm():
    return session.get('current_question_id_dm', 1)

def get_total_questions_dm():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM dmquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_dm(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dmquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@dmquiz_bp.route('/dmquiz', methods=['GET'])
def start_dmquiz():
    session['current_question_id_dm'] = 1
    current_question_id = get_current_question_id_dm()
    question_data = fetch_question_from_database_dm(current_question_id)
    total_questions = get_total_questions_dm()

    if current_question_id <= total_questions:
        return render_template('dmQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result.result'))

@dmquiz_bp.route('/submit_dmanswer', methods=['POST'])
def submit_dmanswer():
    user_answer = request.args.get('answer')
    correct_option = fetch_question_from_database_dm(get_current_question_id_dm())[6]
    current_question_id = get_current_question_id_dm()
    correct_option = fetch_question_from_database_dm(current_question_id)[6]

    print(f'User Answer: {user_answer}')
    print(f'Correct Option: {correct_option}')

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_dm'] = get_current_question_id_dm() + 1

    if get_current_question_id_dm() > get_total_questions_dm():
        return redirect(url_for('result.result'))

    next_question_data = fetch_question_from_database_dm(get_current_question_id_dm())
    return render_template('dmQuiz.html', question=next_question_data[1], options=next_question_data[2:6])
    #return jsonify({'question': next_question_data[1], 'options': next_question_data[2:6]})
