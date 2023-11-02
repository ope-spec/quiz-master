from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db_config
from pymongo import MongoClient

ccquiz_bp = Blueprint('ccquiz', __name__)

def get_current_question_id_cc():
    return session.get('current_question_id_cc', 1)

def get_total_questions_cc():
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    total_questions = db["ccquiz_questions"].count_documents({})
    return total_questions

def fetch_question_from_database_cc(question_id):
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    question_data = db["ccquiz_questions"].find_one({"id": question_id})
    return question_data

@ccquiz_bp.route('/cloud-computing', methods=['GET', 'POST'])
def start_ccquiz():
    current_question_id = get_current_question_id_cc()
    question_data = fetch_question_from_database_cc(current_question_id)
    total_questions = get_total_questions_cc()

    if current_question_id <= total_questions:
        return render_template('ccquiz.html', question=question_data["question"], options=question_data["options"])

    return redirect(url_for('result'))

submit_ccanswer = Blueprint('submit_ccanswer', __name__)

@submit_ccanswer.route('/cloud-computing', methods=['POST'])
def submit_ccanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_cc(get_current_question_id_cc())["correct_option"]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_cc'] = get_current_question_id_cc() + 1

    if get_current_question_id_cc() > get_total_questions_cc():
        return redirect(url_for('result'))

    return redirect(url_for('start_ccquiz'))
