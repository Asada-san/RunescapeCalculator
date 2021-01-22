from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from App.config import Config

db = SQLAlchemy()


def create_app(**kwargs):
    """
    Initialises and configures the application, csrf, socket, migration, database,
    password hasher, login manager, mail, admin, limiter and cors. Blueprints are used for
    simplifying structure are also registered to the app in this function.

    :return: app
    """

    app = Flask(__name__)
    db.init_app(app)
    app.config.from_object(Config)

    from App.routes import RS

    app.register_blueprint(RS)

    return app
