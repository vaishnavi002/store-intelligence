import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


MODEL_PATH = "app/model.pkl"


def train_dummy_model():
    """
    Train a simple model (only runs once if model not found)
    """

    # Features:
    # [entry_count, zone_visits, billing_visits]

    X = np.array([
        [1, 0, 0],
        [2, 1, 0],
        [3, 2, 1],
        [4, 3, 1],
        [5, 4, 2],
        [6, 5, 3],
    ])

    y = np.array([0, 0, 0, 1, 1, 1])  # conversion yes/no

    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_dummy_model()


model = load_model()


def predict_conversion(entry, zone, billing):
    """
    Returns probability of conversion
    """

    features = np.array([[entry, zone, billing]])

    prob = model.predict_proba(features)[0][1]

    return round(float(prob), 3)