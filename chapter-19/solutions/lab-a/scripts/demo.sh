#!/bin/bash
set -euo pipefail

LOCAL_PORT="${LOCAL_PORT:-9091}"
PF_PID=""

# -------------------------------------------------------------------
# Cleanup on exit
# -------------------------------------------------------------------
cleanup() {
    if [ -n "$PF_PID" ] && kill -0 "$PF_PID" 2>/dev/null; then
        echo ""
        echo "Stopping port-forward (PID $PF_PID) ..."
        kill "$PF_PID" 2>/dev/null || true
        wait "$PF_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

echo "============================================"
echo "  Lab A — Demo"
echo "============================================"

# -------------------------------------------------------------------
# 1. Port-forward predictor service
# -------------------------------------------------------------------
echo ""
echo "Starting port-forward to predictor service on localhost:${LOCAL_PORT} ..."
kubectl port-forward svc/predictor "${LOCAL_PORT}:80" &>/dev/null &
PF_PID=$!
sleep 3

if ! kill -0 "$PF_PID" 2>/dev/null; then
    echo "ERROR: Port-forward failed to start. Is the predictor running?"
    exit 1
fi
echo "Port-forward active (PID $PF_PID)."

# -------------------------------------------------------------------
# 2. Query predictions for each hour of the day
# -------------------------------------------------------------------
echo ""
echo "Predicted CPU load and recommended replicas for each hour:"
echo ""
printf "  %-7s  %-14s  %-10s  %s\n" "Hour" "Predicted CPU" "Replicas" "Visual"
printf "  %-7s  %-14s  %-10s  %s\n" "-------" "--------------" "----------" "--------------------"

for hour in $(seq 0 23); do
    RESPONSE=$(curl -s "http://localhost:${LOCAL_PORT}/predict?hour=${hour}&minute=0")

    CPU=$(echo "$RESPONSE" | jq -r '.predicted_cpu')
    REPLICAS=$(echo "$RESPONSE" | jq -r '.recommended_replicas')

    # Build a simple bar chart
    BAR_LEN=$(echo "$CPU" | awk '{printf "%d", $1 / 5}')
    BAR=$(printf '%0.s#' $(seq 1 "$BAR_LEN") 2>/dev/null || echo "")

    printf "  %02d:00    %6.1f%%         %-4s      %s\n" "$hour" "$CPU" "$REPLICAS" "$BAR"
done

# -------------------------------------------------------------------
# 3. Show current state
# -------------------------------------------------------------------
echo ""
echo "Current sample-app replica count:"
kubectl get deployment sample-app -o wide
echo ""

# -------------------------------------------------------------------
# 4. Optional: watch mode
# -------------------------------------------------------------------
if [ "${1:-}" = "--watch" ]; then
    echo "Watching sample-app deployment (Ctrl+C to stop) ..."
    echo ""
    kubectl get deployment sample-app -w
fi
