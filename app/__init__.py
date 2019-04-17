from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    from .api import api as api_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
