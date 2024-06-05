import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load data from the pickle file
pickle_file_path = './data1.pickle'

with open(pickle_file_path, 'rb') as f:
    data_dict = pickle.load(f)

# Extract features and labels
features = data_dict['features']
labels = data_dict['labels']

# Convert to numpy arrays
features = np.array(features)
labels = np.array(labels)

# Normalize the feature vectors
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, shuffle=True, stratify=labels, random_state=42)

# Define SVM model and parameter grid for GridSearchCV
svc = SVC(probability=True, random_state=42)
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto'],
    'kernel': ['rbf', 'poly']
}

# Perform GridSearchCV to find the best hyperparameters
grid_search = GridSearchCV(svc, param_grid, cv=5, n_jobs=-1)
grid_search.fit(x_train, y_train)

# Best estimator from the grid search
best_svc = grid_search.best_estimator_

# Evaluate the best model
y_predict = best_svc.predict(x_test)
score = accuracy_score(y_predict, y_test)
print(f'{score * 100:.2f}% of samples were classified correctly!')

# Save the trained model
with open('model1.p', 'wb') as f:
    pickle.dump({'model': best_svc, 'scaler': scaler}, f)

print("Model and scaler saved to 'model1.p' successfully.")
