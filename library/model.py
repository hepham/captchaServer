from datetime import datetime

from .encrypt import random_string, encrypt
from .extension import db


def is_user_name_taken(email):
    return db.session.query(db.exists().where(Users.email == email)).scalar()


class Users(db.Model):
    id = db.Column(db.Integer,autoincrement =True, primary_key=True)
    fullName = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    merchant_key = db.Column(db.String)
    count_captcha = db.Column(db.Integer)

    def __init__(self, fullName, email, password):
        self.fullName = fullName
        self.email = email
        self.password = password
        now = datetime.now()
        temp = email + str(now)
        self.merchant_key = encrypt(temp) + random_string(8, 4)
        self.count_captcha = 0
