from flask import Flask
from web_flask.quizzes import ccquiz, csyquiz, dmquiz, dsnquiz, pmquiz, wdquiz, result


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    app.register_blueprint(ccquiz.ccquiz_bp)
    app.register_blueprint(csyquiz.csyquiz_bp)
    app.register_blueprint(dmquiz.dmquiz_bp)
    app.register_blueprint(dsnquiz.dsnquiz_bp)
    app.register_blueprint(pmquiz.pmquiz_bp)
    app.register_blueprint(wdquiz.wdquiz_bp)
    app.register_blueprint(result.result_bp)
    return app
