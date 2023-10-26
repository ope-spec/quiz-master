# quiz1.py

from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
   host="sql.freedb.tech",
   user="freedb_quizmaster",
   password="p%@2Z?FpvDFDx5j",
   database="freedb_quizmaster"
)

@app.route('/quiz1')
def display_quiz1():
   cursor = db.cursor()
   cursor.execute("SELECT question_id, question_text FROM quiz1_questions")
   questions = cursor.fetchall()

   return render_template('dsnQuiz.html', questions=questions)

if __name__ == '__main__':
   app.run()
