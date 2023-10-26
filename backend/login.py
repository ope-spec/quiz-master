from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder="templates")


# Database connection
db = mysql.connector.connect(
   host="sql.freedb.tech",
   user="freedb_quizmaster",
   password="p%@2Z?FpvDFDx5j",
   database="freedb_quizmaster"
)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()

    # Check if the username already exists in the database
    cursor.execute("SELECT username FROM user WHERE username = %s",
                   (username,))
    existing_username = cursor.fetchone()

    if existing_username:
        flash('Username is taken', 'error')
        return redirect(url_for('login_page'))

    # Insert the user into the database
    cursor.execute
    ("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
     (username, email, password))
    db.commit()

    flash('Sign-up successful! You can now log in.', 'success')
    return redirect(url_for('login_page'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = db.cursor()

    # Retrieve the user's information based on the provided username
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and user[3] == password:
        # Password matches, set up the session or take any further action
        flash('Login successful!', 'success')
        return redirect(url_for('login_page'))
    else:
        flash('Username or password is wrong', 'error')
        return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
