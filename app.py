from flask import Flask, jsonify, send_from_directory
import torch
import numpy as np
from lstmarch import LSTMModel
import joblib
import os
from dotenv import load_dotenv
import mysql.connector

app = Flask(__name__, static_url_path="", static_folder="static")

# Load LSTM Model
try:
    model = LSTMModel(
        input_size=7, hidden_size=64, num_layers=1, output_size=3, dropout_rate=0
    )
    model.load_state_dict(torch.load("model/finalmodel.pth"))
    model.eval()
    scaler = joblib.load("model/scaler.pkl")
except Exception as e:
    app.logger.error(f"Error loading the model or scaler: {str(e)}")
    raise RuntimeError(f"Model or scaler could not be loaded: {str(e)}")


# Database Connection Setup
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="floodsight"
)
cursor = db.cursor()

# Load in APIKEY from .env
load_dotenv(dotenv_path=".env")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Retrieve last 14 days of data from the database
        cursor.execute(
            "SELECT dew_point, max_temp, min_temp, max_wind_speed, precipitation, avg_temp, wind_speed FROM weather_data ORDER BY date DESC LIMIT 14"
        )
        result = cursor.fetchall()

        # Transform result into numpy array for scaling
        feature_array = np.array(result, dtype=float)

        # Scale and Predict
        scaled_features = scaler.transform(feature_array)
        input_tensor = torch.tensor(scaled_features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            prediction = model(input_tensor)

        return jsonify({"prediction": np.abs(prediction.numpy()).tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    app.run(debug=True, port=6969)
