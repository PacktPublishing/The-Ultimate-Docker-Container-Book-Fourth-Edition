#!/bin/bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PREDICTOR_URL="${PREDICTOR_URL:-http://predictor.default.svc.cluster.local/predict}"
DEPLOYMENT="${TARGET_DEPLOYMENT:-sample-app}"
NAMESPACE="${TARGET_NAMESPACE:-default}"
CURL_TIMEOUT="${CURL_TIMEOUT:-10}"

echo "========================================"
echo "Autoscaler run: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "========================================"

# ---------------------------------------------------------------------------
# 1. Query the predictor
# ---------------------------------------------------------------------------
echo "Querying predictor at ${PREDICTOR_URL} ..."

if ! RESPONSE=$(curl -s --fail --max-time "${CURL_TIMEOUT}" "${PREDICTOR_URL}"); then
    echo "ERROR: Failed to reach predictor service."
    exit 1
fi

echo "Response: ${RESPONSE}"

# ---------------------------------------------------------------------------
# 2. Parse recommended replicas
# ---------------------------------------------------------------------------
if ! RECOMMENDED=$(echo "${RESPONSE}" | jq -r '.recommended_replicas'); then
    echo "ERROR: Failed to parse recommended_replicas from response."
    exit 1
fi

if [ -z "${RECOMMENDED}" ] || [ "${RECOMMENDED}" = "null" ]; then
    echo "ERROR: recommended_replicas is empty or null."
    exit 1
fi

PREDICTED_CPU=$(echo "${RESPONSE}" | jq -r '.predicted_cpu')
echo "Predicted CPU: ${PREDICTED_CPU}%  ->  Recommended replicas: ${RECOMMENDED}"

# ---------------------------------------------------------------------------
# 3. Get current replica count
# ---------------------------------------------------------------------------
CURRENT=$(kubectl get deployment "${DEPLOYMENT}" \
    -n "${NAMESPACE}" \
    -o jsonpath='{.spec.replicas}')

echo "Current replicas: ${CURRENT}"

# ---------------------------------------------------------------------------
# 4. Scale if needed
# ---------------------------------------------------------------------------
if [ "${CURRENT}" -eq "${RECOMMENDED}" ]; then
    echo "No scaling needed — already at ${CURRENT} replicas."
else
    echo "Scaling ${DEPLOYMENT} from ${CURRENT} to ${RECOMMENDED} replicas ..."
    kubectl scale deployment "${DEPLOYMENT}" \
        -n "${NAMESPACE}" \
        --replicas="${RECOMMENDED}"
    echo "Scaling complete."
fi

echo "Done."
