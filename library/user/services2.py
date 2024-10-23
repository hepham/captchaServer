from datetime import datetime 
from datetime import timezone
import base64

import time
from PIL import Image
import io
from flask import jsonify, request
import os

# PyTorch Hub
import numpy as np
import cv2
import torch
import json
import requests
from library.encrypt import encrypt
from library.extension import db
from library.library_ma import UserSchema
from library.model import Users,DataSave
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
model = torch.hub.load('ultralytics/yolov5', 'custom', 'newModel.pt')
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# convert text character to special character
alphabet={"and":"&","acong":"@","thang":"#","per":"%","dolar":"$"}
ListMistake={"j":"l","l":"j","6":"s","s":"6","2":"z","z":"2","z":"7","7":"z","e":"f","f":"e"}
SaveDataSolve={}
ipDict={}
saveCheck={}
ipLockTime={}
session=requests.Session()
file=open("privateKey.pem",'r')
try:
    private_key_string=file.read()
finally:
    file.close()
file=open("publicKey.pem",'r')
try:
    public_key_string=file.read()
finally:
    file.close()
# with open('privateKey.pem', 'r') as f:
#     private_key_string = f.read()
    
# with open('publicKey.pem', 'rb') as f:
#     public_key_string = f.read()
folderSaveImage="Image"
if not os.path.exists(folderSaveImage) :
    os.makedirs(folderSaveImage)

