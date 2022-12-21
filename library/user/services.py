from datetime import datetime

from flask import  jsonify

from library.encrypt import random_string, encrypt
from library.extension import db
from library.library_ma import UserSchema
from library.model import Users
import base64
from PIL import Image
import io
from flask import request
# PyTorch Hub
import numpy as np
import cv2
import torch
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.onnx')
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

def change_key():
    if request.method == 'POST':
        data = request.json
        # print(data)
        user = Users.query.filter_by(merchant_key=data['merchant_key']).first()
        # print(user.password)
        if user:
            try:
                now = datetime.now()
                print(user.email)
                temp = user.email + str(now)
                user.merchant_key = encrypt(temp) + random_string(8, 4)
                db.session.commit()
                print(user_schema.jsonify(user).data)
                return jsonify({'message': 'success', 'email': user.email, 'merchant_key': user.merchant_key,
                            'count_captcha': user.count_captcha}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Something wrong!"}), 200
        else:
            return "not found user"


# update number captcha

def update_captcha_number():
    if request.method == 'POST':
        data = request.json
        user = Users.query.filter_by(email=data['email']).first()
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

def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64
# @app.route('/',methods=['GET'])
# def hello_world():  # put application's code here
#     return render_template('index.html')

def predict():
    # imagefile= request.files['imagefile']
    # image_path="./images/"+imagefile.filename
    # imagefile.save(image_path)
    # print(request.form.get('captcha'))
    captchaImage=request.form.get('captcha')
    key=request.form.get('merchant_key')
    user = Users.query.filter_by(merchant_key=key).first()
    # print(user.password)
    if user:
        if user.count_captcha>0:
            user.count_captcha=user.count_captcha-1;
            db.session.commit()
        # imagetemp=chuyen_base64_sang_anh(capchaImage)
        # image=cv2.cvtColor(imagetemp,cv2.COLOR_BGR2RGB)
            imagedata = base64.b64decode(captchaImage)
            buf = io.BytesIO(imagedata)
            image=Image.open(buf)
            image = image.resize((640, 640))
            # print(image.size)
            # image=image.resize(640,640)
            # cv2.imshow('image', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            results = model(image)
            # results.print()  # or .show(), .save()
            results.xyxy[0]  # im predictions (tensor)
            # print(results.pandas().xyxy[0])  # im predictions (pandas)
            xmin = 0;
            ymin = 10;
            ymax = 200;
            count = 0;
            array = []
            for i in range(len(results.pandas().xyxy[0].name)):
                if results.pandas().xyxy[0].ymin[i] < ymax:
                    array.append(results.pandas().xyxy[0].xmin[i])
            str = ''
            array.sort()
            for i in range(len(array)):
                for j in range(len(results.pandas().xyxy[0].name)):
                    if array[i] == results.pandas().xyxy[0].xmin[j]:
                        if (results.pandas().xyxy[0].name[j] == 'and'):
                            results.pandas().xyxy[0].name[j] = '&'
                            str = str + '&'
                        elif (results.pandas().xyxy[0].name[j] == 'acong'):
                            results.pandas().xyxy[0].name[j] = '@'
                            str = str + '@'
                        elif (results.pandas().xyxy[0].name[j] == 'thang'):
                            results.pandas().xyxy[0].name[j] = '#'
                            str = str + '#'
                        elif (results.pandas().xyxy[0].name[j] == 'per'):
                            results.pandas().xyxy[0].name[j] = '%'
                            str = str + '%'
                        elif (results.pandas().xyxy[0].name[j] == 'dolar'):
                            results.pandas().xyxy[0].name[j] = '$'
                            str = str + '$'
                        else:
                            str = str + results.pandas().xyxy[0].name[j]
            # print("str: "+str)
            strcompare = ''
            ymax = 360
            array = []
            for i in range(len(results.pandas().xyxy[0].name)):
                if results.pandas().xyxy[0].ymin[i] < ymax and results.pandas().xyxy[0].ymin[i] > 250:
                    array.append(results.pandas().xyxy[0].xmin[i])
            array.sort()
            for i in range(len(array)):
                for j in range(len(results.pandas().xyxy[0].name)):
                    if array[i] == results.pandas().xyxy[0].xmin[j]:
                        if (results.pandas().xyxy[0].name[j] == 'and'):
                            results.pandas().xyxy[0].name[j] = '&'
                            strcompare = strcompare + '&'
                        elif (results.pandas().xyxy[0].name[j] == 'acong'):
                            results.pandas().xyxy[0].name[j] = '@'
                            strcompare = strcompare + '@'
                        elif (results.pandas().xyxy[0].name[j] == 'thang'):
                            results.pandas().xyxy[0].name[j] = '#'
                            strcompare = strcompare + '#'
                        elif (results.pandas().xyxy[0].name[j] == 'per'):
                            results.pandas().xyxy[0].name[j] = '%'
                            strcompare = strcompare + '%'
                        elif (results.pandas().xyxy[0].name[j] == 'dolar'):
                            results.pandas().xyxy[0].name[j] = '$'
                            strcompare = strcompare + '$'
                        else:
                            strcompare = strcompare + results.pandas().xyxy[0].name[j]

            ymax = 450
            array = []
            for i in range(len(results.pandas().xyxy[0].name)):
                if results.pandas().xyxy[0].ymin[i] < ymax and results.pandas().xyxy[0].ymin[i] > 370:
                    array.append(results.pandas().xyxy[0].xmin[i])
            array.sort()
            for i in range(len(array)):
                for j in range(len(results.pandas().xyxy[0].name)):
                    if array[i] == results.pandas().xyxy[0].xmin[j]:
                        if (results.pandas().xyxy[0].name[j] == 'and'):
                            results.pandas().xyxy[0].name[j] = '&'
                            strcompare = strcompare + '&'
                        elif (results.pandas().xyxy[0].name[j] == 'acong'):
                            results.pandas().xyxy[0].name[j] = '@'
                            strcompare = strcompare + '@'
                        elif (results.pandas().xyxy[0].name[j] == 'thang'):
                            results.pandas().xyxy[0].name[j] = '#'
                            strcompare = strcompare + '#'
                        elif (results.pandas().xyxy[0].name[j] == 'per'):
                            results.pandas().xyxy[0].name[j] = '%'
                            strcompare = strcompare + '%'
                        elif (results.pandas().xyxy[0].name[j] == 'dolar'):
                            results.pandas().xyxy[0].name[j] = '$'
                            strcompare = strcompare + '$'
                        else:
                            strcompare = strcompare + results.pandas().xyxy[0].name[j]
            ymax = 530
            array = []
            for i in range(len(results.pandas().xyxy[0].name)):
                if results.pandas().xyxy[0].ymin[i] < ymax and results.pandas().xyxy[0].ymin[i] > 460:
                    array.append(results.pandas().xyxy[0].xmin[i])
            array.sort()
            for i in range(len(array)):
                for j in range(len(results.pandas().xyxy[0].name)):
                    if array[i] == results.pandas().xyxy[0].xmin[j]:
                        if (results.pandas().xyxy[0].name[j] == 'and'):
                            results.pandas().xyxy[0].name[j] = '&'
                            strcompare = strcompare + '&'
                        elif (results.pandas().xyxy[0].name[j] == 'acong'):
                            results.pandas().xyxy[0].name[j] = '@'
                            strcompare = strcompare + '@'
                        elif (results.pandas().xyxy[0].name[j] == 'thang'):
                            results.pandas().xyxy[0].name[j] = '#'
                            strcompare = strcompare + '#'
                        elif (results.pandas().xyxy[0].name[j] == 'per'):
                            results.pandas().xyxy[0].name[j] = '%'
                            strcompare = strcompare + '%'
                        elif (results.pandas().xyxy[0].name[j] == 'dolar'):
                            results.pandas().xyxy[0].name[j] = '$'
                            strcompare = strcompare + '$'
                        else:
                            strcompare = strcompare + results.pandas().xyxy[0].name[j]
            # print("strcompare: "+strcompare)
        
            i = 0

            while i < len(strcompare) - 1:
                if (strcompare[i + 1].isdigit()):
                    str = str.replace(strcompare[i], strcompare[i + 1])
                    i = i + 1
                else:
                    i = i + 1

            result = ''.join([i for i in str if i.isdigit()])
            # print("result: "+ result)
            return result
        return jsonify({"message": "your captcha is out"}), 200
    return jsonify({"message": "can't found user"}), 200