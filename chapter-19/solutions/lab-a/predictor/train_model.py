#!/usr/bin/env python3
"""Train a RandomForestRegressor on the synthetic CPU-load data."""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "data", "cpu_load.csv")
MODEL_FILE = os.path.join(BASE_DIR, "model.pkl")

# ---------------------------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------------------------

ROLLING_WINDOW = 10  # minutes


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract time-based features and a rolling average from raw data."""
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["minute"] = df["timestamp"].dt.minute
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    # Rolling window average (backward-looking)
    df["rolling_avg"] = (
        df["cpu_percent"]
        .rolling(window=ROLLING_WINDOW, min_periods=1)
        .mean()
    )

    return df


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def main():
    # --- Load data ---
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: {DATA_FILE} not found. Run generate_data.py first.")
        raise SystemExit(1)

    df = pd.read_csv(DATA_FILE)
    print(f"Loaded {len(df)} rows from {DATA_FILE}")

    # --- Features ---
    df = build_features(df)

    feature_cols = ["hour", "minute", "day_of_week", "rolling_avg"]
    X = df[feature_cols]
    y = df["cpu_percent"]

    # --- Train / test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- Train ---
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # --- Evaluate ---
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nEvaluation on test set ({len(X_test)} samples):")
    print(f"  MAE  = {mae:.2f}")
    print(f"  R²   = {r2:.4f}")

    # --- Feature importance ---
    print("\nFeature importances:")
    for name, imp in zip(feature_cols, model.feature_importances_):
        print(f"  {name:15s} {imp:.4f}")

    # --- Save ---
    joblib.dump(model, MODEL_FILE)
    print(f"\nModel saved -> {MODEL_FILE}")


if __name__ == "__main__":
    main()
