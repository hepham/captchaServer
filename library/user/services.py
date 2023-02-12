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
# import datetime
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')
user_schema = UserSchema()
users_schema = UserSchema(many=True)
saveResult={}
saveIndex={}


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
                now = time.time()
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
                    now = time.time()
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
    titleName=str(datetime.fromtimestamp(int(start)))
    # print("start:",titleName)
    captchaImage=request.form.get('captcha')
    key=request.form.get('merchant_key')
    if(len(saveResult)>100):
        saveResult.clear()
        saveIndex.clear()
    if captchaImage in saveResult:
        print("Da luu trong dict")
        results=saveResult[captchaImage]
        # print("len(saveResult[captchaImage]):",len(saveResult[captchaImage]))
        # print("saveIndex[captchaImage]:",saveIndex[captchaImage])
        if(saveIndex[captchaImage]<len(saveResult[captchaImage])):
            saveIndex[captchaImage]=saveIndex[captchaImage]+1
        else:
            saveIndex[captchaImage]=0
        # print("len(saveResult[captchaImage]):",len(saveResult[captchaImage]))
        # print("saveIndex[captchaImage]:",saveIndex[captchaImage])
        result=results[saveIndex[captchaImage]-1]
        end=time.time()
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
    else:
        user = Users.query.filter_by(merchant_key=key).first()
        # #print(user.password)
        if user:
            if user.count_captcha>0:
                user.count_captcha=user.count_captcha-1;
                db.session.commit()
                end=time.time()
                # print("delta time",end-start)
                imagedata = base64.b64decode(captchaImage)
                buf = io.BytesIO(imagedata)
                image=Image.open(buf)
                image = image.resize((640, 640))
                results = model(image)
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
                t=results.pandas();
                for j in range(len(t.xyxy[0].name)):
                    if (t.xyxy[0].name[j] == 'and'):
                        t.xyxy[0].name[j] = '&'
                    elif (t.xyxy[0].name[j] == 'acong'):
                        t.xyxy[0].name[j] = '@'
                    elif (t.xyxy[0].name[j] == 'thang'):
                        t.xyxy[0].name[j] = '#'
                    elif (t.xyxy[0].name[j] == 'per'):
                        t.xyxy[0].name[j] = '%'
                    elif (t.xyxy[0].name[j] == 'dolar'):
                        t.xyxy[0].name[j] = '$'
                    # print("result:",t.xyxy[0].name[j])    
                for i in range(len(t.xyxy[0].name)):
                    if t.xyxy[0].ymin[i] < ymax:
                        array.append(t.xyxy[0].xmin[i])
                    elif t.xyxy[0].ymin[i] < ymax1 and t.xyxy[0].ymin[i] > 250:
                        array1.append(t.xyxy[0].xmin[i])
                    elif t.xyxy[0].ymin[i] < ymax2 and t.xyxy[0].ymin[i] > 370:
                        array2.append(t.xyxy[0].xmin[i])
                    elif t.xyxy[0].ymin[i] < ymax3 and t.xyxy[0].ymin[i] > 460:
                        array3.append(t.xyxy[0].xmin[i])
                strResult = ''
                array.sort()
                for i in range(len(array)):
                    for j in range(len(t.xyxy[0].name)):
                        if array[i] == t.xyxy[0].xmin[j]:
                            strResult=strResult+t.xyxy[0].name[j]
                # print("str: "+str)
                array1.sort()
                array2.sort()
                array3.sort()
                for x in array2:
                    array1.append(x)
                for x in array3:
                    array1.append(x)
                # print(array1)
                for i in range(len(array1)):
                    for j in range(len(t.xyxy[0].name)):
                        if array1[i] == t.xyxy[0].xmin[j]:
                            strcompare = strcompare + t.xyxy[0].name[j]
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
                            if(index2!=0):
                                for j in range(index2+1,index1,1):
                                    if (not strcompare[j] in dict):
                                        dict[strcompare[j]]=strcompare[index1]
            
                                    elif not check[strcompare[j]]:
                                            dict[strcompare[j]]=strcompare[index1]
                                    if(abs(index2-index1)<=2):
                                            check[strcompare[j]]=True
                            else:
                                for j in range(index2,index1,1):
                                    if (not strcompare[j] in dict):
                                        dict[strcompare[j]]=strcompare[index1]
            
                                    elif not check[strcompare[j]]:
                                            dict[strcompare[j]]=strcompare[index1]
                                    if(abs(index2-index1)<=2):
                                            check[strcompare[j]]=True
                        else :
                            index2=i
                            counter=counter+1
                            for j in range(index1+1,index2,1):      
                                    if (not strcompare[j] in dict):
                                        dict[strcompare[j]]=strcompare[index2]
            
                                    else:
                                        if (not check[strcompare[j]]):
                                            dict[strcompare[j]]=strcompare[index2]
                                    if(abs(index2-index1)<=2):
                                        check[strcompare[j]]=True
                    i=i+1
                strsave=strResult;
                list=[]
                for x in strResult:
                    if not x in dict:
                        strResult=strResult.replace(x,'')
                # print("strResult",strResult)
                if(len(strResult)>=5):
                      for y in strResult:
                            strResult=strResult.replace(y,dict[y])
                            list.append(strResult)
                strResult=strsave
                for x in strResult:
                    if not x in dict:
                        # print("x not in dict",x)
                        dict[x]=-1
                        for value in dict.values():
                            dict[x]=value
                            strResult=strsave
                            for y in strResult:
                                strResult=strResult.replace(y,dict[y])
                            list.append(strResult)
                            strResult=strsave
                    else:
                        strResult=strResult.replace(x,dict[x])
                list.append(strResult)
                index=0
                saveResult[captchaImage]=list
                saveIndex[captchaImage]=index
                # print(dict)
                # print("list:",list)
                result = ''.join([i for i in strResult if i.isdigit()])
                for item in list:
                    if not item.isdigit():
                        list.remove(item)
                    # else:
                    #     print(item)
                # print("list:",list)
                #print("result: "+ result)
                # end=time.time()
                # print("delta time3:",end-start)
                end=time.time()
                # print("strcompare",strcompare)
                titleName=titleName+"--"+str(datetime.fromtimestamp(int(end)))+"--"+str(list)+".txt"
                titleName=titleName.replace(":"," ")
                titleName=titleName.replace("'","")
                file=open(titleName,'w')
                file.write(captchaImage)
                file.close()
                # print("titleName:",titleName)       
                return jsonify({"message": "sucess",
                        "predictions":{
                            "captcha":list[0],
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
