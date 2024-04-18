from flask import Flask, jsonify, request
import torch
import numpy as np
from lstmarch import LSTMModel
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)

# Load your Model
try:
    model = LSTMModel(
        input_size=7, hidden_size=64, num_layers=1, output_size=3, dropout_rate=0.3
    )
    model.load_state_dict(torch.load("model/finalmodel.pth"))
    model.eval()
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    app.logger.error(f"Error loading the model or scaler: {str(e)}")
    raise RuntimeError(f"Model or scaler could not be loaded: {str(e)}")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        input_features = np.array(data["features"])
        scaled_features = scaler.transform(input_features.reshape(1, -1))
        input_tensor = torch.tensor(scaled_features, dtype=torch.float32)

        with torch.no_grad():
            prediction = model(input_tensor)

        return jsonify({"prediction": prediction.numpy().tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
