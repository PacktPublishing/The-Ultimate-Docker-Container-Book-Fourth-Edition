# Lab A — Building an AI-Driven Autoscaler with Synthetic Metrics

**Chapter 19 · AI-Assisted Operations · The Ultimate Docker Container Book**

In this lab you build a complete AI-driven autoscaler from scratch. Instead of
connecting to an existing monitoring system you generate synthetic CPU-load data
that imitates a typical day-and-night workload, train a small machine-learning
model to predict upcoming load, and let that model automatically scale a
Kubernetes Deployment.

The core workflow is **observe &rarr; learn &rarr; act**: observe system
behaviour, learn a predictive pattern, and act by adjusting capacity. In a
production environment the synthetic data would be replaced by real time-series
metrics from Prometheus or a similar backend. Everything here runs locally on a
`kind` (Kubernetes-in-Docker) cluster.

## What You Will Learn

1. How to create synthetic operational data in Python.
2. How to train a time-series forecasting model with scikit-learn.
3. How to expose that model as a REST API with Flask.
4. How to build a simple Kubernetes controller (a CronJob) that queries the
   model and scales a Deployment.

## Prerequisites

| Tool | Purpose |
|------|---------|
| **Docker** | Build container images, run the kind cluster |
| **kind** | Local Kubernetes cluster (runs inside Docker) |
| **kubectl** | Interact with the cluster |
| **Python 3.10+** | Generate data and train the model (offline steps) |
| **pip packages**: `numpy`, `pandas`, `scikit-learn`, `joblib` | Used by the data generator and trainer |

Install the Python packages for the offline steps:

```bash
pip install numpy pandas scikit-learn joblib
```

## Architecture

```
+---------------------+       +---------------------+       +--------------------+
|  Synthetic Data     |       |  ML Predictor       |       |  Autoscaler        |
|  Generator          | ----> |  Service (Flask)     | <---- |  CronJob           |
|  (Python script)    |       |  /predict endpoint   |       |  (shell script)    |
+---------------------+       +---------------------+       +--------------------+
         |                             |                              |
         | generates CSV /             | runs as a Pod                | scales
         | trains model                | in the cluster               | target
         v                             v                              v
   model.pkl                   Predictor Deployment           sample-app Deployment
                               + Service (ClusterIP)          (nginx)
```

Three components work together:

- **predictor/** — A Python Flask API that loads a pre-trained
  `RandomForestRegressor` and returns predicted CPU load plus a recommended
  replica count. Served by Gunicorn on port 8080.
- **autoscaler/** — A Kubernetes CronJob (every 2 minutes) that runs a Bash
  script. The script curls the predictor, parses the recommended replica count
  with `jq`, and runs `kubectl scale` on the target Deployment.
- **sample-app/** — A plain `nginx:alpine` Deployment that represents the
  workload being scaled up and down.

## Project Structure

```
lab-a-v2/
├── kind-config.yaml              # kind cluster — single control-plane node
├── sample-app/
│   └── deployment.yaml           # nginx Deployment + ClusterIP Service
├── predictor/
│   ├── generate_data.py          # synthetic 24h CPU-load generator
│   ├── train_model.py            # model training (RandomForestRegressor)
│   ├── app.py                    # Flask REST API  (/predict, /health)
│   ├── model.pkl                 # trained model (generated, ~7 MB)
│   ├── data/cpu_load.csv         # synthetic dataset (generated)
│   ├── requirements.txt          # Python dependencies for the container
│   ├── Dockerfile                # python:3.12-slim + gunicorn
│   └── deployment.yaml           # K8s Deployment + ClusterIP Service
├── autoscaler/
│   ├── scale.sh                  # scaling logic (curl + jq + kubectl)
│   ├── Dockerfile                # bitnami/kubectl + scale.sh
│   ├── rbac.yaml                 # ServiceAccount + Role + RoleBinding
│   └── cronjob.yaml              # CronJob (*/2 * * * *)
└── scripts/
    ├── setup-cluster.sh          # create cluster, build & load images
    ├── deploy-all.sh             # apply all manifests, wait for rollouts
    ├── demo.sh                   # query predictor for 24h, show scaling table
    └── teardown.sh               # delete the kind cluster
