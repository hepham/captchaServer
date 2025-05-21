import os
from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from library.extension import db, ma
from library.model import Users
from library.user.controller import users
import mysql.connector
import sys

def create_db(app):
    # if not os.path.exists("library/library.db"):
    #     db.create_all(app=app)
    #     print("Created DB!")
    mydb=mysql.connector.connect(
        host="43.228.213.30",
        user="captcha_web_prod",
        passwd="NEiB56LhGZwG7c56",
        database="captcha_web_prod"
    )

    my_cursor=mydb.cursor()
    # my_cursor.execute("CREATE DATABASE IF NOT EXISTS captcha_web")
    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        print(db)


def create_app(config_file="library/config.py"):
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+pymysql://captcha_web_prod:NEiB56LhGZwG7c56@43.228.213.30/captcha_web_prod'
    db.init_app(app)
    ma.init_app(app)
    # app.config.from_pyfile(config_file)
    # create_db(app)
    app.register_blueprint(users)
    return app
# def restart_app():
#     print("Restarting Flask application...")
#     # Dispose of the SQLAlchemy engine to close all connections
#     with app.app_context():
#         # Dispose of the SQLAlchemy engine to close all connections
#         db.engine.dispose()
#         # Restart the Python process
#         print("system:")
#         print(sys.argv)
#         os.execv(sys.executable, [sys.executable] + sys.argv)

# scheduler = BackgroundScheduler()
# # Schedule the restart function to run every two hours
# scheduler.add_job(restart_app, 'interval', minutes=3)
# scheduler.start()

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", port=8080,ssl_context=('cert.pem', 'key.pem'))
