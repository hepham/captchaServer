import base64
from PIL import Image
import io
from flask import Flask,render_template,request
from flask_cors import CORS, cross_origin
import array
# PyTorch Hub
import numpy as np
import cv2
import torch
model = torch.hub.load('ultralytics/yolov5', 'custom', 'C:/Users\Admin/Desktop/New folder (2)/model.pt')
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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

@app.route('/detect',methods=['POST'])
@cross_origin(origin='*')
def predict():
    # imagefile= request.files['imagefile']
    # image_path="./images/"+imagefile.filename
    # imagefile.save(image_path)
    captchaImage=request.form.get('captcha')
    # imagetemp=chuyen_base64_sang_anh(capchaImage)
    # image=cv2.cvtColor(imagetemp,cv2.COLOR_BGR2RGB)
    imagedata = base64.b64decode(captchaImage)
    buf = io.BytesIO(imagedata)
    image=Image.open(buf)
    image = image.resize((640, 640))
    print(image.size)
    # image=image.resize(640,640)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    results = model(image)
    results.print()  # or .show(), .save()
    results.xyxy[0]  # im predictions (tensor)
    print(results.pandas().xyxy[0])  # im predictions (pandas)
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
                if (results.pandas().xyxy[0].name[j] == 'a1'):
                    results.pandas().xyxy[0].name[j] = '&'
                    str = str + '&'
                elif (results.pandas().xyxy[0].name[j] == 'a2'):
                    results.pandas().xyxy[0].name[j] = '@'
                    str = str + '@'
                elif (results.pandas().xyxy[0].name[j] == 'a3'):
                    results.pandas().xyxy[0].name[j] = '#'
                    str = str + '#'
                elif (results.pandas().xyxy[0].name[j] == 'a4'):
                    results.pandas().xyxy[0].name[j] = '%'
                    str = str + '%'
                elif (results.pandas().xyxy[0].name[j] == 'a5'):
                    results.pandas().xyxy[0].name[j] = '$'
                    str = str + '$'
                else:
                    str = str + results.pandas().xyxy[0].name[j]
    print(str)
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
                if (results.pandas().xyxy[0].name[j] == 'a1'):
                    results.pandas().xyxy[0].name[j] = '&'
                    strcompare = strcompare + '&'
                elif (results.pandas().xyxy[0].name[j] == 'a2'):
                    results.pandas().xyxy[0].name[j] = '@'
                    strcompare = strcompare + '@'
                elif (results.pandas().xyxy[0].name[j] == 'a3'):
                    results.pandas().xyxy[0].name[j] = '#'
                    strcompare = strcompare + '#'
                elif (results.pandas().xyxy[0].name[j] == 'a4'):
                    results.pandas().xyxy[0].name[j] = '%'
                    strcompare = strcompare + '%'
                elif (results.pandas().xyxy[0].name[j] == 'a5'):
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
                if (results.pandas().xyxy[0].name[j] == 'a1'):
                    results.pandas().xyxy[0].name[j] = '&'
                    strcompare = strcompare + '&'
                elif (results.pandas().xyxy[0].name[j] == 'a2'):
                    results.pandas().xyxy[0].name[j] = '@'
                    strcompare = strcompare + '@'
                elif (results.pandas().xyxy[0].name[j] == 'a3'):
                    results.pandas().xyxy[0].name[j] = '#'
                    strcompare = strcompare + '#'
                elif (results.pandas().xyxy[0].name[j] == 'a4'):
                    results.pandas().xyxy[0].name[j] = '%'
                    strcompare = strcompare + '%'
                elif (results.pandas().xyxy[0].name[j] == 'a5'):
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
                if (results.pandas().xyxy[0].name[j] == 'a1'):
                    results.pandas().xyxy[0].name[j] = '&'
                    strcompare = strcompare + '&'
                elif (results.pandas().xyxy[0].name[j] == 'a2'):
                    results.pandas().xyxy[0].name[j] = '@'
                    strcompare = strcompare + '@'
                elif (results.pandas().xyxy[0].name[j] == 'a3'):
                    results.pandas().xyxy[0].name[j] = '#'
                    strcompare = strcompare + '#'
                elif (results.pandas().xyxy[0].name[j] == 'a4'):
                    results.pandas().xyxy[0].name[j] = '%'
                    strcompare = strcompare + '%'
                elif (results.pandas().xyxy[0].name[j] == 'a5'):
                    results.pandas().xyxy[0].name[j] = '$'
                    strcompare = strcompare + '$'
                else:
                    strcompare = strcompare + results.pandas().xyxy[0].name[j]
    print(strcompare)
    i = 0

    while i < len(strcompare) - 1:
        if (strcompare[i + 1].isdigit()):
            str = str.replace(strcompare[i], strcompare[i + 1])
            i = i + 1
        else:
            i = i + 1

    result = ''.join([i for i in str if i.isdigit()])
    print(result)
    return result
    # return render_template("index.html",prediction=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)
