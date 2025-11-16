#!/bin/sh
set -e

# Print Node version and environment for diagnostics
echo "Node version: $(node -v)"
echo "NODE_ENV: $NODE_ENV"
echo "LOGGING_FILE: $LOGGING_FILE"

if [ -n "$LOGGING_FILE" ]; then
  mkdir -p $(dirname "$LOGGING_FILE")
  touch "$LOGGING_FILE"
  exec npm start 2>&1 | tee -a "$LOGGING_FILE"
else
  exec npm start 2>&1
fi