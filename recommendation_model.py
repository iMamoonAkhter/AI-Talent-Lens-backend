import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load dataset
df = pd.read_csv('student_dataset.csv')

# Features and target
X_raw = df[['Field']]
y_raw = df['Recommended_Learning_Mode']

# Encoding
field_encoder = LabelEncoder()
target_encoder = LabelEncoder()

X_encoded = field_encoder.fit_transform(X_raw['Field']).reshape(-1, 1)
y_encoded = target_encoder.fit_transform(y_raw)

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y_encoded, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediction function
def predict_roadmap(field_name):
    try:
        field_name = field_name.strip()
        encoded_input = field_encoder.transform([field_name]).reshape(-1, 1)
        prediction_idx = model.predict(encoded_input)
        roadmap = target_encoder.inverse_transform(prediction_idx)
        return roadmap[0]
    except ValueError:
        return f"Error: Field '{field_name}' not found in dataset."
