from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db_config
from pymongo import MongoClient

csyquiz_bp = Blueprint('csyquiz', __name__)

def get_current_question_id_csy():
    return session.get('current_question_id_csy', 1)

def get_total_questions_csy():
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    total_questions = db["csyquiz_questions"].count_documents({})
    return total_questions

def fetch_question_from_database_csy(question_id):
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    question_data = db["csyquiz_questions"].find_one({"id": question_id})
    return question_data

@csyquiz_bp.route('/csyquiz', methods=['GET', 'POST'])
def start_csyquiz():
    current_question_id = get_current_question_id_csy()
    question_data = fetch_question_from_database_csy(current_question_id)
    total_questions = get_total_questions_csy()

    if current_question_id <= total_questions:
        return render_template('csyquiz.html', question=question_data["question"], options=question_data["options"])

    return redirect(url_for('result'))

submit_csyanswer = Blueprint('submit_csyanswer', __name__)

@submit_csyanswer.route('/csyquiz', methods=['POST'])
def submit_csyanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_csy(get_current_question_id_csy())["correct_option"]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_csy'] = get_current_question_id_csy() + 1

    if get_current_question_id_csy() > get_total_questions_csy():
        return redirect(url_for('result'))

    return redirect(url_for('start_csyquiz'))
