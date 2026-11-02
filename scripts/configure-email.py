#!/usr/bin/env python3
"""Run locally from the repository. The Gmail app password is never echoed or saved here."""
import getpass
import json
import pathlib
import sys
import requests

root = pathlib.Path(__file__).resolve().parents[1]
email = input('Gmail sender/recipient address: ').strip()
if not email or '@' not in email:
    raise SystemExit('An email address is required')
password = getpass.getpass('Gmail App Password (hidden input): ').replace(' ', '')
if not password:
    raise SystemExit('No app password entered; nothing changed')
s = requests.Session()
s.auth = ('lab-admin', (root / '.lab/admin-password').read_text().strip())
base = 'http://127.0.0.1:8080/'
r = s.get(base + 'crumbIssuer/api/json', timeout=15)
r.raise_for_status()
crumb = r.json()
s.headers[crumb['crumbRequestField']] = crumb['crumb']
# Use JSON string literals rather than interpolating raw input into Groovy syntax.
script = '''
import jenkins.model.Jenkins
import jenkins.model.JenkinsLocationConfiguration
import hudson.tasks.Mailer
def j = Jenkins.get()
def email = %s
def d = j.getDescriptorByType(Mailer.DescriptorImpl.class)
d.setSmtpHost('smtp.gmail.com')
d.setSmtpPort('465')
d.setUseSsl(true)
d.setUseTls(false)
d.setSmtpAuth(email, %s)
d.setReplyToAddress(email)
d.save()
def location = JenkinsLocationConfiguration.get()
location.setAdminAddress(email)
location.save()
def job = j.getItem('java-maven-freestyle')
def publisher = job.publishersList.get(Mailer.class)
if (publisher != null) job.publishersList.remove(publisher)
job.publishersList.add(new Mailer(email, false, false))
job.save()
def session = d.createSession()
def message = new jakarta.mail.internet.MimeMessage(session)
message.setFrom(new jakarta.mail.internet.InternetAddress(email))
message.setRecipients(jakarta.mail.Message.RecipientType.TO, email)
message.setSubject('Jenkins lab: SMTP configuration test')
message.setText('Genuine SMTP test from the local Ubuntu Jenkins assignment. Failure and recovery notifications are enabled.')
jakarta.mail.Transport.send(message)
println('SMTP test accepted by the outgoing mail server. Failure/recovery notification configured.')
''' % (json.dumps(email), json.dumps(password))
try:
    r = s.post(base + 'scriptText', data={'script': script}, timeout=90)
    r.raise_for_status()
    if 'SMTP test accepted' not in r.text:
        print('SMTP test failed. Check credentials/provider settings locally in Jenkins; no password was logged.')
        raise SystemExit(1)
    marker = root / '.lab/email-ready'
    marker.write_text('SMTP configuration test accepted\n')
    print(r.text.strip())
finally:
    password = None
    script = None
