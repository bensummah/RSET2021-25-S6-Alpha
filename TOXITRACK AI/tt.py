import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('path/to/your/serviceAccountKey.json')  # Replace with your credentials file path
firebase_admin.initialize_app(cred)

# Get an auth object
auth = auth.Client()

# Load Firebase configuration from JSON file
with open('firebaseConfig.json') as json_file:
    firebase_config = json.load(json_file)
firebase = pyrebase.initialize_app(firebase_config)