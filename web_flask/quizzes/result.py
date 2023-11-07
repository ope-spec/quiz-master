from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db_config
import mysql.connector
from datetime import datetime

result_bp = Blueprint('result', __name__)

# Dynamic route to display quiz results for different quizzes
@result_bp.route('/result/<quiz>', methods=['GET'])
def result(quiz):
    correct_answers = session.get('correct_answers', 0)
    total_questions = 10
    incorrect_answers = total_questions - correct_answers if total_questions > correct_answers else 0
    score = round((correct_answers / total_questions) * 100, 1)

    result_data = {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'score': score
    }

    user_id = session.get('user_id')
    print(f'Score: {score}')

    if user_id is not None:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            # Generate a timestamp with seconds only
            now = datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            print(f'Score: {score}')

            insert_query = "INSERT INTO quiz_results (user_id, score, quiz_date, quiz_identifier) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (user_id, score, timestamp, quiz))
            connection.commit()
        except Exception as e:
            connection.rollback()
        finally:
            connection.close()

    return render_template('result.html', result=result_data, user_id=user_id, quiz=quiz)
