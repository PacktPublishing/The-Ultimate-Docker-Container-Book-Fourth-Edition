import math, os, random, time
from datetime import datetime, timezone

DAYS = int(os.getenv("DAYS", "7"))
STEP = int(os.getenv("STEP", "300"))  # 5 minutes
# Anchor end to UTC "now" unless END_TS is provided
end_ts = int(os.getenv("END_TS") or datetime.now(timezone.utc).timestamp())
# Align end to the step boundary and prevent future skew
end_ts = end_ts - (end_ts % STEP)
start_ts = end_ts - DAYS*24*3600

random.seed(7)

def traffic_rate(ts):
    t = datetime.fromtimestamp(ts, tz=timezone.utc)
    diurnal = 0.5 + 0.5*math.sin(2*math.pi*(t.hour*60+t.minute)/(24*60))
    lunch  = math.exp(-((t.hour + t.minute/60)-12)**2/1.2)
    dinner = math.exp(-((t.hour + t.minute/60)-19)**2/1.0)
    wknd = 0.7 if t.weekday() >= 5 else 1.0
    noise = 0.9 + 0.2*random.random()
    return max(0.2, 8.0*wknd*(0.4+0.6*diurnal) + 2*lunch + 2.5*dinner) * noise

def cpu_rate(ts, rps):
    t = datetime.fromtimestamp(ts, tz=timezone.utc)
    peak = 1.0 + 0.3*math.sin(2*math.pi*(t.hour*60+t.minute)/(24*60))
    noise = 0.95 + 0.1*random.random()
    return max(0.01, 0.05 + 0.01*rps*peak) * noise

def emit_counter(name, points):
    out = [f"# TYPE {name} counter"]
    for ts, val in points:
        out.append(f"{name} {val:.6f} {ts}")  # seconds
    return "\n".join(out)

orders, cpu = [], []
o_tot = c_tot = 0.0
for ts in range(start_ts, end_ts+1, STEP):
    rps = traffic_rate(ts)
    o_tot += rps * STEP
    c_tot += cpu_rate(ts, rps) * STEP
    orders.append((ts, o_tot))
    cpu.append((ts, c_tot))

with open("sample.om", "w", newline="\n") as f:
    f.write(emit_counter("orders_requests_total", orders))
    f.write("\n")  # exactly one newline between series
    f.write(emit_counter("container_cpu_usage_seconds_total", cpu))
    f.write("\n# EOF\n")

def fmt(ts): return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
print(f"Wrote sample.om with {len(orders)} points per series")
print(f"First ts: {orders[0][0]} -> {fmt(orders[0][0])}")
print(f" Last ts: {orders[-1][0]} -> {fmt(orders[-1][0])}")