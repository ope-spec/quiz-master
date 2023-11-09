import mysql.connector
from config import db_config
from datetime import datetime

def update_result_in_db(user_id, correct_answers, total_questions, quiz):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Generate a timestamp with seconds only
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        score_for_db = round((correct_answers / total_questions) * 100, 1)

        insert_query = "INSERT INTO quiz_results (user_id, score, quiz_date, quiz_identifier) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (user_id, score_for_db, timestamp, quiz))
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        connection.close()
