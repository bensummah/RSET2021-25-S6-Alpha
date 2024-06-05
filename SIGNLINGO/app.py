import pickle
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import mysql.connector
import base64
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to load the trained model and scaler based on the input language
def load_model(input_language):
    model_file = 'model.p' if input_language == 'asl' else 'model1.p'
    with open(model_file, 'rb') as f:
        model_data = pickle.load(f)
    return model_data['model'], model_data['scaler']

# Function to extract hand landmarks from an image
def extract_hand_landmarks(image, input_language):
    data_aux = []

    # Convert image from BGR to RGB
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect hand landmarks
    max_hands = 1 if input_language == 'asl' else 2
    with mp_hands.Hands(static_image_mode=False, max_num_hands=max_hands, min_detection_confidence=0.7) as hands:
        results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                data_aux.append(landmark.x)
                data_aux.append(landmark.y)
                data_aux.append(landmark.z)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        return None, image

    # Ensure data_aux has a fixed length based on the input language
    required_length = 21 * 3 * max_hands
    if len(data_aux) < required_length:
        data_aux.extend([0] * (required_length - len(data_aux)))
    elif len(data_aux) > required_length:
        data_aux = data_aux[:required_length]
    
    return np.array(data_aux).reshape(1, -1), image

# Database connection setup
def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="anushri"
    )
    return connection

# Function to get the image path from the database
def get_image_data(label, output_language):
    connection = connect_db()
    cursor = connection.cursor()
    label_str = str(label)
    query = "SELECT isl_img FROM translation_table WHERE label = %s" if output_language == 'isl' else "SELECT asl_img FROM translation_table WHERE label = %s"
    cursor.execute(query, (label_str,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result and result[0]:
        # Convert BLOB to base64 string
        img_blob = result[0]
        img_base64 = base64.b64encode(img_blob).decode('utf-8')
        return img_base64
    return None

@app.route('/')
def index():
    return render_template('index.html')

'''@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '2024':
        return redirect(url_for('translation'))
    else:
        return 'Incorrect username or password!', 401'''

@app.route('/translation')
def translation():
    return render_template('translation.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('frame')
def handle_frame(data):
    start_time = time.time()
    
    img_data = base64.b64decode(data['image'])
    input_language = data['input_language']
    output_language = data['output_language']
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    landmarks, annotated_image = extract_hand_landmarks(frame, input_language)
    
    if landmarks is not None:
        model, scaler = load_model(input_language)
        landmarks = scaler.transform(landmarks)
        prediction = model.predict(landmarks)
        label = prediction[0]
        image_data = get_image_data(label, output_language)
    else:
        label = 'No hand detected'
        image_data = None

    _, buffer = cv2.imencode('.jpg', annotated_image)
    img_str = base64.b64encode(buffer).decode('utf-8')
    emit('response_frame', {'image': img_str, 'label': label, 'image_data': image_data})

    end_time = time.time()
    print(f"Frame processed in {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    socketio.run(app, debug=True)
