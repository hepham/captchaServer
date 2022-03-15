import os

from flask import Flask
from flask_cors import CORS

from .extension import db, ma
from .model import Users
from .user.controller import users


def create_db(app):
    if not os.path.exists("library/library.db"):
        db.create_all(app=app)
        print("Created DB!")


def create_app(config_file="config.py"):
    app = Flask(__name__)
    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    app.config.from_pyfile(config_file)
    create_db(app)
    app.register_blueprint(users)
    return app
