#!/bin/sh
set -e

# 1. Generate a synthetic CPU value (0.4 – 1.0)
CPU_NOW=$(awk -v min=$(date +%M) 'BEGIN{
  srand();
  v = 0.4 + 0.6 * sin(min/60 * 6.28318) + rand() * 0.1;
  if (v < 0) v = 0;
  print v;
}')
echo "Simulated CPU=$CPU_NOW"

# 2. Ask the AI model for a prediction
REPLICAS=$(wget -qO- \
  --header='Content-Type: application/json' \
  --post-data="{\"cpu_now\": $CPU_NOW}" \
  http://ai-autoscaler-api.aiops.svc.cluster.local:8080/predict |
  sed -n 's/.*"suggested_replicas":\
  \s*\([0-9]\+\).*/\1/p')

# Trim whitespace
REPLICAS=$(echo "$REPLICAS" | tr -d '[:space:]')

echo "AI suggests replicas=$REPLICAS"

# Validate REPLICAS is a number
if [ -z "$REPLICAS" ] || \
   ! echo "$REPLICAS" | grep -qE '^[0-9]+$'; then
  echo "ERROR: Invalid replicas value: '$REPLICAS'"
  exit 1
fi

# 3. Apply the scaling
kubectl -n aiops scale deployment demo-app \
  --replicas=$REPLICAS