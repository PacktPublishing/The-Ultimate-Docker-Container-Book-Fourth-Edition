#!/usr/bin/env python3
"""Generate synthetic CPU-load data that mimics a 24-hour day/night cycle."""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NUM_MINUTES = 1440          # 24 hours × 60 minutes
BASE_LOW = 20.0             # minimum CPU % (night-time trough)
BASE_HIGH = 80.0            # maximum CPU % (afternoon peak)
NOISE_STD = 4.0             # standard deviation of Gaussian noise
SPIKE_PROBABILITY = 0.02    # chance of a burst spike per minute
SPIKE_AMPLITUDE_MIN = 10.0  # extra CPU % added by a spike (lower bound)
SPIKE_AMPLITUDE_MAX = 25.0  # extra CPU % added by a spike (upper bound)
SEED = 42                   # reproducible randomness

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cpu_load.csv")

# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_cpu_data() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    start = datetime(2025, 6, 1, 0, 0, 0)
    timestamps = [start + timedelta(minutes=m) for m in range(NUM_MINUTES)]

    # Sinusoidal base: trough at ~04:00, peak at ~14:00
    # sin reaches -1 at 04:00 (minute 240) and +1 at 16:00 (minute 960)
    minutes = np.arange(NUM_MINUTES, dtype=float)
    phase_shift = 2 * np.pi * (240 / NUM_MINUTES)  # shift so minimum is at 04:00
    base = np.sin(2 * np.pi * minutes / NUM_MINUTES - phase_shift)

    # Scale from [-1, 1] to [BASE_LOW, BASE_HIGH]
    amplitude = (BASE_HIGH - BASE_LOW) / 2
    midpoint = (BASE_HIGH + BASE_LOW) / 2
    cpu = midpoint + amplitude * base

    # Gaussian noise
    noise = rng.normal(0, NOISE_STD, size=NUM_MINUTES)
    cpu += noise

    # Random burst spikes
    spike_mask = rng.random(NUM_MINUTES) < SPIKE_PROBABILITY
    spike_values = rng.uniform(SPIKE_AMPLITUDE_MIN, SPIKE_AMPLITUDE_MAX, size=NUM_MINUTES)
    cpu += spike_mask * spike_values

    # Clamp to [0, 100]
    cpu = np.clip(cpu, 0.0, 100.0)

    return pd.DataFrame({
        "timestamp": timestamps,
        "cpu_percent": np.round(cpu, 2),
    })


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = generate_cpu_data()
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Generated {len(df)} data points -> {OUTPUT_FILE}")
    print(f"  cpu_percent  min={df['cpu_percent'].min():.2f}  "
          f"max={df['cpu_percent'].max():.2f}  "
          f"mean={df['cpu_percent'].mean():.2f}")


if __name__ == "__main__":
    main()
