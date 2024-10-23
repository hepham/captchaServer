import base64
import os
path="image"
text_files = [f for f in os.listdir(path) if f.endswith('.txt')]
outputPath="output"
if not (os.path.exists(outputPath)):
    os.makedirs(outputPath)
for file in text_files:
    with open(f"{path}/{file}","r",encoding="utf-8")as f:
        base64String=f.read()
        image=base64.b64decode(base64String)
        filename=file[:-4]+".png"
        with open(f"{outputPath}/{filename}","wb")as g:
            g.write(image)