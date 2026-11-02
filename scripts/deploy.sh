#!/bin/sh
set -eu
case "$ENV" in dev|staging|prod) ;; *) echo "Invalid ENV" >&2; exit 2;; esac
printf '%s\n' '=============================================='
printf ' Deploying version %s to %s (SIMULATION)\n' "$VERSION" "$ENV"
printf '%s\n' '=============================================='
if [ "$ENV" = prod ]; then echo "WARNING: Production deployment simulation"; fi
echo "Simulating copying application to $ENV server..."
sleep 2
echo "Deployment to $ENV completed (simulation; no remote server changed)"
if [ "$RUN_SMOKE_TEST" = true ]; then
  echo "Running simulated smoke tests on $ENV..."
  sleep 1
  echo "Smoke tests passed (simulation)"
else
  echo "Smoke tests skipped"
fi
