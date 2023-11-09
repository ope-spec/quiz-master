from flask import Flask, Response, redirect, url_for, render_template
from config import SECRET_KEY
from web_flask.quizzes import dsnquiz_bp, dmquiz_bp, ccquiz_bp, wdquiz_bp, csyquiz_bp, pmquiz_bp, result_bp
from web_flask.quizzes import result_history_bp
from web_flask.login import login_bp
from web_flask.signup import signup_bp
from flask_login import LoginManager
from web_flask.user import User


app = Flask(__name__, static_folder='static')

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


@app.route('/no-cache-page')
def no_cache_page():
    response = Response("This page should not be cached", status=200)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/quiz-master')
def quiz_master():
    return render_template('quiz-master.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
