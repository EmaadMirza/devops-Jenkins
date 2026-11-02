# Jenkins calculator CI/CD lab

Executed on Ubuntu 24.04 with Java 21, Git, Jenkins **2.580.2 LTS**, and Maven **3.9.16**. The assignment instructions were read from the 23-page `Jenkins.pdf` on the accessible Windows data partition. Windows storage was accessed read-only; this lab writes to the Ubuntu project directory.

## What the lab does

```text
GitHub main changes
    → Jenkins Poll SCM
    → java-maven-freestyle
        clean workspace → checkout → compile → 2 JUnit tests → package → run JAR
        publish test results → archive/fingerprint JAR → failure/recovery email
        SUCCESS only → deploy-job (dev, smoke=true, version=1.0)
```

Three freestyle jobs implement the PDF's required workflow:

| Job | Configuration |
| --- | --- |
| `hello-world-job` | Prints greeting, job/build information, Ubuntu user, and date. |
| `java-maven-freestyle` | Checks out this repository's `main`, uses `JDK-21` and `Maven-3.9`, executes `clean package`, runs the JAR, publishes JUnit XML, archives successful JARs, sends notifications, and triggers deployment only on `SUCCESS`. |
| `deploy-job` | Simulates deployment with `ENV` (`dev`, `staging`, `prod`), `RUN_SMOKE_TEST` (default `true`), and `VERSION` (default `1.0`). It changes no remote server. |

The calculator has addition and subtraction operations. Exactly two JUnit 5 tests verify them. A deliberately broken assertion and its repair are separate commits, so the failure/recovery exercise is auditable in Git history.

## Actual results

See [the evidence index](evidence/README.md), [raw build logs](evidence/logs/), and [Ubuntu environment capture](evidence/environment.txt). Results are from Jenkins execution, not sample output. The index records build numbers, commit IDs, trigger causes, artifact availability, and notification status.

## Minimal installation and storage

To avoid the system package-manager lock and keep disk use small, this lab uses the official Jenkins WAR and Maven binary archive under ignored `.lab/`. It installs no Docker, extra JDK, database, or pipeline plugin bundle. SHA-256/SHA-512 checksums verify the tools, and all 47 required plugins/dependencies are pinned with SHA-256 checksums in [plugins-lock.json](jenkins/plugins-lock.json). The six requested plugin roots are Git, JUnit, Mailer, Workspace Cleanup, Timestamper, and Build Timeout.

Jenkins runs as the logged-in Ubuntu user in the **user systemd service** `jenkins-assignment`, bound to **127.0.0.1:8080**. This differs from the PDF's system-wide apt installation: there is no dedicated `jenkins` Unix account, no boot enablement, no firewall change, and no network exposure. This is a single-user teaching lab, not a production deployment.

One executor, a 768 MiB Java heap limit, a 10-minute build timeout, ten retained builds/artifacts per job, and one shared `.lab/m2` Maven cache limit resource usage. Each successful calculator run records `df -h /`. No unrelated files were removed or modified.

The provided repository is **public**, so Jenkins checks it out anonymously over HTTPS. A GitHub PAT is unnecessary for this checkout and is not stored in Jenkins. Repository writes use the authenticated GitHub connection. Existing history is preserved; no force-push is used.

## Run the calculator without Jenkins

With Java 21 and Maven 3.9 installed:

```bash
mvn -B -ntp clean package
java -jar target/jenkins-demo-1.0.jar
```

On this machine, Maven is local to the lab:

```bash
.lab/tools/apache-maven-3.9.16/bin/mvn -B -ntp \
  -Dmaven.repo.local="$PWD/.lab/m2" clean package
java -jar target/jenkins-demo-1.0.jar
```

Surefire writes `target/surefire-reports/*.xml`; the package is `target/jenkins-demo-1.0.jar`.

## Reproduce the Jenkins setup

Prerequisites: Ubuntu, Java 21 JDK, Git, Python 3, and `python3-requests` for the optional local email helper. Java and Git were already installed for this execution. The setup helper needs at least 750 MiB available and does not run sudo.

