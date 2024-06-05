from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

app = Flask(__name__)

interpreter = None

def load_my_model():
    global interpreter
    interpreter = tf.lite.Interpreter(model_path="copy-directorty-path/detection.tflite")
    interpreter.allocate_tensors()

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('home.html', prediction_text='No file found')
        
        file = request.files['file']
        image_path = "./images/" + file.filename
        file.save(image_path)

        if file.filename == '':
            return render_template('home.html', prediction_text='No selected file')

        if file:
            img = Image.open(image_path).resize((100, 100))
            img_array = np.asarray(img) / 255.0  # Normalize pixel values
            img_array = np.expand_dims(img_array, axis=0)
            
            # Prepare input tensor
            input_details = interpreter.get_input_details()
            interpreter.set_tensor(input_details[0]['index'], img_array.astype(np.float32))
            interpreter.invoke()

            # Get output tensor
            output_details = interpreter.get_output_details()
            output = interpreter.get_tensor(output_details[0]['index'])

            # Get predicted class
            predicted_class_index = np.argmax(output)
            class_names = ['background','carboard','glass','metal','paper','plastic']
            prediction_text = class_names[predicted_class_index]

        return render_template('detec.html', prediction_text='Prediction:{}'.format(prediction_text))

if __name__ == "__main__":
    load_my_model()
    app.run(port=3000, debug=True)
