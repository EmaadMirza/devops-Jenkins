#!/bin/sh
set -eu
echo "Hello from Jenkins!"
echo "Job Name     : $JOB_NAME"
echo "Build Number : $BUILD_NUMBER"
echo "Build URL    : $BUILD_URL"
echo "Workspace    : $WORKSPACE"
echo "Running as   : $(whoami)"
date
