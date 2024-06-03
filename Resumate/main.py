import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from flask import make_response
import fitz
from io import BytesIO
import binascii
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy_transformers, spacy
import re

app = Flask(__name__)
app.config["MONGO_URI"]="enter-mongodb-connection-string"
mongo=PyMongo(app)

@app.route('/')
def index():
    #message = request.args.get('message')
    return render_template('loginpage.html')

@app.route('/login_page',methods=['POST'])
def login_page():
    return render_template('loginpage.html')

@app.route('/loginpage', methods=['POST'])
def loginpage():
    entered_email = request.form['email']
    entered_password = request.form['pass']



    login_user = mongo.db.user1.find_one({"email": entered_email, "password": entered_password})

    if login_user:
        return redirect(url_for('next_page'))
    else:
        return render_template('loginpage.html', message="Invalid credentials")


@app.route('/next_page')
def next_page():
    return render_template('mainpage.html')

@app.route('/register')
def register():
    return render_template('SignupPage.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    email = request.form['userid']
    password = request.form['pass']
    confirm_password = request.form['confirm_pass']
    print("email=", email)
    print("password =", password)
    print("confirm password =", confirm_password)

    # Check if the email is in a valid format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render_template('SignupPage.html', message="Invalid email format. Please enter a valid email address.")

    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        return render_template('SignupPage.html', pw_message="INVALID FORMAT: min 8 characters, at least 1 letter & 1 digit.")
    
    login_user = mongo.db.user1.find_one({"email": email})

    if login_user:
        return render_template('loginpage.html', message="User already exists! Please login.")
    elif password != confirm_password:
        return render_template('SignupPage.html', error_message="Passwords do not match. Please try again.")
    else:
        mongo.db.user1.insert_one({"email": email, "password": password})
        return render_template('loginpage.html', message="Account created successfully! Please login.")

@app.route('/logout', methods=['POST'])
def logout():
    # Logic to handle logout, e.g., clearing session data if any
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileUpload' not in request.files:
        return "No file uploaded", 400
    uploaded_file = request.files['fileUpload']
    if uploaded_file.filename == '':
        return "No file selected", 400
    return '', 204

@app.route('/process', methods=['POST'])
def processfile():
    if 'fileUpload' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    if 'jobDescription' not in request.form:
        return jsonify({"error": "No job description provided"}), 400

    uploaded_file = request.files['fileUpload']
    if uploaded_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        pdf_data = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        extracted_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            extracted_text += page.get_text()

        job_description = request.form['jobDescription']
        matchpercentage = cosine_check(extracted_text, job_description)
        return jsonify({"matchPercentage": matchpercentage})
    except Exception as e:
        logging.error("Error occurred while processing PDF", exc_info=True)
        return jsonify({"error": "Error occurred while processing PDF"}), 500

def cosine_check(extracted_text, job_description):
    #load the model
    nlp = spacy.load('path-to-spacy-model') # insert path to the folder 'model-best' from one among the two models. we chose model-best from output2 since it performs better

    final_text = ""
    doc = nlp(extracted_text)
    for ent in doc.ents:    
        final_text = final_text + ent.text + "\n" 

    resume_job_list = [final_text, job_description]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(resume_job_list)
    matchpercentage = cosine_similarity(count_matrix)[0][1]
    print(matchpercentage)
    return round(matchpercentage * 100, 2)


if __name__ == '__main__':
    app.run(debug=True)