import os

from flask import Flask
from flask_cors import CORS

from .extension import db, ma
from .model import Users
from .user.controller import users
import mysql.connector

def create_db(app):
    # if not os.path.exists("library/library.db"):
    #     db.create_all(app=app)
    #     print("Created DB!")
    mydb=mysql.connector.connect(
        host="103.90.224.67",
        user="vietanhnd",
        passwd="vietanhnd1909",
        database="captcha_web"
    )

    my_cursor=mydb.cursor()
    # my_cursor.execute("CREATE DATABASE IF NOT EXISTS captcha_web")
    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        print(db)
    # my_cursor.execute("CREATE TABLE IF NOT EXISTS USERS(\
    #     id int NOT NULL AUTO_INCREMENT primary key,\
    #     fullname varchar(100) not null,\
    #     email varchar(100) not null unique,\
    #     password varchar(100) not null, \
    #     merchant_key varchar(100) not null,\
    #     count_captcha int default 0\
    #     )")

def create_app(config_file="config.py"):
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+pymysql://vietanhnd:vietanhnd1909@103.90.224.67/captcha_web_prod'
    db.init_app(app)
    ma.init_app(app)
    app.config.from_pyfile(config_file)
    # create_db(app)
    app.register_blueprint(users)
    return app
