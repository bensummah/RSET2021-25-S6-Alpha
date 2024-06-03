from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, session
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import tensorflow as tf
import joblib
import os
import librosa
from datetime import datetime
import time
import pyaudio
import wave

app = Flask(__name__)
app.secret_key = '1234abcde'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'new_database.db')
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_function'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

@app.route('/predict_realtime', methods=['POST'])
def predict_realtime():
    try:
        prediction = record_audio_and_save_wav()
        predicted_label = int(prediction[0])
        genre_mapping = {0: 'Pop', 1: 'Metal', 2: 'Disco', 3: 'Blues', 4: 'Reggae',
                         5: 'Classical', 6: 'Rock', 7: 'Hip Hop', 8: 'Country', 9: 'Jazz'}
        predicted_genre = genre_mapping.get(predicted_label, "Unknown")
        flash(f"Predicted Genre: {predicted_genre}")
        return jsonify({'genre': predicted_genre})
    except Exception as e:
        print(f"Error during prediction: {e}")
        flash(f"Error: {e}", "error")
        return jsonify({'error': 'Prediction failed'}), 500


def record_audio_and_save_wav(filename="output.wav", duration=10):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    sample_rate = 16000

    p = pyaudio.PyAudio()

    print('Recording...')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=sample_rate,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print('Finished recording')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    waveform, sr = librosa.load("output.wav", sr=16000)

    segment_length = 1.0
    num_segments = int(waveform.shape[0] / (sr * segment_length))
    features = []

    for i in range(num_segments):
        start = int(i * segment_length * sr)
        end = int(start + sr * segment_length)
        segment = waveform[start:end]
        vgg_features = vggish(segment).numpy()
        features.append(vgg_features)

    aggregated_features = np.mean(features, axis=0)
    input_features = aggregated_features.flatten()
    prediction = model.predict(input_features.reshape(1, -1))
    return prediction
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Correct indentation for SearchHistory class
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recommendation(db.Model):
    genre = db.Column(db.String(80), nullable=False)
    song_name = db.Column(db.String(100), primary_key=True)
    artist_name = db.Column(db.String(100))
    link = db.Column(db.String(200))

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    search_term = db.Column(db.String(100), nullable=False)
    predicted_genre = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('search_history', lazy=True))



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()  # Create all tables if they don't exist

    # Check if the user already exists before adding
    if not User.query.filter_by(email='adishrafique@gmail.com').first():
        user1 = User(
            name='Adish Rafique',  # Add the name here
            email='adishrafique@gmail.com',
            password_hash=generate_password_hash('adishadish')
        )
        db.session.add(user1)
        db.session.commit()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


sample_rate = 16000
model_path = os.path.join(os.path.dirname(__file__), 'svm_model.pkl')
model = joblib.load(model_path)

vggish_path = r"C:/Users/adish/Desktop/final/vggish/1"
vggish = tf.saved_model.load(vggish_path)



def file_predict(file_path):
    try:
        waveform, sr = librosa.load(file_path, sr=16000)

        segment_length = 1.0
        num_segments = int(waveform.shape[0] / (sr * segment_length))
        features = []

        for i in range(num_segments):
            start = int(i * segment_length * sr)
            end = int(start + sr * segment_length)
            segment = waveform[start:end]
            vgg_features = vggish(segment).numpy()
            features.append(vgg_features)

        aggregated_features = np.mean(features, axis=0)
        input_features = aggregated_features.flatten()
        prediction = model.predict(input_features.reshape(1, -1))
        return prediction

    except Exception as e:
        print(f"Error during prediction: {e}")

def predict_genre(val):
    predicted_label = val[0]
    genre_mapping = {0: 'Pop',
                     1: 'Metal',
                     2: 'Disco',
                     3: 'Blues',
                     4: 'Reggae',
                     5: 'Classical',
                     6: 'Rock',
                     7: 'Hip Hop',
                     8: 'Country',
                     9: 'Jazz'
                     }
    return (genre_mapping[predicted_label])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    predicted_genre = None
    if request.method == 'POST':
        if 'filename' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filename']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.instance_path, 'uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

            genre = file_predict(filepath)
            predicted_genre = predict_genre(genre)

            if predicted_genre:
                search_history = SearchHistory(
                    user_id=current_user.id,
                    search_term=filename,
                    predicted_genre=predicted_genre
                )
                db.session.add(search_history)
                db.session.commit()

                return jsonify({'prediction': predicted_genre})  # Return the prediction as JSON

    else:
        return render_template('main.html', predicted_genre=predicted_genre)

@app.route('/login', methods = ['POST'])
def login_function():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):  # Check hashed password
        login_user(user)  # Log the user in
        return redirect(url_for('main'))
    else:
        flash("Incorrect email or password","error")
        return redirect('/')


@app.route('/history')
@login_required
def history():
    # Fetch history from the database for the current user
    history_objects = SearchHistory.query.filter_by(user_id=current_user.id).order_by(SearchHistory.timestamp.desc()).all()

    # Transform history_objects into a list of tuples
    history = [(item.search_term, item.predicted_genre, item.timestamp) for item in history_objects]

    return render_template('history.html', history=history)

@app.route('/about_us', methods=['GET', 'POST'])
@login_required
def about_us():
    return render_template('about_us.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template("account.html",
                           username=current_user.name,
                           email=current_user.email)

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(email=email).first():
        flash('Email address already exists.')
        return redirect(url_for('index'))

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash('Account created successfully! You can now log in.', "success")
    return redirect(url_for('index'))
