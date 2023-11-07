from flask import Flask, redirect, url_for, render_template
from config import SECRET_KEY
from web_flask.quizzes import dsnquiz_bp, dmquiz_bp, ccquiz_bp, wdquiz_bp, csyquiz_bp, pmquiz_bp, result_bp
from web_flask.quizzes import result_history_bp
from web_flask.login import login_bp
from web_flask.signup import signup_bp
from flask_login import LoginManager
from web_flask.user import User


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

# Set the secret key
app.secret_key = SECRET_KEY

# Register the blueprints for the quizzes
app.register_blueprint(dsnquiz_bp)
app.register_blueprint(dmquiz_bp)
app.register_blueprint(ccquiz_bp)
app.register_blueprint(wdquiz_bp)
app.register_blueprint(csyquiz_bp)
app.register_blueprint(pmquiz_bp)
app.register_blueprint(result_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(result_history_bp)


@app.route('/')
def root():
    return redirect(url_for('quiz_master_index'))

@app.route('/quiz-master-index')
def quiz_master_index():
    return render_template('quiz-master-index.html')

@app.route('/quiz-master')
def quiz_master():
    return render_template('quiz-master.html')

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user_id
    # Replace this with the actual code to load the user
    return User.query.get(int(user_id))  # Example assuming a User model



if __name__ == '__main__':
    app.run(debug=True)
