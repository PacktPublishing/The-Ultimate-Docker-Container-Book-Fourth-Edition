#!/bin/bash
set -euo pipefail

CLUSTER_NAME="lab-a"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================"
echo "  Lab A — Setup Cluster"
echo "============================================"

# -------------------------------------------------------------------
# 1. Check prerequisites
# -------------------------------------------------------------------
echo ""
echo "Checking prerequisites ..."

for cmd in docker kind kubectl; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "ERROR: '$cmd' is not installed or not on PATH."
        exit 1
    fi
done

echo "  docker  $(docker version --format '{{.Client.Version}}' 2>/dev/null)"
echo "  kind    $(kind version 2>/dev/null)"
echo "  kubectl $(kubectl version --client -o json 2>/dev/null | jq -r .clientVersion.gitVersion)"

# -------------------------------------------------------------------
# 2. Delete existing cluster if present (idempotent)
# -------------------------------------------------------------------
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo ""
    echo "Deleting existing '${CLUSTER_NAME}' cluster ..."
    kind delete cluster --name "$CLUSTER_NAME"
fi

# -------------------------------------------------------------------
# 3. Create cluster
# -------------------------------------------------------------------
echo ""
echo "Creating kind cluster '${CLUSTER_NAME}' ..."
kind create cluster --config "$PROJECT_DIR/kind-config.yaml" --name "$CLUSTER_NAME"

# -------------------------------------------------------------------
# 4. Build Docker images
# -------------------------------------------------------------------
echo ""
echo "Building predictor image ..."
docker build -t predictor:1.0 "$PROJECT_DIR/predictor"

echo ""
echo "Building autoscaler image ..."
docker build -t autoscaler:1.0 "$PROJECT_DIR/autoscaler"

# -------------------------------------------------------------------
# 5. Load images into kind
# -------------------------------------------------------------------
echo ""
echo "Loading images into kind cluster ..."
kind load docker-image predictor:1.0 --name "$CLUSTER_NAME"
kind load docker-image autoscaler:1.0 --name "$CLUSTER_NAME"

# -------------------------------------------------------------------
# Done
# -------------------------------------------------------------------
echo ""
echo "============================================"
echo "  Cluster '${CLUSTER_NAME}' is ready!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  bash scripts/deploy-all.sh"
echo ""
