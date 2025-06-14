# model_handler.py

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from utils.extract_features_from_one_url import extract_features_from_url
from utils.load_data import load_data
from sklearn.model_selection import train_test_split
from utils.find_path import get_data_path, get_model_path

# Masquer les logs TensorFlow et forcer le CPU
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Masque les logs TF # 0 = tous logs, 1 = warnings, 2 = erreurs, 3 = rien
os.environ['CUDA_VISIBLE_DEVICES'] = ''   # Force le CPU
tf.config.set_visible_devices([], 'GPU')  # Évite les erreurs GPU

# Chemin vers le fichier de modèle
MODEL_PATH = get_model_path()

def get_model():
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
         # Important : recompiler pour activer les métriques
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model

    X, y = load_data(get_data_path("features_phishing_dataset.csv"))
    X_train, X_, y_train, y_ = train_test_split(X, y, test_size=0.40, random_state=1)
    X_cv, X_test, y_cv, y_test = train_test_split(X_, y_, test_size=0.50, random_state=1)
    del X_, y_

    model = Sequential([
        Input(shape=(13,)),              
        Dense(25, activation='relu'),
        Dense(15, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
            optimizer='adam',                     # ou tf.keras.optimizers.Adam(learning_rate=0.001)
            loss='binary_crossentropy',          # car on fait de la classification binaire (Phishing vs Legitimate)
            metrics=['accuracy']                 # pour voir la précision lors de l’évaluation
    )

    model.fit(X_train, y_train, validation_data=(X_cv, y_cv), epochs=30, batch_size=32, verbose=0)
    model.save(MODEL_PATH)
    return model

# Fonction de prédiction utilisée par Flask
def predict_url(model, url):
    features = np.array(extract_features_from_url(url)).reshape(1, -1)
    prediction = model.predict(features, verbose=0)[0][0]
    return "Phishing" if prediction >= 0.5 else "Legitimate"
