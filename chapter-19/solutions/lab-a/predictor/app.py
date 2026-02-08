#!/usr/bin/env python3
"""Flask REST API that serves CPU-load predictions."""

import math
import os
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# Configuration (overridable via environment variables)
# ---------------------------------------------------------------------------
MIN_REPLICAS = int(os.environ.get("MIN_REPLICAS", "1"))
MAX_REPLICAS = int(os.environ.get("MAX_REPLICAS", "10"))
CPU_LOW = float(os.environ.get("CPU_LOW", "20"))    # CPU% at or below -> MIN_REPLICAS
CPU_HIGH = float(os.environ.get("CPU_HIGH", "80"))   # CPU% at or above -> MAX_REPLICAS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)
model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _synthetic_rolling_avg(hour: int, minute: int) -> float:
    """Approximate the rolling-average feature at inference time.

    During training the rolling_avg was a 10-minute backward-looking mean of
    the actual CPU series.  At inference we don't have a live series, so we
    reconstruct the expected base-curve value for the requested time.  This
    matches the sinusoidal pattern used by generate_data.py.
    """
    total_minutes = hour * 60 + minute
    phase_shift = 2 * math.pi * (240 / 1440)
    base = math.sin(2 * math.pi * total_minutes / 1440 - phase_shift)
    # Scale to [20, 80] — same BASE_LOW / BASE_HIGH as the generator
    return 50.0 + 30.0 * base


def _cpu_to_replicas(cpu: float) -> int:
    """Linearly map a predicted CPU% to a replica count."""
    if cpu <= CPU_LOW:
        return MIN_REPLICAS
    if cpu >= CPU_HIGH:
        return MAX_REPLICAS
    ratio = (cpu - CPU_LOW) / (CPU_HIGH - CPU_LOW)
    return max(MIN_REPLICAS, min(MAX_REPLICAS, round(
        MIN_REPLICAS + ratio * (MAX_REPLICAS - MIN_REPLICAS)
    )))


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict")
def predict():
    now = datetime.now(timezone.utc)

    hour = request.args.get("hour", default=now.hour, type=int)
    minute = request.args.get("minute", default=now.minute, type=int)
    day_of_week = now.weekday()

    rolling_avg = _synthetic_rolling_avg(hour, minute)

    features = pd.DataFrame([{
        "hour": hour,
        "minute": minute,
        "day_of_week": day_of_week,
        "rolling_avg": rolling_avg,
    }])

    predicted_cpu = float(model.predict(features)[0])
    predicted_cpu = max(0.0, min(100.0, round(predicted_cpu, 2)))

    replicas = _cpu_to_replicas(predicted_cpu)

    return jsonify({
        "predicted_cpu": predicted_cpu,
        "recommended_replicas": replicas,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


# ---------------------------------------------------------------------------
# Dev server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
