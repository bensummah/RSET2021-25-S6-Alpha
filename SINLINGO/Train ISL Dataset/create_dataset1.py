import os
import cv2
import mediapipe as mp
import pickle
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)
mp_drawing = mp.solutions.drawing_utils  # Utility for drawing

# Function to detect hand landmarks and extract features
def detect_hand_landmarks(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found or cannot be read: {image_path}")
        return None
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    if results.multi_hand_landmarks:
        feature_vector = []
        for hand_landmarks in results.multi_hand_landmarks:
            landmark_list = []
            for lm in hand_landmarks.landmark:
                landmark_list.append([lm.x, lm.y, lm.z])
            feature_vector.extend(np.array(landmark_list).flatten())
        # Ensure the feature vector has a fixed size by padding with zeros if needed
        while len(feature_vector) < 63 * 2:  # 63 landmarks per hand, 2 hands
            feature_vector.extend([0] * 63)
        return np.array(feature_vector)
    else:
        return None

# Function to visualize hand landmarks for a specific image
def visualize_hand_landmarks(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found or cannot be read: {image_path}")
        return
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Hand Landmarks', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"No hand landmarks detected in {image_path}")

# Path to the dataset directory
dataset_dir = r'C:\Users\SAKHI dILIP\Anushri\ISL_dataset'

# Initialize lists to hold features and labels
features = []
labels = []

# Initialize counters for detected and not detected landmarks
detected_count = 0
not_detected_count = 0

# Assuming the directory structure is dataset_dir/class_x/filename.png
for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith('.jpg'):  # Change this if your images have a different extension
            image_path = os.path.join(root, file)
            print(f"Processing image: {image_path}")
            class_label = os.path.basename(root)  # Assuming the folder name is the class label
            feature_vector = detect_hand_landmarks(image_path)
            if feature_vector is not None:
                features.append(feature_vector)
                labels.append(class_label)
                detected_count += 1
                print(f"Hand landmarks detected in {image_path}")
            else:
                not_detected_count += 1
                print(f"No hand landmarks detected in {image_path}")

# Save the extracted features and labels to a pickle file
with open('data1.pickle', 'wb') as f:
    pickle.dump({'features': features, 'labels': labels}, f)

print("Features and labels saved to data1.pickle")

# Print the number of images where hand landmarks were detected and not detected
print(f"Number of images with hand landmarks detected: {detected_count}")
print(f"Number of images with no hand landmarks detected: {not_detected_count}")

# Optional: Visualize landmarks for specific images (example usage)
# visualize_hand_landmarks(r'C:\Users\SAKHI dILIP\Anushri\ISL_dataset1\class_x\example.png')
