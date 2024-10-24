from datetime import datetime 
from datetime import timezone
import time
from flask import  jsonify
from sqlalchemy.ext.declarative import declarative_base
from library.encrypt import encrypt_message, random_string, encrypt
from library.extension import db
from library.library_ma import UserSchema
from library.model import Users,DataSave
import base64
from PIL import Image
import io
from flask import request
# PyTorch Hub
import numpy as np
import cv2
import torch
import json
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
# import datetime
model = torch.hub.load('ultralytics/yolov5', 'custom', 'newModel.pt')
user_schema = UserSchema()
users_schema = UserSchema(many=True)
saveResult={}
saveIndex={}
saveCheck={}
countcaptcha=0;
rename={}
ipDict={}
ipLockTime={}
isCheck=False
session=requests.Session()
with open('privateKey.pem', 'r') as f:
    private_key_string = f.read()
with open('publicKey.pem', 'rb') as f:
    public_key_string = f.read()
# Sign Up
if(countcaptcha>10):
    countcaptcha=0
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
def solve():
    global isCheck
    ip_address = request.remote_addr
    response=jsonify({"message": "spam"}), 508
    print("ip_address:",ip_address)
    if ip_address in ipDict:
        print("count:",ipDict[ip_address])
        ipDict[ip_address]=ipDict[ip_address]+1
    else:
        ipDict[ip_address]=0
    if ipDict[ip_address]>2:
        ipDict[ip_address]-=1
        if(ip_address in ipLockTime):
            if(ipLockTime[ip_address]>time.time()):
                # ipLockTime[ip_address]=time.time()+30
                return jsonify({"message": "spam"}), 508
            else:
                isCheck=False
                response= predict()
                print("isCheck:",isCheck)
                if(isCheck):
                    ipDict[ip_address]-=1
                    del ipLockTime[ip_address]
                else:
                    ipLockTime[ip_address]=time.time()+60
                    return jsonify({"message": "spam"}), 508
        else:
            ipLockTime[ip_address]=time.time()+60
            return jsonify({"message": "spam"}), 508
    else:
        isCheck=False
        response= predict()
        if(isCheck):
            ipDict[ip_address]-=1
    return response
