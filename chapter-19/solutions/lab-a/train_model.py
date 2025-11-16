import pandas as pd, numpy as np, joblib
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

df = pd.read_csv("cpu_metrics.csv", parse_dates=["timestamp"])
df["minute_of_day"] = df["timestamp"].dt.hour*60 + df["timestamp"].dt.minute
df["day"] = df["timestamp"].dt.day
df["cpu_next"] = df["cpu"].shift(-6)  # 30 min ahead (6 × 5 min)

train = df.dropna()
X = train[["minute_of_day","day","cpu"]]
y = train["cpu_next"]

model = RandomForestRegressor(n_estimators=80, random_state=7)
model.fit(X,y)
joblib.dump(model,"cpu_forecast.joblib")
print("Model trained and saved to cpu_forecast.joblib")