```bash
python3 scripts/setup-lab.py
sh scripts/start-jenkins.sh
systemctl --user status jenkins-assignment --no-pager
```

Open <http://localhost:8080/>. The local administrator username is `lab-admin`; the generated password is in the mode-600 file `.lab/admin-password`. Read it locally, never commit it. The dashboard permits read-only access on localhost; changing configuration or starting builds requires login.

The bootstrap imports the [three job XML templates](jenkins/) if the jobs do not already exist, configures the installed JDK and Maven, and replaces `@LAB_ROOT@` with the current repository location. Adjust the JDK path in `jenkins/bootstrap.groovy` if your JDK is elsewhere. Existing jobs are not overwritten.

Stop/start the local lab service using:

```bash
systemctl --user stop jenkins-assignment
sh scripts/start-jenkins.sh
```

The service is transient, so use the start script again after a reboot. Its data remains in `.lab/jenkins-home`.

## Job settings and exercises

- **SCM:** `https://github.com/EmaadMirza/devops-Jenkins.git`, branch `*/main`.
- **Polling:** final schedule `H/5 * * * *` (every five minutes). An every-minute schedule was used during the lab to shorten verification. Builds marked `SCMTriggerCause` were scheduled by Jenkins polling; they were not started through Build Now.
- **Environment:** clean workspace before checkout, timestamps, absolute 10-minute timeout with abort.
- **Build:** Maven `-B -ntp clean package` with the shared local cache, followed by running the executable JAR.
- **JUnit:** `target/surefire-reports/*.xml`, empty results forbidden.
- **Artifacts:** `target/*.jar`, successful builds only, fingerprinted.
- **Chaining:** core “Build other projects” publisher targeting `deploy-job`, threshold `SUCCESS`. Automatically triggered deployments use the parameter defaults. Separate manual parameter demonstrations cover staging with smoke tests and production simulation without them.
- **Failure:** change `assertEquals(5, c.add(2, 3))` to `assertEquals(6, c.add(2, 3))`, commit, and let polling build it. Maven must return nonzero; no JAR is archived and no downstream deployment is triggered.
- **Recovery:** change `6` back to `5`, commit, and let polling build it. Both tests pass, the JAR is archived, and deployment resumes.

## Email without committing credentials

Gmail requires 2-Step Verification and a Google App Password; a normal Google account password is not sufficient. Create one at <https://myaccount.google.com/apppasswords>, then run locally:

```bash
python3 scripts/configure-email.py
```

The helper asks for the address and hidden App Password, sends them only to the local Jenkins server, configures SMTP SSL on `smtp.gmail.com:465`, and sends a real configuration test. It saves the credential encrypted inside ignored Jenkins home. It never places the password in a command argument, repository file, screenshot, or build console. The exported job template has an empty recipient; configure your own locally. “Send to individuals” is disabled so only the configured recipient receives lab messages.

Successful SMTP submission proves acceptance by the outgoing server; inbox delivery requires recipient confirmation. See the evidence index for the status actually verified in this run.

## Evidence and secrets

Screenshots are genuine Jenkins pages captured by the installed Firefox running on Ubuntu in headless mode. They are browser-page screenshots, not full-desktop captures or fabricated terminal images. Reproduce one with:

```bash
sh scripts/capture-evidence.sh example.png job/java-maven-freestyle/1/
```

The capture uses a dedicated lab Firefox profile. Screenshots avoid credential/settings pages. `.lab/`, Maven `target/`, keys, environment files, and Python bytecode are excluded from Git. The public evidence includes selected build metadata, test results, logs with the notification address redacted, and actual archived JARs with SHA-256 checksums. [Final disk output](evidence/final-disk-space.txt) records approximately 2.7 GiB available when the evidence was finalized.

References: [Jenkins WAR installation](https://www.jenkins.io/doc/book/installing/war-file/), [Maven installation](https://maven.apache.org/install.html), [Google App Passwords](https://support.google.com/accounts/answer/185833).
