#!/bin/sh
# Genuine screenshots rendered by installed Firefox on Ubuntu; no mock images.
# Run one capture at a time so Firefox can use its dedicated lab profile.
set -eu
name=${1:?Usage: capture-evidence.sh filename.png Jenkins-path}
path=${2?A Jenkins URL path is required (use an empty string for the dashboard)}
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
profile="$HOME/snap/firefox/common/jenkins-lab-profile"
mkdir -p "$profile" "$root/evidence/screenshots"
exec firefox --headless --no-remote --profile "$profile" \
  --window-size 1440,1000 --screenshot "$root/evidence/screenshots/$name" \
  "http://127.0.0.1:8080/$path"
