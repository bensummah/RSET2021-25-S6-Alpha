from flask import Flask, render_template, request, jsonify
from urllib.parse import unquote
import requests

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    x= unquote(userText)
    # Analyze emotion from the user's message
    detected_emotion = analyze_emotion(x)
    # Increment the count for the detected emotion
    #if detected_emotion in emotion_counts:
    #    emotion_counts[detected_emotion] += 1
    print("\n",x,"\n")
    print("Detected Emotion:", detected_emotion)
    response= chatbot_response(userText)
    return jsonify(response)

@app.route("/get_emotion_counts", methods=["GET"])
def get_emotion_counts():
    global emotion_counts, emotion_order_index

    # Find the maximum count among all emotions
    max_count = max(emotion_counts.values())
    # Get all emotions that have the maximum count
    predominant_emotions = [emotion for emotion, count in emotion_counts.items() if count == max_count]
     # Choose the emotion with the highest order index if there are ties in counts

    if len(predominant_emotions) > 1:
        predominant_emotions = sorted(predominant_emotions, key=lambda e: emotion_order_index[e], reverse=True)
    latest_emotion = predominant_emotions[0]  # Choose the first emotion with the highest order index

    print("Current Emotion Counts:", emotion_counts)
    print("Predominant Emotion(s):", predominant_emotions)
    # Search for recommended tracks based on the predominant emotion
    recommended_tracks = search_tracks_by_emotion(latest_emotion)

    return jsonify({"emotion": latest_emotion, "tracks": recommended_tracks})

# Function to search for tracks by tag (emotion)
def search_tracks_by_emotion(emotion):
    params = {
        'method': 'tag.gettoptracks',
        'tag': emotion,
        'api_key': api_key,
        'format': 'json',
        'limit': 100  # Limiting to 100 tracks for simplicity
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    # Check if the request was successful
    if 'tracks' in data:
        tracks = data['tracks']['track']
        track_list = []
        for track in tracks:
            track_dict = {
                'name': track['name'],
                'artist': track['artist']['name'],
                'url': track['url']
            }
            track_list.append(track_dict)
        
        # Select 7 random items from track_list
        random_tracks = random.sample(track_list, 7)
        
        return random_tracks
    else:
        return None

@app.route("/search_tracks", methods=["GET"])
def search_tracks():
    emotion = request.args.get('emotion')
    if emotion:
        tracks = search_tracks_by_emotion(emotion)
        #sent back from web server to client application using jsonify
        return jsonify(tracks)
    else:
        return jsonify([])  # Return empty list if no emotion is specified

if __name__ == "__main__":
    app.run() #to run the flask app