from flask import Flask, make_response, request, jsonify, render_template, redirect, session, url_for
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn as nn
import firebase_admin
from firebase_admin import credentials, auth
app = Flask(__name__)
CORS(app)


cred = credentials.Certificate("id.json")

firebase_admin.initialize_app(cred)
app.secret_key = 'your_secret_key'

model_name_or_path = 'unitary/toxic-bert'
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_name_or_path)
model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=model_name_or_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

def check_text_toxicity(text) -> dict:
    try:
        # Tokenize and encode the input text
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        inputs = {key: val.to(device) for key, val in inputs.items()}
        
        # Perform model inference
        outputs = model(**inputs)
        
        # Calculate probabilities
        sigmoid = nn.Sigmoid()
        probabilities = sigmoid(outputs.logits)
        probabilities = probabilities.to('cpu').detach().numpy() * 100
        
        # Map label indices to label names
        id2label = model.config.id2label
        
        # Initialize result dictionary
        result = {
            'status': 1,
            'message': 'Request successful',
            'response': {
                'toxic': 0,
                'severe_toxic': 0,
                'obscene': 0,
                'threat': 0,
                'insult': 0
            }
        }
        
        # Update result dictionary based on model predictions
        for index, label_name in id2label.items():
            result['response'][label_name] = round(float(probabilities[0][index]), 2)
        
        return result
        print(result)
    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")
        return {
            'status': -1,
            'message': f'Error at the model level: {error_message}',
            'response': {}
        }


@app.route('/')
def home():
    if not session.get('username'):
            return render_template('authentication.html')
    return render_template('index.html',username=session.get('username'))

@app.route('/api/text')
def api_text():
    text = request.args.get('jtext')
    print(text)
    if text:
        output = check_text_toxicity(text)
        toxicity_values = output['response']
        overall_toxicity = False
        
        for value in toxicity_values.values():
            if value > 50:
                overall_toxicity = True
                break
        output['overall_toxicity'] = overall_toxicity
        
        return jsonify(output)
    else:
        return jsonify({'error': 'Text field is empty'})
@app.route('/post')
def post():
            return render_template('post.html')

@app.route('/webs11')
def webs():
        if not session.get('username'):
            return render_template('webs.html')
        return render_template('webs.html')

@app.route('/post1')
def post1():
    text = request.args.get('jtext')
     # Print the text to the terminal
    if text:
        output = check_text_toxicity(text)
        toxicity_values = output['response']
        overall_toxicity = False
        
        for value in toxicity_values.values():
            if value > 50:
                overall_toxicity = True
                break
        output['overall_toxicity'] = overall_toxicity
        
        print(output)  

        return jsonify(output)
    else:
        return jsonify({'error': 'Text field is empty'})

@app.route('/index')
def index():
            return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('authentication.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        user = auth.get_user_by_email(email)
        session['username'] = email
        response = make_response('Done')
        return response
        
    else:
        if not session.get('username'):
            return render_template('authentication.html')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

