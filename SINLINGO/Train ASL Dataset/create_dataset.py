import os
import cv2
import mediapipe as mp
import pickle
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)

# Function to detect hand landmarks and extract features
def detect_hand_landmarks(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found: {image_path}")
        return None
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmark_list = []
            for lm in hand_landmarks.landmark:
                landmark_list.append([lm.x, lm.y, lm.z])
            return np.array(landmark_list).flatten()
    else:
        return None

# Path to the dataset directory
dataset_dir = './ASL_dataset1'

# Initialize lists to hold features and labels
features = []
labels = []

# Initialize counters for detected and not detected landmarks
detected_count = 0
not_detected_count = 0

# Assuming the directory structure is dataset_dir/class_x/filename.png
for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith('.png'):  # Change this if your images have a different extension
            image_path = os.path.join(root, file)
            class_label = os.path.basename(root)  # Assuming the folder name is the class label
            feature_vector = detect_hand_landmarks(image_path)
            if feature_vector is not None:
                features.append(feature_vector)
                labels.append(class_label)
                detected_count += 1
            else:
                not_detected_count += 1

# Save the extracted features and labels to a pickle file
with open('data.pickle', 'wb') as f:
    pickle.dump({'features': features, 'labels': labels}, f)

print("Features and labels saved to data.pickle")

# Print the number of images where hand landmarks were detected and not detected
print(f"Number of images with hand landmarks detected: {detected_count}")
print(f"Number of images with no hand landmarks detected: {not_detected_count}")
