from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
bootstrap = Bootstrap5()


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    db.init_app(app)
    bootstrap.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
