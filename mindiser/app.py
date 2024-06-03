import pickle
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import numpy as np
from flask_cors import CORS
import google.generativeai as genai
import secrets
import firebase_admin
from firebase_admin import credentials, db, auth

app = Flask(__name__)
CORS(app)

# Configure the generative AI model
genai.configure(api_key="AIzaSyB6bZ-JMG0D9s6qgEVSZ6BglODCNj9KHAY")

app.secret_key = secrets.token_hex(16)

# Initialize the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

depression_model = pickle.load(open('models/rf_model_depression.pkl', 'rb'))
anxiety_model = pickle.load(open('models/rf_model_anxiety.pkl', 'rb'))
stress_model = pickle.load(open('models/rf_model_stress.pkl', 'rb'))


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/tracker')
def tracker():
    return render_template('tracker.html')

@app.route('/community')
def community():
    return render_template('community.html')
@app.route('/qoutes')
def qoutes():
    return render_template('qoutes.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        form_data = request.form

        input_data = [
            int(form_data['q1']), int(form_data['q2']), int(form_data['q3']), int(form_data['q4']), int(form_data['q5']),
            int(form_data['q6']), int(form_data['q7']), int(form_data['q8']), int(form_data['q9']), int(form_data['q10']),
            int(form_data['q11']), int(form_data['q12']), int(form_data['q13']), int(form_data['q14']), int(form_data['q15']),
            int(form_data['q16']), int(form_data['q17']), int(form_data['q18']), int(form_data['q19']), int(form_data['q20']),
            int(form_data['q21'])
        ]

        input_array = np.array(input_data).reshape(1, -1)

        try:
            depression_prediction = depression_model.predict(input_array)[0]
            anxiety_prediction = anxiety_model.predict(input_array)[0]
            stress_prediction = stress_model.predict(input_array)[0]

            return render_template('predict.html', 
                                   depression_prediction=depression_prediction,
                                   anxiety_prediction=anxiety_prediction,
                                   stress_prediction=stress_prediction)
        except Exception as e:
            return render_template('error.html', error=str(e))

@app.route('/process-message', methods=['POST'])
def process_message():
    print("Received")
    user_input = request.json['message']
    bot_response = generate_bot_response(user_input)
    
    print(bot_response)
    return jsonify({'bot_response': bot_response})

def generate_bot_response(user_input):
    convo = model.start_chat(history=[{"role": "model", "parts": ["Hey there! 👋 It's so great to chat with you today. What's been keeping you busy lately? 😊"]}])
    convo.send_message(user_input)
    
    bot_response = convo.last.text
    
    return bot_response



if __name__ == "__main__":
    app.run(debug=True)

