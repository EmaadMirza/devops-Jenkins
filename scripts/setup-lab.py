#!/usr/bin/env python3
"""Install only verified lab-local Jenkins, Maven, and locked required plugins. No sudo."""
import base64
import concurrent.futures
import hashlib
import json
import pathlib
import secrets
import shutil
import tarfile
import urllib.request

root = pathlib.Path(__file__).resolve().parents[1]
lab = root / '.lab'
tools = lab / 'tools'
home = lab / 'jenkins-home'
if shutil.disk_usage(root).free < 750 * 1024 * 1024:
    raise SystemExit('Need at least 750 MiB free for this minimal lab; no files changed.')
tools.mkdir(parents=True, exist_ok=True)
(home / 'plugins').mkdir(parents=True, exist_ok=True)
checksums = json.loads((root / 'jenkins/tool-checksums.json').read_text())

def fetch(url, path, algo, expected):
    if not path.exists():
        print('Downloading', path.name, flush=True)
        data = urllib.request.urlopen(url, timeout=180).read()
        digest = hashlib.new(algo, data).hexdigest()
        if digest != expected: raise ValueError('Checksum mismatch: ' + path.name)
        path.write_bytes(data)
    elif hashlib.new(algo, path.read_bytes()).hexdigest() != expected:
        raise ValueError('Existing file checksum mismatch: ' + str(path))

fetch('https://get.jenkins.io/war-stable/2.580.2/jenkins.war', tools / 'jenkins.war', 'sha256', checksums['jenkins-war-sha256'])
maven = tools / 'apache-maven-3.9.16-bin.tar.gz'
fetch('https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.16/apache-maven-3.9.16-bin.tar.gz', maven, 'sha512', checksums['maven-tar-sha512'])
if not (tools / 'apache-maven-3.9.16').exists():
    with tarfile.open(maven) as archive:
        archive.extractall(tools, filter='data')

plugins = json.loads((root / 'jenkins/plugins-lock.json').read_text())
def plugin(item):
    name, data = item
    expected = base64.b64decode(data['sha256']).hex()
    fetch(data['url'], home / 'plugins' / (name + '.jpi'), 'sha256', expected)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(plugin, plugins.items()))

password = lab / 'admin-password'
if not password.exists():
    password.write_text(secrets.token_urlsafe(32))
password.chmod(0o600)
(home / 'init.groovy.d').mkdir(exist_ok=True)
shutil.copyfile(root / 'jenkins/bootstrap.groovy', home / 'init.groovy.d/10-lab.groovy')
print('Verified lab files ready. Run: sh scripts/start-jenkins.sh')
