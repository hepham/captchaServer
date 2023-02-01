from datetime import datetime
import time
from flask import  jsonify
from sqlalchemy.ext.declarative import declarative_base
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
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')
user_schema = UserSchema()
users_schema = UserSchema(many=True)
import datetime;

# Sign Up

def sign_up_service():
    data = request.json
    #print(data)
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
        #print(data)
        user = Users.query.filter_by(email=data['email']).first()
        # #print(user.password)
        if not user:
            return jsonify({'message': 'Please check your email, password and try again.'}), 401
        elif user.password == data['password']:
            #print("success")
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
        #print(Exception)
        return jsonify({"message": "user Not found"}), 200


# change merchant key

def change_key():
    if request.method == 'POST':
        data = request.json
        # #print(data)
        user = Users.query.filter_by(merchant_key=data['merchant_key']).first()
        # #print(user.password)
        if user:
            try:
                now = datetime.now()
                #print(user.email)
                temp = user.email + str(now)
                user.merchant_key = encrypt(temp) + random_string(8, 4)
                db.session.commit()
                #print(user_schema.jsonify(user).data)
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

# def getValue(arr):
def predict():
    # imagefile= request.files['imagefile']
    # image_path="./images/"+imagefile.filename
    # imagefile.save(image_path)
    # #print(request.form.get('captcha'))
    start=time.time()
    captchaImage=request.form.get('captcha')
    key=request.form.get('merchant_key')
    user = Users.query.filter_by(merchant_key=key).first()
    # #print(user.password)
    if user:
        if user.count_captcha>0:
            user.count_captcha=user.count_captcha-1;
            db.session.commit()
            # end=time.time()
            # print("delta time",end-start)
        # imagetemp=chuyen_base64_sang_anh(capchaImage)
        # image=cv2.cvtColor(imagetemp,cv2.COLOR_BGR2RGB)
            
            imagedata = base64.b64decode(captchaImage)
            buf = io.BytesIO(imagedata)
            image=Image.open(buf)
            image = image.resize((640, 640))
            # start=time.time()
            # #print(image.size)
            # image=image.resize(640,640)
            # cv2.imshow('image', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            results = model(image)
            end=time.time()
            print("deltatime 176:",end-start)
            # results.#print()  # or .show(), .save()
            # results.xyxy[0]  # im predictions (tensor)
            print(results.pandas().xyxy[0])  # im predictions (pandas)
            xmin = 0;
            ymin = 10;
            ymax = 200;
            count = 0;
            array = []
            strcompare = ''
            ymax1 = 360
            array1 = []
            ymax2 = 450
            ymax3 = 530
            array2 = []
            array3 = []
            for j in range(len(results.pandas().xyxy[0].name)):
                if (results.pandas().xyxy[0].name[j] == 'and'):
                    results.pandas().xyxy[0].name[j] = '&'
                elif (results.pandas().xyxy[0].name[j] == 'acong'):
                    results.pandas().xyxy[0].name[j] = '@'
                elif (results.pandas().xyxy[0].name[j] == 'thang'):
                    results.pandas().xyxy[0].name[j] = '#'
                elif (results.pandas().xyxy[0].name[j] == 'per'):
                    results.pandas().xyxy[0].name[j] = '%'
                elif (results.pandas().xyxy[0].name[j] == 'dolar'):
                    results.pandas().xyxy[0].name[j] = '$'
                # print("result:",results.pandas().xyxy[0].name[j])    
            end=time.time()
            print("deltatime 205:",end-start)
            for i in range(len(results.pandas().xyxy[0].name)):
                if results.pandas().xyxy[0].ymin[i] < ymax:
                    array.append(results.pandas().xyxy[0].xmin[i])
                elif results.pandas().xyxy[0].ymin[i] < ymax1 and results.pandas().xyxy[0].ymin[i] > 250:
                    array1.append(results.pandas().xyxy[0].xmin[i])
                elif results.pandas().xyxy[0].ymin[i] < ymax2 and results.pandas().xyxy[0].ymin[i] > 370:
                    array2.append(results.pandas().xyxy[0].xmin[i])
                elif results.pandas().xyxy[0].ymin[i] < ymax3 and results.pandas().xyxy[0].ymin[i] > 460:
                    array3.append(results.pandas().xyxy[0].xmin[i])
            str = ''
            end=time.time()
            print("deltatime 217:",end-start)
            array.sort()
            for i in range(len(array)):
                for j in range(len(results.pandas().xyxy[0].name)):
                    if array[i] == results.pandas().xyxy[0].xmin[j]:
                        str=str+results.pandas().xyxy[0].name[j]
            print("str: "+str)
            array1.sort()
            array2.sort()
            array3.sort()
            end=time.time()
            print("deltatime 228:",end-start)
            for x in array1:
                array.append(x)
            for x in array2:
                array.append(x)
            # print(array1)
            for i in range(len(array)):
                for j in range(len(results.pandas().xyxy[0].name)):
                    if array[i] == results.pandas().xyxy[0].xmin[j]:
                        strcompare = strcompare + results.pandas().xyxy[0].name[j]
            end=time.time()
            print("deltatime 237:",end-start)
            i = 0
            index1=0
            index2=0
            counter=0
            check={}
            dict={}
            for x in strcompare:
                if not x.isdigit():
                    check[x]=False
            while(i<len(strcompare)):
                if(strcompare[i].isdigit()):
                   
                    if (counter%2==0):
                        index1=i
                        counter=counter+1
                        #print("index1:",index1)
                        #print("index2:",index2)
                        if(index2!=0):
                            for j in range(index2+1,index1,1):
                                #print("strcompare[j]]:",strcompare[j])
                                #print("check[strcompare[j]]",check[strcompare[j]])
                                #print("strcompare[index1]:",strcompare[index1])
                                if (not strcompare[j] in dict):
                                    dict[strcompare[j]]=strcompare[index1]
        
                                elif not check[strcompare[j]]:
                                        dict[strcompare[j]]=strcompare[index1]
                                if(abs(index2-index1)<=2):
                                        check[strcompare[j]]=True
                        else:
                            for j in range(index2,index1,1):
                                #print("strcompare[j]]:",strcompare[j])
                                #print("check[strcompare[j]]",check[strcompare[j]])
                                #print("strcompare[index1]:",strcompare[index1])
                                if (not strcompare[j] in dict):
                                    dict[strcompare[j]]=strcompare[index1]
        
                                elif not check[strcompare[j]]:
                                        dict[strcompare[j]]=strcompare[index1]
                                if(abs(index2-index1)<=2):
                                        check[strcompare[j]]=True
                    else :
                        index2=i
                        counter=counter+1
                        #print("index1:",index1)
                        #print("index2:",index2)
                        #print("----------------------------------------")
                        for j in range(index1+1,index2,1):
                                # dict[strcompare[j]]=strcompare[index2]       
                                if (not strcompare[j] in dict):
                                    dict[strcompare[j]]=strcompare[index2]
        
                                else:
                                    if (not check[strcompare[j]]):
                                        dict[strcompare[j]]=strcompare[index2]
                                if(abs(index2-index1)<=2):
                                    check[strcompare[j]]=True
                i=i+1
            strsave=str;
            list=[]
            for x in str:
                if not x in dict:
                    # print("khong co trong dict:",x)
                    dict[x]=-1
                    for value in dict.values():
                        # print("value:",value)
                        dict[x]=value
                        str=strsave
                        for y in str:
                            str=str.replace(y,dict[y])
                            list.append(str)
                        # print("str:",str)
                        str=strsave
                else:
                    str=str.replace(x,dict[x])
            # print("str:",str)
            result = ''.join([i for i in str if i.isdigit()])
            #print("result: "+ result)
            end=time.time()
            # print("delta time3:",end-start)
            return jsonify({"message": "sucess",
                            "predictions":{
                                "captcha":result,
                                "confidence":"oke",
                                "OriginCaptcha":{
                                    "hint_1":"x_x",
                                    "hint_2":"x_x",
                                    "hint_3":"x_x",
                                    "hint_4":"x_x",
                                    "hint_5":"x_x",
                                    "main":"xxxxx"
                                },
                                "time":end-start
                                },
                            "success":True
                            }
                           ), 200
        return jsonify({"message": "your captcha is out"}), 200
    return jsonify({"message": "can't found user"}), 200