```

## Quick Start

The lab provides helper scripts that automate the full lifecycle.

### Step 1 — Generate Data and Train the Model

```bash
# Generate 1 440 synthetic data points (one per minute, 24 hours)
python predictor/generate_data.py

# Train the model on the synthetic data
python predictor/train_model.py
```

You should see output similar to:

```
Generated 1440 data points -> predictor/data/cpu_load.csv
  cpu_percent  min=8.93  max=96.17  mean=50.13

Loaded 1440 rows
Evaluation on test set (288 samples):
  MAE  = 3.75
  R^2  = 0.9482
Model saved -> predictor/model.pkl
```

### Step 2 — Create the Cluster and Build Images

```bash
bash scripts/setup-cluster.sh
```

This script:
1. Checks that `docker`, `kind`, and `kubectl` are installed.
2. Creates a single-node kind cluster named `lab-a`.
3. Builds the `predictor:1.0` and `autoscaler:1.0` Docker images.
4. Loads both images into the kind cluster.

### Step 3 — Deploy Everything

```bash
bash scripts/deploy-all.sh
```

This applies all Kubernetes manifests in order, waits for the Deployments to
become ready, and prints a summary of all resources.

### Step 4 — Observe the Autoscaler

```bash
# See predicted load and recommended replicas for every hour of the day
bash scripts/demo.sh
```

Example output:

```
  Hour     Predicted CPU   Replicas    Visual
  -------  --------------  ----------  --------------------
  00:00      25.7%         2         #####
  03:00      44.2%         5         ########
  09:00      78.0%         10        ###############
  14:00      66.8%         8         #############
  21:00      16.5%         1         ###
```

You can also watch scaling happen in real time:

```bash
# Watch the sample-app replica count update as the CronJob fires
kubectl get deployment sample-app -w
```

Or inspect the CronJob logs after it runs:

```bash
kubectl get jobs
kubectl logs job/<job-name>
```

### Step 5 — Tear Down

```bash
bash scripts/teardown.sh
```

## Step-by-Step Walkthrough (Manual)

If you prefer to run each command yourself rather than using the helper scripts:

```bash
# 1. Generate data and train model
python predictor/generate_data.py
python predictor/train_model.py

# 2. Build Docker images
docker build -t predictor:1.0  ./predictor
docker build -t autoscaler:1.0 ./autoscaler

# 3. Create kind cluster
kind create cluster --config kind-config.yaml --name lab-a

# 4. Load images into the cluster
kind load docker-image predictor:1.0  --name lab-a
kind load docker-image autoscaler:1.0 --name lab-a

# 5. Deploy workloads
kubectl apply -f sample-app/deployment.yaml
kubectl apply -f predictor/deployment.yaml
kubectl rollout status deployment/predictor --timeout=120s
kubectl rollout status deployment/sample-app --timeout=120s

# 6. Deploy autoscaler
kubectl apply -f autoscaler/rbac.yaml
kubectl apply -f autoscaler/cronjob.yaml

# 7. Verify
kubectl get deployments,services,cronjobs

# 8. Watch scaling (the CronJob fires every 2 minutes)
kubectl get deployment sample-app -w

