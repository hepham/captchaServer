from datetime import datetime

from .encrypt import random_string, encrypt
from .extension import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

def is_user_name_taken(email):
    return db.session.query(db.exists().where(Users.email == email)).scalar()


class Users(db.Model):
    __tablename__="jhi_user"
    meta = MetaData()
    id = db.Column(db.Integer,autoincrement =True, primary_key=True)
    created_by=db.Column(db.String(50),nullable=False)
    # create_date=db.Column(db.DateTime)
    last_modified_by=db.Column(db.String(50),nullable=True)
    activated=db.Column(db.Integer,nullable=False)
    activation_key=db.Column(db.String(20))
    first_name = db.Column(db.String(50),nullable=False)
    image_url=db.Column(db.String(256))
    lang_key=db.Column(db.String(10))
    last_name = db.Column(db.String(50),nullable=False)
    login=db.Column(db.String(50),nullable=False,unique=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    # reset_date=
    
    merchant_key = db.Column(db.String(254))
    count_captcha = db.Column(db.Integer)

    def __init__(self, fullName, email, password):
        self.fullName = fullName
        self.email = email
        self.password = password
        now = datetime.now()
        temp = email + str(now)
        self.merchant_key = encrypt(temp) + random_string(8, 4)
        self.count_captcha = 0
class DataSave():
    def __init__(self, captchaDecode, timesave):
        self.captchaDecode = captchaDecode
        self.timesave = timesave