from flask import Flask, render_template, request,redirect, url_for, jsonify,flash
from tensorflow.keras.models import load_model  
from tensorflow.keras.applications.imagenet_utils import *
import PIL
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from flask_pymongo import PyMongo
import app
from flask_pymongo import PyMongo
from flask import make_response
import fitz
from io import BytesIO
import binascii
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

app.config["MONGO_URI"]="mongodb://localhost:27017/mydb"
mongo=PyMongo(app)

model = None

def load_my_model():
    global model
    model = load_model('C:/Users/aleen/OneDrive/Desktop/Desktop/project/model_resnet50.h5')  

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    
    e_username = request.form['username']
    e_password = request.form['password']

    login_user = mongo.db.user.find_one({"username": e_username, "password": e_password})
    if login_user:
        return render_template('index.html')
    else:
         return render_template('newuser.html',message="No User Found")

@app.route('/new', methods=['POST'])
def new():
    
    un = request.form['username']
    pw = request.form['password']

    login_user = mongo.db.user.insert_one({"username": un, "password": pw})
    if login_user:
        return render_template('login.html')
    


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file found')
        
        file = request.files['file']
        image_path = "./images/" + file.filename
        if not os.path.exists("./images/"):
            os.makedirs("./images/")

        image_path = os.path.join("./images/", file.filename)
        file.save(image_path)        

        if file.filename == ' ':
            return render_template('index.html', message='No selected file')

        if file:
            img = image.load_img(image_path, target_size=(100, 100))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            prediction = model.predict(img_array)
            p=list((prediction*100).astype('int'))
            pp=list(p[0])
            index = pp.index(max(pp))
            name_class=['Eczema', 'Melanoma']
            prediction_text=plt.title(name_class[index])
            text=str(prediction_text)
            parts = text.split(", ")
            third_attribute = parts[2].strip("')")
            return render_template('result.html', prediction_text='{}'.format(third_attribute))

if __name__ == "__main__":
    load_my_model()
    app.run(port=3000, debug=True)
