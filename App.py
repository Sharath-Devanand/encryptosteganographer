from flask import Flask, render_template, url_for, request, redirect,jsonify
from datetime import datetime
import cv2
import numpy
import base64
from PIL import Image
import io
from DIP_AES import *
from DIP_Stegano import *

app = Flask(__name__,static_folder='static',
            template_folder='templates')


# decorators @ for app routing
@app.route('/b', methods = ["POST", "GET"])
def encryptor():

    megOnPage = ""  # Message for users
    
    if request.method == "POST":

        # Store the image file, hey and text
        image = request.files["file"]
        key = request.form["key"]
        text = request.form["InputMess"]
        img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_COLOR)

        a=AES_Encrypt(text,key)
        if(len(a)>int(img.shape[0]*img.shape[1]/3)):
            megOnPage = "Please reduce the data for encryption or upload bigger image"
            return (render_template('b.html',img='',message=megOnPage))
        else:
            c=encode(a,img)
            _, im_arr = cv2.imencode('.png', c)  # im_arr: image in Numpy one-dim array format.
            im_bytes = im_arr.tobytes()
            im_b64 = base64.b64encode(im_bytes)
            img_base64=im_b64.decode()
            return (render_template('b.html',img="data:image/png;base64,"+img_base64,showBtN1=True))
    else:
        return (render_template('b.html'))

@app.route('/g', methods =["POST","GET"] )
def decryptor():

    if request.method == "POST":

        # Store the image and key
        image = request.files["image1"]
        key = request.form["key1"]
        img = cv2.imdecode(numpy.fromstring(request.files['image1'].read(), numpy.uint8), cv2.IMREAD_COLOR)
        b=decode(img)
        z=AES_Decrypt(b,key)
        return (render_template('b.html',text=z,showBtN=True))
    else:
        return (redirect(url_for('encryptor')))
@app.route('/', methods = ["GET"])
def landing():
    return (redirect(url_for('encryptor')))

if __name__ == "__main__":
    app.run(port= 1000, debug=True)
