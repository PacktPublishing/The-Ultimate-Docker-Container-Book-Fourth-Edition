#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================"
echo "  Lab A — Deploy All Resources"
echo "============================================"

# -------------------------------------------------------------------
# 1. Deploy sample-app
# -------------------------------------------------------------------
echo ""
echo "Deploying sample-app ..."
kubectl apply -f "$PROJECT_DIR/sample-app/deployment.yaml"

# -------------------------------------------------------------------
# 2. Deploy predictor
# -------------------------------------------------------------------
echo ""
echo "Deploying predictor ..."
kubectl apply -f "$PROJECT_DIR/predictor/deployment.yaml"

# -------------------------------------------------------------------
# 3. Wait for rollouts
# -------------------------------------------------------------------
echo ""
echo "Waiting for deployments to become ready ..."
kubectl rollout status deployment/predictor --timeout=120s
kubectl rollout status deployment/sample-app --timeout=120s

# -------------------------------------------------------------------
# 4. Deploy autoscaler RBAC and CronJob
# -------------------------------------------------------------------
echo ""
echo "Deploying autoscaler RBAC and CronJob ..."
kubectl apply -f "$PROJECT_DIR/autoscaler/rbac.yaml"
kubectl apply -f "$PROJECT_DIR/autoscaler/cronjob.yaml"

# -------------------------------------------------------------------
# 5. Summary
# -------------------------------------------------------------------
echo ""
echo "============================================"
echo "  All resources deployed!"
echo "============================================"
echo ""
kubectl get deployments,services,cronjobs
echo ""
echo "The autoscaler CronJob will fire every 2 minutes."
echo "Watch scaling with:"
echo "  kubectl get deployment sample-app -w"
echo ""