def predict():
            # return jsonify({"message": "spam"}), 508
    # print(datetime.now(timezone.utc).strftime("%d%Y%m%H"))
    global isCheck
    keyEncrypt=int(datetime.now(timezone.utc).strftime("%d%Y%m%H"))
    strings = datetime.now(timezone.utc).strftime("%d,%Y,%m,%H")
    t = strings.split(',')
    keyEncrypt="";
    numbers = [ int(x) for x in t ]
    for x in numbers:
        keyEncrypt=keyEncrypt+str(x)
    keyEncrypt=str(int(keyEncrypt)>>1);
    # keyEncrypt=str(keyEncrypt);  
    # print(keyEncrypt)    
    # encrypted_message = encrypt("65454654654", keyEncrypt)
    start=time.time()
    titleName=str(datetime.fromtimestamp(int(start)))
    message=request.form.get('data')
    # print(message)
    captcha2=request.form.get('captcha')
    private_key = RSA.import_key(private_key_string)
    cipher = PKCS1_v1_5.new(private_key)
    try:
        encrypted_bytes = base64.b64decode(message)
        captcha1 = cipher.decrypt(encrypted_bytes, None)
    except Exception as e:
        print("Error RSA decrypt")
        return jsonify({"message": "decode error"}), 400
    # print(captcha1.decode('utf-8'))
    captchaImage=captcha1.decode('utf-8')+captcha2
    # captchaImage=request.form.get('captcha')
    key=request.form.get('key')
    # loai bo cac gia tri khoi dictionary sau 300s
    keyRemove=[]
    for keyR in saveResult:
        if(start-saveResult[keyR].timesave> 300):
            keyRemove.append(keyR)
    for keyR in keyRemove:
        del(saveResult[keyR])
    saveResultLength=len(saveResult)
    # do dai cua dict=10000  
    while(saveResultLength>10000):
        # lay phan tu dau tien cua dictionary va loai bo chung
        res = next(iter(saveResult))
        del(saveResult[res])   
        saveResultLength=len(saveResult)
    
        
    if captchaImage in saveResult:
        # print("Da luu trong dict")
        results=saveResult[captchaImage]
        result=results.captchaDecode
        # save file
        # if saveCheck[captchaImage]:
        #     #save file wrong
        #     titleName=titleName+"-"+result+".txt"
        #     titleName=titleName.replace(":"," ")
        #     titleName=titleName.replace("'","")
        #     file=open(titleName,'w')
        #     file.write(captchaImage)
        #     file.close()
        #     saveCheck[captchaImage]=False
        end=time.time()
        
        # encrypted_message = encrypt(result, keyEncrypt)
        public_key = RSA.import_key(public_key_string)
        cipher = PKCS1_v1_5.new(public_key)
        res_bytes=str.encode(result)
        encrypted_message = cipher.encrypt(res_bytes)
        isCheck=True;
        encrypt_message="true|"+base64.b64encode(encrypted_message).decode("utf-8");
        # print(encrypt_message)
        return encrypt_message
    else:
        try:
            user = Users.query.filter_by(merchant_key=key).first()
        except Exception as e:
            return jsonify({"message": "something wrong"}), 401
        if user:
            if user.count_captcha>0:
                # print(user.count_captcha)
                user.count_captcha=user.count_captcha-1;
                db.session.commit()
                try:
                    imagedata = base64.b64decode(captchaImage)
                    buf = io.BytesIO(imagedata)
                    image=Image.open(buf)
                    image = image.resize((640, 640))
                    # Decode captcha____________________________________________________________________________________
                    results = model(image)
                    t=results.pandas();
                except Exception as e:
                    print("Error decode image")
                    return jsonify({"message": "decode error"}), 400
                
                res= decodeCaptcha(t);
                saveResult[captchaImage]=DataSave(res,start)
                # post data history
                url="http://157.245.200.170:80/api/admin/account/save-captcha-history"
                params={"merchantKey":key,"userIp":request.remote_addr,"captcha":res}
                username="adminvietanh"
                password="vanhngoc"
                try:
                    response=session.post(url,auth=(username,password),json=params)
                    print(response)
                    response.close()
                except Exception as e:
                    print(e)

                encrypted_message = encrypt(res, keyEncrypt)
                print("result:",res)
                public_key = RSA.import_key(public_key_string)
                cipher = PKCS1_v1_5.new(public_key)
                res_bytes=str.encode(res)
                encrypted_message = cipher.encrypt(res_bytes)
                isCheck=True;
                # encrypted_message = cipher.encrypt(res_bytes)
                # print(base64.b64encode(encrypted_message).decode("utf-8"))
                encrypt_message="true|"+base64.b64encode(encrypted_message).decode("utf-8");
                # print(encrypt_message)
                # encrypted_message="true|"+encrypted_message.decode('utf-8')
                return encrypt_message
            return jsonify({"message": "your captcha is out"}), 423
        return jsonify({"message": "can't found user"}), 401
      
