from flask import Flask, jsonify, request
import torch
import numpy as np
from lstmarch import LSTMModel
from sklearn.preprocessing import StandardScaler
from api.openweather import get_weather_data, format_weather_json
import joblib
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load LSTM Model
try:
    model = LSTMModel(
        input_size=7, hidden_size=64, num_layers=1, output_size=3, dropout_rate=0.3
    )
    model.load_state_dict(torch.load("model/finalmodel.pth"))
    model.eval()
    scaler = joblib.load("model/scaler.pkl")
except Exception as e:
    app.logger.error(f"Error loading the model or scaler: {str(e)}")
    raise RuntimeError(f"Model or scaler could not be loaded: {str(e)}")


# Load in APIKEY from .env
load_dotenv(dotenv_path=".env")
api_key = os.getenv("APIKEY")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Transform JSON response from Openweather API into its individual feature values
        weather_data = get_weather_data(api_key)
        input_features = format_weather_json(weather_data)
        feature_array = np.array([list(input_features.values())])

        # Scale and Predict
        scaled_features = scaler.transform(feature_array)
        input_tensor = torch.tensor(scaled_features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            prediction = model(input_tensor)

        return jsonify({"prediction": prediction.numpy().tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=6969)
