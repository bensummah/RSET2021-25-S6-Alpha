import pickle
import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Load the trained model and scaler
with open('model1.p', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    scaler = model_data['scaler']

# Function to extract hand landmarks from an image
def extract_hand_landmarks(image):
    data_aux = []

    # Convert image from BGR to RGB
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect hand landmarks
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7) as hands:
        results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                data_aux.append(landmark.x)
                data_aux.append(landmark.y)
                data_aux.append(landmark.z)  # Add the z-coordinate
            # Draw hand landmarks on the image for debugging
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        return None

    # Ensure data_aux has a fixed length for both hands (2 hands * 21 landmarks * 3 coordinates)
    required_length = 2 * 21 * 3
    if len(data_aux) < required_length:
        data_aux.extend([0] * (required_length - len(data_aux)))
    elif len(data_aux) > required_length:
        data_aux = data_aux[:required_length]
    
    return np.array(data_aux).reshape(1, -1)

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Extract hand landmarks
    landmarks = extract_hand_landmarks(frame)
    if landmarks is not None:
        # Normalize the landmarks using the scaler
        landmarks = scaler.transform(landmarks)

        # Predict the label using the trained model
        prediction = model.predict(landmarks)
        label = prediction[0]

        # Display the prediction on the frame
        cv2.putText(frame, f'Prediction: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('ASL Prediction', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