def base64StringToImage(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64
# this function for decode image yolov5 to number
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
    # alphabet={}
    # for j in range(len(t.xyxy[0].name)):
    #     if (t.xyxy[0].name[j] == 'and'):
    #         alphabet[t.xyxy[0].name[j]] = '&'
    #     elif (t.xyxy[0].name[j] == 'acong'):
    #         alphabet[t.xyxy[0].name[j]]= '@'
    #     elif (t.xyxy[0].name[j] == 'thang'):
    #         alphabet[t.xyxy[0].name[j]] = '#'
    #     elif (t.xyxy[0].name[j] == 'per'):
    #         alphabet[t.xyxy[0].name[j]]= '%'
    #     elif (t.xyxy[0].name[j] == 'dolar'):
    #         alphabet[t.xyxy[0].name[j]] = '$'
    #     else: alphabet[t.xyxy[0].name[j]] = t.xyxy[0].name[j]
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
                if t.xyxy[0].name[j] in alphabet:
                    strResult=strResult+alphabet[t.xyxy[0].name[j]]
                else:strResult=strResult+t.xyxy[0].name[j]
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
                if t.xyxy[0].name[j] in alphabet:
                    strcompare = strcompare + alphabet[t.xyxy[0].name[j]]
                else:strcompare = strcompare + t.xyxy[0].name[j]
    dataConvert={}
    dataTemp=[]
    index=0;
    # print(strResult)
    # print(strcompare)
    for x in strcompare:
        index+=1
        if not x.isdigit():
            dataTemp.append(x)
        else:
            if(len(dataTemp)==0):
                dataConvert[strcompare[index-1]]=x
            if len(dataTemp)==1:
                dataConvert[dataTemp[0]]=x
            else:
                for k in dataTemp:
                    if not k in dataConvert:
                        dataConvert[k]=x
            dataTemp.clear()
    # print("encode:",strResult)
    # print("decode",dataConvert)
    for character in strResult:
        if not character in dataConvert:
            # print("character",character)
            # print(ListMistake.get(character))
            if (character in ListMistake) and(ListMistake.get(character)in dataConvert):
                dataConvert[character]=dataConvert[ListMistake[character]]
            else:
                strResult=strResult.replace(character,"")
    # print("encode2:",strResult)
    for character in strResult:
        if(character in dataConvert):
            strResult=strResult.replace(character,dataConvert[character])
        
        
    
    return strResult
    
# this funtion for solving captcha
def predict(captchaImage,timeStart):
    result="error";
    try:
        imagedata = base64.b64decode(captchaImage)
        buf = io.BytesIO(imagedata)
        image=Image.open(buf)
        image = image.resize((640, 640))
        # Decode captcha____________________________________________________________________________________
        img = model(image)
        result=decodeCaptcha(img.pandas())
        SaveDataSolve[captchaImage]=DataSave(result,timeStart)
    except Exception as e:
        print("Error decode image")
    
    return result
def solver():
    start=time.time()
    message=request.form.get('data')
    captcha2=request.form.get('captcha')
    key=request.form.get('key')
    private_key = RSA.import_key(private_key_string)
    cipher = PKCS1_v1_5.new(private_key)
    try:
        encrypted_bytes = base64.b64decode(message)
        captcha1 = cipher.decrypt(encrypted_bytes, None)
    except Exception as e:
        print("Error RSA decrypt")
        return jsonify({"message": "decode error"}), 400
    captchaImage=captcha1.decode('utf-8')+captcha2
    # loai bo cac gia tri khoi dictionary sau 300s
    keyRemove=[]
    for keyR in SaveDataSolve:
        if(start-SaveDataSolve[keyR].timesave> 300):
            keyRemove.append(keyR)
    for keyR in keyRemove:
        del(SaveDataSolve[keyR])
    saveResultLength=len(SaveDataSolve)
    # do dai cua dict=10000  
    while(saveResultLength>10000):
        # lay phan tu dau tien cua dictionary va loai bo chung
        res = next(iter(SaveDataSolve))
        del(SaveDataSolve[res])   
        saveResultLength=len(SaveDataSolve)
    
    if captchaImage in SaveDataSolve:
         # save file
        
        result=SaveDataSolve[captchaImage].captchaDecode
        if captchaImage in saveCheck and saveCheck[captchaImage]:
            #save file wrong
            titleName=str(datetime.fromtimestamp(int(start)))
            titleName=titleName+"-"+result+".txt"
            titleName=titleName.replace(":"," ")
            titleName=titleName.replace("'","")
            # with open(f"image/{titleName}","w")as f:
            #     f.write(captchaImage)
            saveCheck[captchaImage]=False
        if captchaImage not in saveCheck:
            saveCheck[captchaImage]=True
        public_key = RSA.import_key(public_key_string)
        cipher = PKCS1_v1_5.new(public_key)
        res_bytes=str.encode(result)
        encrypted_message = cipher.encrypt(res_bytes)
        isCheck=True
        encrypt_message="true|"+base64.b64encode(encrypted_message).decode("utf-8");
        # print(encrypt_message)
        return encrypt_message,200
    else:
        try:
            user = Users.query.filter_by(merchant_key=key).first()
        except Exception as e:
            return jsonify({"message": "something wrong"}), 401
        if(user):
            if user.count_captcha>0:
                # print(user.count_captcha)
                user.count_captcha=user.count_captcha-1;
                db.session.commit()
                result=predict(captchaImage,start)
                if result=="error":
                    return jsonify({"message": "decode error"}), 400
                else:
                    # post data history
                    url="http://157.245.200.170:80/api/admin/account/save-captcha-history"
                    params={"merchantKey":key,"userIp":request.remote_addr,"captcha":result}
                    username="adminvietanh"
                    password="vanhngoc"
                    # try:
                    #     response=session.post(url,auth=(username,password),json=params)
                    #     print(response)
                    #     response.close()
                    # except Exception as e:
                    #     print(e)
                    
                    public_key = RSA.import_key(public_key_string)
                    cipher = PKCS1_v1_5.new(public_key)
                    res_bytes=str.encode(result)
                    encrypted_message = cipher.encrypt(res_bytes)
                    # print ("result:",result)
                    encrypt_message="true|"+base64.b64encode(encrypted_message).decode("utf-8");
                    return encrypt_message,200
            return jsonify({"message": "your captcha is out"}), 423
        return jsonify({"message": "can't found user"}), 401
        
def solveCaptchaApi():
    global isCheck
    ip_address = request.remote_addr
    response=jsonify({"message": "spam"}), 508
    # print("ip_address:",ip_address)
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
                response,status= solver()

                if(status):
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
        response,status= solver()
      
        # print("response.status_code",status)
     
        if(status==200):
            ipDict[ip_address]-=1
    return response
def test():
    start=time.time()
    captcha=request.form.get('captcha')
    
    res=predict(captcha,start)
    return jsonify({"message":res}),200
def detectapi():
    global isCheck
    # print(datetime.now(datetime.timezone.utc).strftime("%d%Y%m%H"))
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
    for keyR in SaveDataSolve:
        if(start-SaveDataSolve[keyR].timesave> 300):
            keyRemove.append(keyR)
    for keyR in keyRemove:
        del(SaveDataSolve[keyR])
    saveResultLength=len(SaveDataSolve)
    # do dai cua dict=10000  
    while(saveResultLength>10000):
        # lay phan tu dau tien cua dictionary va loai bo chung
        res = next(iter(SaveDataSolve))
        del(SaveDataSolve[res])   
        saveResultLength=len(SaveDataSolve)
    
    if captchaImage in SaveDataSolve:
        result=SaveDataSolve[captchaImage].captchaDecode
        public_key = RSA.import_key(public_key_string)
        cipher = PKCS1_v1_5.new(public_key)
        res_bytes=str.encode(result)
        encrypted_message = encrypt(result, keyEncrypt)
        isCheck=True;
        encrypt_message="true|"+encrypted_message
        # print(encrypt_message)
        return encrypt_message,200
    else:
        user = Users.query.filter_by(merchant_key=key).first()
        if user:
            if user.count_captcha>0:
                # print(user.count_captcha)
                user.count_captcha=user.count_captcha-1;
                db.session.commit()
                result=predict(captchaImage,start)
                if result=="error":
                    return jsonify({"message": "decode error"}), 400
                else:
                    # post data history
                    url="http://157.245.200.170:80/api/admin/account/save-captcha-history"
                    params={"merchantKey":key,"userIp":request.remote_addr,"captcha":result}
                    username="adminvietanh"
                    password="vanhngoc"
                    # try:
                    #     response=session.post(url,auth=(username,password),json=params)
                    #     print(response)
                    #     response.close()
                    # except Exception as e:
                    #     print(e)
                    encrypted_message = encrypt(result, keyEncrypt)
                
                encrypted_message="true|"+encrypted_message
                return encrypted_message,200
            return jsonify({"message": "your captcha is out"}), 423
        return jsonify({"message": "can't found user"}), 401
def detectapiV2():
    global isCheck
    # print(datetime.now(datetime.timezone.utc).strftime("%d%Y%m%H"))
    keyEncrypt=int(datetime.now(timezone.utc).strftime("%d%Y%m%H"))
    strings = datetime.now(timezone.utc).strftime("%d,%m,%H")
    print(strings)
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
    for keyR in SaveDataSolve:
        if(start-SaveDataSolve[keyR].timesave> 300):
            keyRemove.append(keyR)
    for keyR in keyRemove:
        del(SaveDataSolve[keyR])
    saveResultLength=len(SaveDataSolve)
    # do dai cua dict=10000  
    while(saveResultLength>10000):
        # lay phan tu dau tien cua dictionary va loai bo chung
        res = next(iter(SaveDataSolve))
        del(SaveDataSolve[res])   
        saveResultLength=len(SaveDataSolve)
    
    if captchaImage in SaveDataSolve:
        result=SaveDataSolve[captchaImage].captchaDecode
        public_key = RSA.import_key(public_key_string)
        cipher = PKCS1_v1_5.new(public_key)
        res_bytes=str.encode(result)
        encrypted_message = encrypt(result, keyEncrypt)
        isCheck=True;
        encrypt_message="true|"+encrypted_message
        # print(encrypt_message)
        return encrypt_message,200
    else:
        user = Users.query.filter_by(merchant_key=key).first()
        if user:
            if user.count_captcha>0:
                # print(user.count_captcha)
                user.count_captcha=user.count_captcha-1;
                db.session.commit()
                result=predict(captchaImage,start)
                if result=="error":
                    return jsonify({"message": "decode error"}), 400
                else:
                    # post data history
                    url="http://157.245.200.170:80/api/admin/account/save-captcha-history"
                    params={"merchantKey":key,"userIp":request.remote_addr,"captcha":result}
                    username="adminvietanh"
                    password="vanhngoc"
                    # try:
                    #     response=session.post(url,auth=(username,password),json=params)
                    #     print(response)
                    #     response.close()
                    # except Exception as e:
                    #     print(e)
                    encrypted_message = encrypt(result, keyEncrypt)
                
                encrypted_message="true|"+encrypted_message
                return encrypted_message,200
            return jsonify({"message": "your captcha is out"}), 423
        return jsonify({"message": "can't found user"}), 401
def solvedetectApi():
    global isCheck
    ip_address = request.remote_addr
    response=jsonify({"message": "spam"}), 508
    # print("ip_address:",ip_address)
    if ip_address in ipDict:
        # print("count:",ipDict[ip_address])
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
                response,status= detectapi()
                # print("status:",status)
                if(status):
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
        response,status= detectapi()
        if(status):
            ipDict[ip_address]-=1
    return response
def solvedetectApiV2():
    global isCheck
    ip_address = request.remote_addr
    response=jsonify({"message": "spam"}), 508
    # print("ip_address:",ip_address)
    if ip_address in ipDict:
        # print("count:",ipDict[ip_address])
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
                response,status= detectapiV2()
                # print("status:",status)
                if(status):
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
        response,status= detectapiV2()
        if(status):
            ipDict[ip_address]-=1
    return response