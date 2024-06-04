

from flask import Flask, render_template, request, jsonify, send_file
import pyttsx3
import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.translate.bleu_score import sentence_bleu
import cv2
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model

app = Flask(__name__)

# Load the trained captioning model
model = load_model("C:/Users/DELL/Desktop/one/MiniProject/web_flask/thecorrectone.h5")

# Load vocabulary
with open('words_to_indices.p', 'rb') as f:
    words_to_indices = pickle.load(f)

with open('indices_to_words.p', 'rb') as f:
    indices_to_words = pickle.load(f)

# Load ResNet-50 model for feature extraction
base_model = ResNet50(weights='imagenet')
model_resnet = Model(inputs=base_model.inputs, outputs=base_model.layers[-2].output)

max_length = 40

def greedy_search(photo):
    photo = photo.reshape(1, 2048)
    in_text = '<start>'
    for i in range(max_length):
        sequence = [words_to_indices.get(s, 0) for s in in_text.split()]
        sequence = pad_sequences([sequence], maxlen=max_length, padding='post')
        y_pred = model.predict([photo, sequence], verbose=0)
        y_pred = np.argmax(y_pred)
        word = indices_to_words.get(y_pred, 'Unk')
        in_text += ' ' + word
        if word == '<end>':
            break
    final = in_text.split()
    final = final[1:-1]
    return final

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/second-page', methods=['GET'])
def second_page():
    return render_template('second-page.html')

@app.route('/generate-captions', methods=['POST'])
def generate_captions():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    # Preprocess the image
    img = load_img(filepath, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Extract features using ResNet-50
    photo = model_resnet.predict(img_array)

    # Generate caption using the loaded model
    candidate = greedy_search(photo)
    caption = ' '.join(candidate)

    return jsonify({'captions': [caption]})

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text', '')

    if text:
        engine = pyttsx3.init()
        audio_file = 'caption_audio.mp3'
        engine.save_to_file(text, audio_file)
        engine.runAndWait()

        return send_file(audio_file, as_attachment=True, mimetype='audio/mpeg')
    return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(port=3000, debug=True)
