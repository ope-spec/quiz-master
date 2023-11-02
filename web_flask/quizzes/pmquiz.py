from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db_config
from pymongo import MongoClient

pmquiz_bp = Blueprint('pmquiz', __name__)

def get_current_question_id_pm():
    return session.get('current_question_id_pm', 1)

def get_total_questions_pm():
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    total_questions = db["pmquiz_questions"].count_documents({})
    return total_questions

def fetch_question_from_database_pm(question_id):
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    question_data = db["pmquiz_questions"].find_one({"id": question_id})
    return question_data

@pmquiz_bp.route('/pmquiz', methods=['GET', 'POST'])
def start_pmquiz():
    current_question_id = get_current_question_id_pm()
    question_data = fetch_question_from_database_pm(current_question_id)
    total_questions = get_total_questions_pm()

    if current_question_id <= total_questions:
        return render_template('pmquiz.html', question=question_data["question"], options=question_data["options"])

    return redirect(url_for('result'))

submit_pmanswer = Blueprint('submit_pmanswer', __name__)

@submit_pmanswer.route('/pmquiz', methods=['POST'])
def submit_pmanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_pm(get_current_question_id_pm())["correct_option"]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_pm'] = get_current_question_id_pm() + 1

    if get_current_question_id_pm() > get_total_questions_pm():
        return redirect(url_for('result'))

    return redirect(url_for('start_pmquiz'))
