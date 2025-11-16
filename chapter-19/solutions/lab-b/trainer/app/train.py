import math, random, joblib, pandas as pd
from datetime import datetime, timezone, timedelta
from sklearn.ensemble import RandomForestRegressor

now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
start = now - timedelta(hours=24)

ts, cpu = [], []
t = start
while t <= now:
    m = t.hour*60 + t.minute
    base = 0.6 + 0.4*math.sin(2*math.pi*m/(24*60))
    val = max(0.05, base*(0.9 + 0.2*random.random()))
    ts.append(t); cpu.append(val); t += timedelta(minutes=5)

df = pd.DataFrame({"ts": ts, "cpu": cpu})
df["minute_of_day"] = df["ts"].dt.hour*60 + df["ts"].dt.minute
df["cpu_next"] = df["cpu"].shift(-6)

train = df.dropna()
X = train[["minute_of_day","cpu"]]
y = train["cpu_next"]

m = RandomForestRegressor(n_estimators=80, random_state=7).fit(X, y)
joblib.dump(m, "/tmp/cpu_forecast.joblib")
print("Saved /tmp/cpu_forecast.joblib")