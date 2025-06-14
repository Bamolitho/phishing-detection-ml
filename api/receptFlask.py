# receptFlask.py
from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #  Ça permet à Python de comprendre que model/ est dans le dossier parent.
from model.model_handler import get_model, predict_url


app = Flask(__name__)
model = get_model()  # Chargement une seule fois

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Aucune URL fournie"}), 400

    url = data["url"]
    verdict = predict_url(model, url)
    return jsonify({"verdict": verdict}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
