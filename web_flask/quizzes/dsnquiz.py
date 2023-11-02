from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db_config
from pymongo import MongoClient

dsnquiz_bp = Blueprint('dsnquiz', __name__)

def get_total_questions_dsn():
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    total_questions = db["dsnquiz_questions"].count_documents({})
    return total_questions

def fetch_question_from_database_dsn(question_id):
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    question_data = db["dsnquiz_questions"].find_one({"id": question_id})
    return question_data

@dsnquiz_bp.route('/dsnquiz', methods=['GET', 'POST'])
def start_dsnquiz():
    current_question_id = session.get('current_question_id_dsn', 1)
    total_questions = get_total_questions_dsn()

    if current_question_id <= total_questions:
        question_data = fetch_question_from_database_dsn(current_question_id)

        if question_data:
            return render_template('dsnQuiz.html', question=question_data["question_text"], options=[
                question_data["option1"],
                question_data["option2"],
                question_data["option3"],
                question_data["option4"]
            ])
    
    if current_question_id > total_questions and total_questions > 0:
        return redirect(url_for('result.result'))
    
    return redirect(url_for('dsnquiz.start_dsnquiz'))


submit_dsnanswer = Blueprint('submit_dsnanswer', __name__)

@submit_dsnanswer.route('/dsnquiz', methods=['POST'])
def submit_dsnanswer():
    user_answer = request.form.get('answer')
    current_question_id = session.get('current_question_id_dsn', 1)
    
    if current_question_id == 1:
        correct_option = question_data["correct_option"]

        if user_answer == str(correct_option):
            session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_dsn'] = current_question_id + 1

    if current_question_id >= get_total_questions_dsn():
        return redirect(url_for('result.result'))

    return redirect(url_for('dsnquiz.start_dsnquiz'))
