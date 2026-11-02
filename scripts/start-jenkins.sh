#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
test -f "$root/.lab/tools/jenkins.war" || {
  echo 'Download the verified Jenkins WAR described in README.md first.' >&2; exit 1;
}
available=$(df -Pk "$root" | awk 'NR==2 {print $4}')
test "$available" -gt 524288 || { echo 'Less than 512 MiB free; stopping.' >&2; exit 1; }
exec systemd-run --user --unit=jenkins-assignment --working-directory="$root" \
  --setenv="JENKINS_HOME=$root/.lab/jenkins-home" \
  /usr/bin/java -Xms128m -Xmx768m -Djava.awt.headless=true \
  -Djenkins.install.runSetupWizard=false -jar "$root/.lab/tools/jenkins.war" \
  --httpListenAddress=127.0.0.1 --httpPort=8080 --webroot="$root/.lab/war"
