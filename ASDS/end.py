from flask import Flask, render_template, request, send_from_directory, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import numpy as np
import os

app = Flask(__name__)

model = None

def load_my_model():
    global model
    model = load_model('copy-path-location-/model_resnet50.h5', compile=False)

@app.route('/', methods=['GET'])
def open_home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('home.html', prediction_text='No file found')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('home.html', prediction_text='No selected file')

    if file:
        image_path = os.path.join('images', file.filename)
        file.save(image_path)

        img = image.load_img(image_path, target_size=(100, 100))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        prediction = model.predict(img_array)
        p = (prediction * 100).astype('int')
        pp = list(p[0])
        index = pp.index(max(pp))
        name_class = ['cardboard', 'glass', 'metal', 'paper', 'plastic']
        prediction_text = name_class[index]

        return render_template('detect.html', prediction_text=prediction_text, image_path=image_path)

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Get the prediction and image path from the form data
        prediction_text = request.form.get('prediction')
        image_path = request.form.get('image_path')
    else:
        # Get the prediction and image path from the query parameters (fallback for GET requests)
        prediction_text = request.args.get('prediction')
        image_path = request.args.get('image_path')

    # Set the boolean variables based on the prediction
    plastic = prediction_text == 'plastic'
    metal = prediction_text == 'metal'
    paper = prediction_text == 'paper'
    cardboard = prediction_text == 'cardboard'
    glass = prediction_text == 'glass'

    # Render the result template with the prediction and boolean variables
    return render_template('result.html', prediction_text=prediction_text, image_path=image_path, plastic=plastic, metal=metal, paper=paper, cardboard=cardboard, glass=glass)

@app.route('/footwear')
def footwear():
    return render_template('footwear.html')

@app.route('/home')
def home():
    return render_template('home.html')



if __name__ == "__main__":
    load_my_model()
    if not os.path.exists('images'):
        os.makedirs('images')
    app.run(port=5000, debug=True)
