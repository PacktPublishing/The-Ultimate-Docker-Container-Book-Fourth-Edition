#!/usr/bin/env python3
import math, csv, time, random, datetime as dt
from datetime import timedelta

# three days of 5-min samples
start = dt.datetime.now(dt.timezone.utc) - timedelta(days=3)
step = timedelta(minutes=5)
rows = []

for i in range(int(3*24*60/5)):
    ts = start + i*step
    minute_of_day = ts.hour*60 + ts.minute
    # sinusoid pattern (0.2–1.0) + small noise
    base = 0.6 + 0.4*math.sin(2*math.pi*minute_of_day/(24*60))
    noise = 0.9 + 0.2*random.random()
    cpu = round(base*noise, 3)
    rows.append([ts.isoformat(), cpu])

with open("cpu_metrics.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp","cpu"])
    w.writerows(rows)

print(f"Generated {len(rows)} samples to cpu_metrics.csv")