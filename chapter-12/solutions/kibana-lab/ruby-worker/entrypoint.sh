#!/bin/sh
set -e
if [ -n "$LOGGING_FILE" ]; then
  mkdir -p "$(dirname "$LOGGING_FILE")"
  : > "$LOGGING_FILE"
  exec ruby worker.rb 2>&1 | tee -a "$LOGGING_FILE"
else
  exec ruby worker.rb 2>&1
fi