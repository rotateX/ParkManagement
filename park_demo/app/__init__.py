from flask import Flask, template_rendered
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config


db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bootstrap.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
