from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db_config
from pymongo import MongoClient

wdquiz_bp = Blueprint('wdquiz', __name__)

def get_current_question_id_wd():
    return session.get('current_question_id_wd', 1)

def get_total_questions_wd():
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    total_questions = db["wdquiz_questions"].count_documents({})
    return total_questions

def fetch_question_from_database_wd(question_id):
    client = MongoClient(db_config["uri"])
    db = client[db_config["database"]]
    question_data = db["wdquiz_questions"].find_one({"id": question_id})
    return question_data

@wdquiz_bp.route('/wdquiz', methods=['GET', 'POST'])
def start_wdquiz():
    current_question_id = get_current_question_id_wd()
    question_data = fetch_question_from_database_wd(current_question_id)
    total_questions = get_total_questions_wd()

    if current_question_id <= total_questions:
        return render_template('wdquiz.html', question=question_data["question"], options=question_data["options"])

    return redirect(url_for('result'))

submit_wdanswer = Blueprint('submit_wdanswer', __name__)

@submit_wdanswer.route('/wdquiz', methods=['POST'])
def submit_wdanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_wd(get_current_question_id_wd())["correct_option"]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_wd'] = get_current_question_id_wd() + 1

    if get_current_question_id_wd() > get_total_questions_wd():
        return redirect(url_for('result'))

    return redirect(url_for('start_wdquiz'))
