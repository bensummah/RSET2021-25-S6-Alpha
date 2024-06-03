#venv/Scripts/activate
#Get-ExecutionPolicy -List
#Set-ExecutionPolicy -ExecutionPolicy /// -Scope /////

from flask import Flask,render_template,request

import mysql.connector

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img,img_to_array
import os
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt


app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost", 
    user="root",
    password="amith",
    database="foodshazam"
)
cursor = db.cursor()

@app.route('/',methods=['GET'])
def nice():
    return render_template('imgupd.html')

@app.route('/',methods=['POST'])
def predict():
    # model=VGG16()
    img=request.files['image-file']
    img_path="./images/"+img.filename
    img.save(img_path)

    model = load_model('C:/Users/ami1p/Downloads/my_model_pain150.h5')
    # img_path = 'C:/Users/ami1p/Downloads/foodclassification/Food Classification/burger/001.jpg'.encode('ascii', 'ignore').decode()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))

    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.array([img_array]) 
    print(img_array)

    class_names=["burger","butter_naan","chai","chapati","chole_bhature","dal_makhani","dhokla","fried_rice","idli","jalebi","kaathi_rolls","kadai_paneer","kulfi","masala_dosa","momos","paani_puri","pakode","pav_bhaji","pizza","samosa"] #names in ""

    predictions = model.predict(img_array)
    print(predictions)
    class_id = np.argmax(predictions, axis = 1)
    print(class_id)
    print(class_names[class_id.item()])
    query = "SELECT * FROM nutritional_information WHERE fname = %s"
    cursor.execute(query, (class_names[class_id.item()],))
    data = cursor.fetchall()

    d=[]
    dt=list(data[0])
    title=['carbohydrate','fat','protein']
    d.append(dt[2])
    d.append(dt[3])
    d.append(dt[5])
    plt.figure(facecolor='black')
    plt.pie(d, labels=title,textprops={'color': 'white'})
    plt.savefig('C:/Users/ami1p/OneDrive/Desktop/food_kandupidichilla/static/styles/pie_chart.png')
    print(data)

    query1 = "SELECT ingredients FROM food_items WHERE name = %s"
    cursor.execute(query1, (class_names[class_id.item()],))
    data1 = cursor.fetchone()
    print(data)
    if data and data1:
        ingredients = data1[0].split(', ')
        return render_template('biriyani.html',prediction=class_names[class_id.item()], ingredients=ingredients,data=data)
    else:
        return render_template('not_found.html',prediction=class_names[class_id.item()])

@app.route('/bir',methods=['POST'])
def search():
    if request.method == 'POST':
        fn = request.form['food_name']
        fn= fn.replace(" ","_")
        query = "SELECT * FROM nutritional_information WHERE fname = %s"
        cursor.execute(query, (fn,))
        data = cursor.fetchall()

        d=[]
        dt=list(data[0])
        title=['carbohydrate','fat','protein']
        d.append(dt[2])
        d.append(dt[3])
        d.append(dt[5])
        plt.figure(facecolor='black')
        plt.pie(d, labels=title,textprops={'color': 'white'})
        plt.savefig('C:/Users/ami1p/OneDrive/Desktop/food_kandupidichilla/static/styles/pie_chart.png')
        print(data)

        query = "SELECT ingredients FROM food_items WHERE name = %s"
        cursor.execute(query, (fn,))
        data1 = cursor.fetchone()
        if data and data1:
            ingredients = data1[0].split(', ')
            return render_template('biriyani.html', prediction=fn, ingredients=ingredients,data=data)
        else:
            return render_template('not_found.html', food_name=fn)



if __name__=="__main__":
    app.run(port=5502)
