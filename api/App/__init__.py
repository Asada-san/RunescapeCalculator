from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api.App.config import Config

db = SQLAlchemy()


def create_app(**kwargs):
    """
    Initialises and configures the application, csrf, socket, migration, database,
    password hasher, login manager, mail, admin, limiter and cors. Blueprints are used for
    simplifying structure are also registered to the app in this function.

    :return: app
    """

    app = Flask(__name__, static_folder='../../webapp/dist/', static_url_path='')

    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    from api.App.routes import api

    app.register_blueprint(api, url_prefix="/api")

    return app