def decodeCaptcha(t):
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
    alphabet={}
    for j in range(len(t.xyxy[0].name)):
        if (t.xyxy[0].name[j] == 'and'):
            alphabet[t.xyxy[0].name[j]] = '&'
        elif (t.xyxy[0].name[j] == 'acong'):
            alphabet[t.xyxy[0].name[j]]= '@'
        elif (t.xyxy[0].name[j] == 'thang'):
            alphabet[t.xyxy[0].name[j]] = '#'
        elif (t.xyxy[0].name[j] == 'per'):
            alphabet[t.xyxy[0].name[j]]= '%'
        elif (t.xyxy[0].name[j] == 'dolar'):
            alphabet[t.xyxy[0].name[j]] = '$'
        else: alphabet[t.xyxy[0].name[j]] = t.xyxy[0].name[j]
        # print("result:",t.xyxy[0].name[j])    
        # get cordinate point
    for i in range(len(t.xyxy[0].name)):
        if t.xyxy[0].ymin[i] < ymax:
            array.append(t.xyxy[0].xmin[i])
        elif t.xyxy[0].ymin[i] < ymax1 and t.xyxy[0].ymin[i] > 250:
            array1.append(t.xyxy[0].xmin[i])
        elif t.xyxy[0].ymin[i] < ymax2 and t.xyxy[0].ymin[i] > 370:
            array2.append(t.xyxy[0].xmin[i])
            # array2.append(alphabet[t.xyxy[0].xmin[i]])
        elif t.xyxy[0].ymin[i] < ymax3 and t.xyxy[0].ymin[i] > 460:
            array3.append(t.xyxy[0].xmin[i])
            # array3.append(alphabet[t.xyxy[0].xmin[i]])
    strResult = ''
    array.sort()
    for i in range(len(array)):
        for j in range(len(t.xyxy[0].name)):
            if array[i] == t.xyxy[0].xmin[j]:
                strResult=strResult+alphabet[t.xyxy[0].name[j]]
                # if t.xyxy[0].name[j] in alphabet:
                #     strResult=strResult+alphabet[t.xyxy[0].name[j]]
                # else:strResult=strResult+t.xyxy[0].name[j]
                # print("arr:",t.xyxy[0].name[j],t.xyxy[0].xmin[j])
    # print("str: "+str)
    array1.sort()
    array2.sort()
    array3.sort()
    for x in array2:
        array1.append(x)
    for x in array3:
        array1.append(x)
    for i in range(len(array1)):
        # print(i)
        for j in range(len(t.xyxy[0].name)):
            if array1[i] == t.xyxy[0].xmin[j]:
                strcompare = strcompare + alphabet[t.xyxy[0].name[j]]
                # if t.xyxy[0].name[j] in alphabet:
                #     strcompare = strcompare + alphabet[t.xyxy[0].name[j]]
                # else:strcompare = strcompare + t.xyxy[0].name[j]
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
    listResult=[]
    # print(strResult)
    ListMistake={}
    
    
    if(len(strResult)>6):
        for x in strResult:
            if not x in dict:
                strResult=strResult.replace(x,'')
    else:
        strResult=strResult
        for x in strResult:
            if not x in dict:
                if x in ListMistake:
                    strResult=strResult.replace(x,ListMistake.get(x))
                else:
                    strResult=strResult.replace(x,list(dict.keys())[0])
    for y in strResult:
            strResult=strResult.replace(y,dict[y])
    # print("ket qua:"+strResult)
    listResult.append(strResult)
    strResult=strsave
    # Ket thuc decode captcha______________________________________________________________________
    # print(dict)
    # check gần đúng-------------------------
    # for x in strResult:
    #     if not x in dict:
    #         # print("x not in dict",x)
    #         dict[x]=-1
    #         for value in dict.values():
    #             dict[x]=value
    #             strResult=strsave
    #             for y in strResult:
    #                 strResult=strResult.replace(y,dict[y])
    #             list.append(strResult)
    #             strResult=strsave
    #     else:
    #         strResult=strResult.replace(x,dict[x])
    # list.append(strResult)
    index=0
    # saveIndex[captchaImage]=index
    # ------------------------------------------------
    # print(dict)
    # print("list:",list)
    result = ''.join([i for i in strResult if i.isdigit()])
    for item in listResult:
        if not item.isdigit():
            listResult.remove(item)
    end=time.time()
    # print("strcompare",strcompare)   
    # saveCheck[captchaImage]=True
    print("Result decode:",listResult[0])
    # print(type(listResult[0]))
    return listResult[0]
