from flask import Flask, request, jsonify
import joblib, pandas as pd, math
from datetime import datetime, timezone

m = joblib.load("/model/cpu_forecast.joblib")
app = Flask(__name__)

@app.post("/predict")
def predict():
    print("Predicting CPU usage...")
    body = request.get_json(silent=True) or {}
    cpu_now = float(body.get("cpu_now", 0.5))
    ts = datetime.now(timezone.utc)
    features = pd.DataFrame({
        "minute_of_day":[ts.hour*60+ts.minute],
        "day":[ts.day],
        "cpu":[cpu_now]
    })
    forecast = float(m.predict(features)[0])
    replicas = max(1, math.ceil(forecast*10))
    return jsonify({
        "current_cpu": cpu_now,
        "predicted_cpu": round(forecast,3),
        "suggested_replicas": replicas
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)