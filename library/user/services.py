from datetime import datetime

from flask import request, jsonify

from library.encrypt import random_string, encrypt
from library.extension import db
from library.library_ma import UserSchema
from library.model import Users

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Sign Up

def sign_up_service():
    data = request.json
    print(data)
    if data and ('email' in data) and ('password' in data):

        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'This email is already taken!'}), 409
        else:
            fullName = data['fullName']
            email = data['email']
            password = data['password']
            try:
                new_user = Users(fullName, email, password)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'message': 'success'}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({'message': 'Can not register'}), 500
    else:
        return jsonify({"message": "Request error"}), 200


# sign in
def sign_in():
    if request.method == 'POST':
        data = request.json
        print(data)
        user = Users.query.filter_by(email=data['email']).first()
        # print(user.password)
        if not user:
            return jsonify({'message': 'Please check your email, password and try again.'}), 401
        elif user.password == data['password']:
            print("success")
            return jsonify({'message': 'success', 'email': user.email, 'merchant_key': user.merchant_key,
                            'count_captcha': user.count_captcha}), 200
        return jsonify({"message": "Please check your email, password and try again."}), 401


# get infor user by id

def get_infor_by_id_service(id):
    user = Users.query.get(id)
    if user:
        return user_schema.jsonify(user)
    else:
        return jsonify({"message": "Not found user"}), 200


# get all users

def get_all_service():
    try:
        users = Users.query.all()
        if users:
            return users_schema.jsonify(users)
        else:
            return jsonify({"message": "Not found"}), 200
    except Exception:
        print(Exception)
        return jsonify({"message": "user Not found"}), 200


# change merchant key

def change_key(id):
    user = Users.query.get(id)
    if user:
        try:
            now = datetime.now()
            print(user.email)
            temp = user.email + str(now)
            user.merchant_key = encrypt(temp) + random_string(8, 4)
            db.session.commit()
            return user_schema.jsonify(user)
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Something wrong!"}), 200
    else:
        return "not found user"


# update number captcha

def update_captcha_number(email):
    user = Users.query.get(email)
    data = request.json
    if user:
        if data and "count_captcha" in data:
            try:
                user.count_captcha = user.count_captcha + int(data["count_captcha"])
                db.session.commit()
                now = datetime.now()
                return jsonify({
                    "email": user.email,
                    "count_capcha": user.count_captcha,
                    "time": str(now)
                })
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "something is wrong"}), 200
    else:
        return jsonify({"message": "not found"}), 200