def predict2():
    global isCheck
    print(datetime.now(timezone.utc).strftime("%d%Y%m%H"))
    keyEncrypt=int(datetime.now(timezone.utc).strftime("%d%Y%m%H"))
    strings = datetime.now(timezone.utc).strftime("%d,%Y,%m,%H")
    t = strings.split(',')
    keyEncrypt="";
    numbers = [ int(x) for x in t ]
    for x in numbers:
        keyEncrypt=keyEncrypt+str(x)
    keyEncrypt=str(int(keyEncrypt)>>1);
    # keyEncrypt=str(keyEncrypt);  
    # print(keyEncrypt)
    # encrypted_message = encrypt("65454654654", keyEncrypt)
    start=time.time()
   
    titleName=str(datetime.fromtimestamp(int(start)))
    captchaImage=request.form.get('captcha')
    key=request.form.get('merchant_key')
    # loai bo cac gia tri khoi dictionary sau 300s
    keyRemove=[]
    for keyR in saveResult:
        if(start-saveResult[keyR].timesave> 300):
            keyRemove.append(keyR)
    for keyR in keyRemove:
        del(saveResult[keyR])
    saveResultLength=len(saveResult)
    # do dai cua dict=10000
    while(saveResultLength>10000):
        # lay phan tu dau tien cua dictionary va loai bo chung
        res = next(iter(saveResult))
        del(saveResult[res])   
        saveResultLength=len(saveResult)
    
        
    if captchaImage in saveResult:
        # print("Da luu trong dict")
        results=saveResult[captchaImage]
        result=results.captchaDecode[0]
        # save file
        # if saveCheck[captchaImage]:
        #     #save file wrong
        #     titleName=titleName+"-"+result+".txt"
        #     titleName=titleName.replace(":"," ")
        #     titleName=titleName.replace("'","")
        #     file=open(titleName,'w')
        #     file.write(captchaImage)
        #     file.close()
        #     saveCheck[captchaImage]=False
        end=time.time()
        
        encrypted_message = encrypt(result, keyEncrypt)
        isCheck=True
        encrypt_message="true|"+encrypted_message;
        return encrypt_message
    else:
        user = Users.query.filter_by(merchant_key=key).first()
        if user:
            if user.count_captcha>0:
                user.count_captcha=user.count_captcha-1;
                db.session.commit()
                try:
                    imagedata = base64.b64decode(captchaImage)
                    buf = io.BytesIO(imagedata)
                    image=Image.open(buf)
                    image = image.resize((640, 640))
                    # Decode captcha____________________________________________________________________________________
                    results = model(image)
                except Exception as e:
                    print("Error decode image")
                    return jsonify({"message": "decode error"}), 400
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
                            # print("arr:",t.xyxy[0].name[j],t.xyxy[0].xmin[j])
                print("abcdef: "+str)
                array1.sort()
                array2.sort()
                array3.sort()
                for x in array2:
                    array1.append(x)
                for x in array3:
                    array1.append(x)
                print(array1)
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
                listResult=[]
                print("text:"+strResult)
                ListMistake={}
                
                
                if(len(strResult)>6):
                    for x in strResult:
                        if not x in dict:
                            strResult=strResult.replace(x,'')
                else:
                    strResult=strResult
                    for x in strResult:
                        if not x in dict:
                            if x in ListMistake:
                                strResult=strResult.replace(x,ListMistake.get(x))
                            else:
                                strResult=strResult.replace(x,list(dict.keys())[0])
                for y in strResult:
                        strResult=strResult.replace(y,dict[y])
                print("ket qua:"+strResult)
                listResult.append(strResult)
                strResult=strsave
                # Ket thuc decode captcha______________________________________________________________________
                # print(dict)
                # check gần đúng-------------------------
                # for x in strResult:
                #     if not x in dict:
                #         # print("x not in dict",x)
                #         dict[x]=-1
                #         for value in dict.values():
                #             dict[x]=value
                #             strResult=strsave
                #             for y in strResult:
                #                 strResult=strResult.replace(y,dict[y])
                #             list.append(strResult)
                #             strResult=strsave
                #     else:
                #         strResult=strResult.replace(x,dict[x])
                # list.append(strResult)
                index=0
                saveResult[captchaImage]=DataSave(listResult,start)
                # saveIndex[captchaImage]=index
                # ------------------------------------------------
                # print(dict)
                # print("list:",list)
                result = ''.join([i for i in strResult if i.isdigit()])
                for item in listResult:
                    if not item.isdigit():
                        listResult.remove(item)
                end=time.time()
                # print("strcompare",strcompare)   
                # saveCheck[captchaImage]=True
                print("listResult[0]",listResult[0])
                # print(type(listResult[0]))

                # post data history
                url="http://157.245.200.170:80/api/admin/account/save-captcha-history"
                params={"merchantKey":key,"userIp":request.remote_addr,"captcha":listResult[0]}
                username="adminvietanh"
                password="vanhngoc"
                try:
                    response=session.post(url,auth=(username,password),json=params)
                    print("response"+response)
                    response.close()
                except Exception as e:
                    print(e)
                encrypted_message = encrypt(listResult[0], keyEncrypt)
                
                encrypted_message="true|"+encrypted_message
                isCheck=True
                return encrypted_message
            return jsonify({"message": "your captcha is out"}), 423
        return jsonify({"message": "can't found user"}), 401
def solve2():
    global isCheck
    ip_address = request.remote_addr
    response=jsonify({"message": "spam"}), 508
    print("ip_address:",ip_address)
    if ip_address in ipDict:
        print("count:",ipDict[ip_address])
        ipDict[ip_address]=ipDict[ip_address]+1
    else:
        ipDict[ip_address]=0
    if ipDict[ip_address]>2:
        ipDict[ip_address]-=1
        if(ip_address in ipLockTime):
            if(ipLockTime[ip_address]>time.time()):
                # ipLockTime[ip_address]=time.time()+30
                return jsonify({"message": "spam"}), 508
            else:
                isCheck=False
                response= predict2()
                print("isCheck:",isCheck)
                if(isCheck):
                    ipDict[ip_address]-=1
                    del ipLockTime[ip_address]
                else:
                    ipLockTime[ip_address]=time.time()+60
                    return jsonify({"message": "spam "}), 508
        else:
            ipLockTime[ip_address]=time.time()+60
            return jsonify({"message": "spam"}), 508
    else:
        isCheck=False
        response= predict2()
        if(isCheck):
            ipDict[ip_address]-=1
    return response
def test():
    captchaImage=request.form.get('captcha')
    imagedata = base64.b64decode(captchaImage)
    buf = io.BytesIO(imagedata)
    image=Image.open(buf)
    image = image.resize((640, 640))
    results = model(image)
    t=results.pandas();
    res= decodeCaptcha(t);
    return jsonify({"message":res}), 200