from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db_config
from pymongo import MongoClient

dmquiz_bp = Blueprint('dmquiz', __name__)

def get_current_question_id_dm():
    return session.get('current_question_id_dm', 1)

def get_total_questions_dm():
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    total_questions = db["dmquiz_questions"].count_documents({})
    return total_questions

def fetch_question_from_database_dm(question_id):
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    question_data = db["dmquiz_questions"].find_one({"id": question_id})
    return question_data

@dmquiz_bp.route('/dmquiz', methods=['GET', 'POST'])
def start_dmquiz():
    current_question_id = get_current_question_id_dm()
    question_data = fetch_question_from_database_dm(current_question_id)
    total_questions = get_total_questions_dm()

    if current_question_id <= total_questions:
        return render_template('dmquiz.html', question=question_data["question"], options=question_data["options"])

    return redirect(url_for('result'))

submit_dmanswer = Blueprint('submit_dmanswer', __name__)

@submit_dmanswer.route('/dmquiz', methods=['POST'])
def submit_dmanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_dm(get_current_question_id_dm())["correct_option"]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_dm'] = get_current_question_id_dm() + 1

    if get_current_question_id_dm() > get_total_questions_dm():
        return redirect(url_for('result'))

    return redirect(url_for('start_dmquiz'))
