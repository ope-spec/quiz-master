from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import flash
from flask import jsonify
import mysql.connector
import secrets

app = Flask(__name__)

app.config['SERVER_NAME'] = '127.0.0.1:5000'

# Generate a secret key
secret_key = secrets.token_hex(16)

# Set the secret key
app.secret_key = secret_key

# MySQL database connection configuration
db_config = {
    "host": "sql.freedb.tech",
    "user": "freedb_quizmaster",
    "password": "p%@2Z?FpvDFDx5j",
    "database": "freedb_quizmaster"
}

# Define a route for the login and signup page


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check the credentials in the 'users' table
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[1]
            # Successful login, render the index.html page
            flash('Login successful', 'success')
            connection.close()  # Close the database connection
            return redirect(url_for('index'))
        else:
            # Authentication failed, you can display an error message or redirect back to the login page
            flash('Login failed. Please check your credentials.', 'danger')
        print(f"SQL Query: SELECT * FROM users WHERE email = {email} AND password = {password}")

    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Check if the email or username already exists
    cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, username))
    existing_user = cursor.fetchone()

    if existing_user:
        # User with the provided email or username already exists
        flash('Email or username already exists. Please sign in instead.', 'danger')
        return redirect(url_for('login'))
    else:
        # Insert the new user into the 'users' table
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        connection.commit()
        flash('Signup successful. You can now log in.', 'success')
        return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')

# Data Science Fundamentals Quiz Session Variables
def get_current_question_id_dsn():
    return session.get('current_question_id_dsn', 1)

def get_total_questions_dsn():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM dsnquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_dsn(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dsnquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@app.route('/dsnquiz', methods=['GET'])
def start_dsnquiz():
    current_question_id = get_current_question_id_dsn()
    question_data = fetch_question_from_database_dsn(current_question_id)
    total_questions = get_total_questions_dsn()

    if current_question_id <= total_questions:
        return render_template('dsnQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@app.route('/dsnquiz', methods=['POST'])
def submit_dsnanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_dsn(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_dsn'] = get_current_question_id_dsn() + 1

    if get_current_question_id_dsn() > get_total_questions_dsn():
        return redirect(url_for('result'))

    return redirect(url_for('start_dsnquiz'))


# Database Management Quiz Session Variables
def get_current_question_id_dm():
    return session.get('current_question_id_dm', 1)

def get_total_questions_dm():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM dmquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_dm(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dmquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@app.route('/dmquiz', methods=['GET'])
def start_dmquiz():
    current_question_id = get_current_question_id_dm()
    question_data = fetch_question_from_database_dm(current_question_id)
    total_questions = get_total_questions_dm()

    if current_question_id <= total_questions:
        return render_template('dmQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@app.route('/dmquiz', methods=['POST'])
def submit_dmanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_dm(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_dm'] = get_current_question_id_dm() + 1

    if get_current_question_id_dm() > get_total_questions_dm():
        return redirect(url_for('result'))

    return redirect(url_for('start_dmquiz'))


# Cloud Computing Quiz Session Variables
def get_current_question_id_cc():
    return session.get('current_question_id_cc', 1)

def get_total_questions_cc():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM ccquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_cc(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ccquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@app.route('/cloud-computing', methods=['GET'])
def start_cloud_computing():
    current_question_id = get_current_question_id_cc()
    question_data = fetch_question_from_database_cc(current_question_id)
    total_questions = get_total_questions_cc()

    if current_question_id <= total_questions:
        return render_template('ccQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@app.route('/cloud-computing', methods=['POST'])
def submit_ccanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_cc(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_cc'] = get_current_question_id_cc() + 1

    if get_current_question_id_cc() > get_total_questions_cc():
        return redirect(url_for('result'))

    return redirect(url_for('start_cloud_computing'))


# Web Development Quiz Session Variables
def get_current_question_id_wd():
    return session.get('current_question_id_wd', 1)

def get_total_questions_wd():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM wdquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_wd(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wdquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@app.route('/wdquiz', methods=['GET'])
def start_wdquiz():
    current_question_id = get_current_question_id_wd()
    question_data = fetch_question_from_database_wd(current_question_id)
    total_questions = get_total_questions_wd()

    if current_question_id <= total_questions:
        return render_template('wdQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@app.route('/wdquiz', methods=['POST'])
def submit_wdanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_wd(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_wd'] = get_current_question_id_wd() + 1

    if get_current_question_id_wd() > get_total_questions_wd():
        return redirect(url_for('result'))

    return redirect(url_for('start_wdquiz'))


# Cybersecurity Quiz Session Variables
def get_current_question_id_csy():
    return session.get('current_question_id_csy', 1)

def get_total_questions_csy():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM csyquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_csy(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM csyquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@app.route('/csyquiz', methods=['GET'])
def start_csyquiz():
    current_question_id = get_current_question_id_csy()
    question_data = fetch_question_from_database_csy(current_question_id)
    total_questions = get_total_questions_csy()

    if current_question_id <= total_questions:
        return render_template('csyQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@app.route('/csyquiz', methods=['POST'])
def submit_csyanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_csy(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_csy'] = get_current_question_id_csy() + 1

    if get_current_question_id_csy() > get_total_questions_csy():
        return redirect(url_for('result'))

    return redirect(url_for('start_csyquiz'))


# Project Management Quiz Session Variables
def get_current_question_id_pm():
    return session.get('current_question_id_pm', 1)

def get_total_questions_pm():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM pmquiz_questions")
    total_questions = cursor.fetchone()[0]
    connection.close()
    return total_questions

def fetch_question_from_database_pm(question_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pmquiz_questions WHERE id = %s", (question_id,))
    question_data = cursor.fetchone()
    connection.close()
    return question_data

@app.route('/pmquiz', methods=['GET'])
def start_pmquiz():
    current_question_id = get_current_question_id_pm()
    question_data = fetch_question_from_database_pm(current_question_id)
    total_questions = get_total_questions_pm()

    if current_question_id <= total_questions:
        return render_template('pmQuiz.html', question=question_data[1], options=question_data[2:6])

    return redirect(url_for('result'))

@app.route('/pmquiz', methods=['POST'])
def submit_pmanswer():
    user_answer = request.form.get('answer')
    correct_option = fetch_question_from_database_pm(get_current_question_id_dsn())[6]

    if user_answer == str(correct_option):
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    session['current_question_id_pm'] = get_current_question_id_pm() + 1

    if get_current_question_id_pm() > get_total_questions_pm():
        return redirect(url_for('result'))

    return redirect(url_for('start_pmquiz'))

# Route to display quiz results
@app.route('/result', methods=['GET'])
def result():
    correct_answers = session.get('correct_answers')
    total_questions = 10
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    result_data = {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': total_questions - correct_answers,
        'score': score
    }

    return render_template('result.html', result=result_data)


if __name__ == '__main__':
    app.run(debug=True)
