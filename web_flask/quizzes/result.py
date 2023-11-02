from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db_config
import mysql.connector

result_bp = Blueprint('result', __name__)

# Route to display quiz results
@result_bp.route('/result', methods=['GET'])
def result():
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    result_data = {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': total_questions - correct_answers,
        'score': score
    }

    return render_template('result.html', result=result_data)
