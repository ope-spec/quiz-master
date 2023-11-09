from flask import Blueprint, render_template, request, session
import mysql.connector
from config import db_config
from datetime import datetime

result_bp = Blueprint('result', __name__)

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

    # Render result_history.html regardless of the result of the quiz
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT qr.quiz_date, qr.score, qr.quiz_identifier " \
            "FROM quiz_results qr " \
            "WHERE qr.user_id = %s " \
            "ORDER BY qr.quiz_date DESC"
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    connection.close()

    return render_template('result_history.html', results=results, user_id=user_id)