# 9. Clean up
kind delete cluster --name lab-a
```

## How It Works

### Synthetic Data Generation

`predictor/generate_data.py` creates 1 440 data points (one per minute for 24
hours). The CPU load follows a sinusoidal curve with a trough around 20% at
night and a peak around 80% in the afternoon. Gaussian noise and random burst
spikes are added for realism. The output is written to
`predictor/data/cpu_load.csv`.

### Model Training

`predictor/train_model.py` reads the CSV and engineers four features:

| Feature | Description |
|---------|-------------|
| `hour` | Hour of the day (0-23) |
| `minute` | Minute of the hour (0-59) |
| `day_of_week` | Day of the week (0=Monday) |
| `rolling_avg` | 10-minute backward-looking rolling average of CPU load |

A `RandomForestRegressor` (100 trees, max depth 12) is trained on an 80/20
split. The model achieves an MAE of ~3.75 percentage points and an R^2 of
~0.95. It is serialized to `predictor/model.pkl` with `joblib`.

### Predictor API

`predictor/app.py` is a Flask application that loads the trained model at
startup and exposes two endpoints:

- `GET /health` — returns `{"status": "ok"}` (used as liveness/readiness probe).
- `GET /predict?hour=HH&minute=MM` — returns a JSON object:

```json
{
  "predicted_cpu": 62.3,
  "recommended_replicas": 7,
  "timestamp": "2025-06-01T14:30:00Z"
}
```

The `hour` and `minute` parameters are optional and default to the current UTC
time. The predicted CPU percentage is linearly mapped to a replica count between
`MIN_REPLICAS` (default 1) and `MAX_REPLICAS` (default 10).

### Autoscaler CronJob

Every two minutes the CronJob runs `autoscaler/scale.sh` inside a container
that has `kubectl`, `curl`, and `jq`. The script:

1. Queries the predictor service at
   `http://predictor.default.svc.cluster.local/predict`.
2. Parses `recommended_replicas` from the JSON response.
3. Compares it with the current replica count of the `sample-app` Deployment.
4. Runs `kubectl scale` only if the count differs.

The autoscaler uses a dedicated ServiceAccount (`autoscaler-sa`) with a Role
that grants only `get`, `list`, `patch`, and `update` on Deployments — no
delete, no access to Secrets.

## Configuration

### Predictor Environment Variables

Set these on the predictor Deployment to tune the replica mapping:

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_REPLICAS` | `1` | Minimum replica count |
| `MAX_REPLICAS` | `10` | Maximum replica count |
| `CPU_LOW` | `20` | CPU% at or below which MIN_REPLICAS is returned |
| `CPU_HIGH` | `80` | CPU% at or above which MAX_REPLICAS is returned |

### Autoscaler Environment Variables

Set these on the CronJob container to override defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `PREDICTOR_URL` | `http://predictor.default.svc.cluster.local/predict` | URL of the predictor API |
| `TARGET_DEPLOYMENT` | `sample-app` | Deployment to scale |
| `TARGET_NAMESPACE` | `default` | Namespace of the target Deployment |
| `CURL_TIMEOUT` | `10` | HTTP request timeout in seconds |

## Experimenting

Once the lab is running, try these modifications to observe different scaling
behaviour:

- **Change the data pattern** — Edit the constants in `generate_data.py`
  (`BASE_LOW`, `BASE_HIGH`, `NOISE_STD`, `SPIKE_PROBABILITY`) and re-run the
  data generation and training steps. Rebuild the predictor image and redeploy.
- **Adjust the replica mapping** — Change `CPU_LOW`, `CPU_HIGH`,
  `MIN_REPLICAS`, or `MAX_REPLICAS` in `predictor/deployment.yaml` and
  re-apply.
- **Use a different model** — Swap `RandomForestRegressor` in `train_model.py`
  for `GradientBoostingRegressor` or even a simple `LinearRegression` and
  compare the accuracy.
- **Change the CronJob schedule** — Edit the `schedule` field in
  `autoscaler/cronjob.yaml` (e.g. `*/1 * * * *` for every minute).

## From Lab to Production

In a real environment the synthetic data in this lab would be replaced by actual
time-series metrics:

| Lab Component | Production Equivalent |
|---------------|----------------------|
| `generate_data.py` | Prometheus, Datadog, or CloudWatch metrics |
| `train_model.py` | Scheduled retraining pipeline (Airflow, Kubeflow) |
| `model.pkl` baked into the image | Model registry (MLflow, S3) |
| CronJob polling | Custom controller or event-driven trigger |
| `kubectl scale` | Kubernetes client library (client-go, kubernetes Python client) |

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Languages | Python 3.12, Bash |
| ML library | scikit-learn (RandomForestRegressor) |
| API framework | Flask + Gunicorn |
| Model serialization | joblib |
| Container runtime | Docker |
| Orchestrator | Kubernetes via kind |
| Autoscaler controller | CronJob + kubectl + curl + jq |
| Data format | CSV (synthetic data), JSON (API) |
