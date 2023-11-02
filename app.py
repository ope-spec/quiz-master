from flask import Flask, redirect, url_for, render_template
from flask_pymongo import PyMongo
from config import SECRET_KEY, db_config
from web_flask.quizzes import dsnquiz_bp, dmquiz_bp, ccquiz_bp, wdquiz_bp, csyquiz_bp, pmquiz_bp, result_bp
from web_flask.login import login_bp
from web_flask.signup import signup_bp


app = Flask(__name__)

# Set the secret key
app.secret_key = SECRET_KEY

# Initialize the MongoDB connection
app.config["MONGO_URI"] = db_config["uri"]
mongo = PyMongo(app)

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


@app.route('/')
def root():
    return redirect(url_for('login_bp.login_route'))


@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
