# Execution evidence

All logs, JSON test/build results, and images here came from actual execution on Ubuntu. Email addresses in saved console logs are replaced with `[configured-recipient]`; passwords and Jenkins authentication files are excluded entirely. The original 15 Firefox/Jenkins website screenshots remain unchanged. The nine additional terminal screenshots are native desktop captures cropped to the real evidence terminal, with no rendered or substituted text.

## Ubuntu terminal evidence

All new images are in `evidence/screenshots/`, alongside the preserved website images. Open a screenshot at original size for full readability. The Codex chat and unrelated monitor are excluded from every published terminal crop.

| Requirement | Screenshot and concise caption | Source/type |
| --- | --- | --- |
| Ubuntu, Java, Git, Maven, service | [16 — environment and active Jenkins service](screenshots/16-terminal-environment-window.png) | Live version/status commands; user systemd service identified explicitly |
| Hello World | [17 — Hello World SUCCESS](screenshots/17-terminal-hello-world-window.png) | `hello-world-job #1`; saved output from earlier run |
| Fresh Maven build | [18 — two tests pass and BUILD SUCCESS](screenshots/18-terminal-fresh-maven-window.png) | Fresh `clean package` executed in this terminal session; [complete stdout](terminal-fresh-maven-20261102T225321.txt) |
| Generated JAR | [19 — JAR listed, hashed and executed](screenshots/19-terminal-generated-jar-window.png) | Live commands on that fresh build's JAR; prints `Sum of 2 and 3 is 5` |
| Automatic build | [20 — poll finds GitHub change, build succeeds](screenshots/20-terminal-automatic-scm-window.png) | `java-maven-freestyle #2`; saved polling log and selected earlier build lines |
| Deliberate failure | [21 — expected 6, actual 5, Jenkins FAILURE](screenshots/21-terminal-failed-build-window.png) | `java-maven-freestyle #5`; saved output from earlier run |
| Recovery | [22 — two tests pass, archive and SUCCESS](screenshots/22-terminal-recovery-window.png) | `java-maven-freestyle #6`; saved output from earlier run |
| Upstream deployment | [23 — successful upstream, dev/1.0 and smoke tests](screenshots/23-terminal-upstream-deploy-window.png) | `deploy-job #6`, upstream calculator #6; saved cause, parameters and console output |
| Failure safety gate | [24 — failed build produces no deployment](screenshots/24-terminal-failure-gate-window.png) | Failed calculator #5; saved before/after downstream counts and deployment upstream-link cross-check |

[Capture provenance](terminal-capture-provenance.json) records lossless crop coordinates and screenshot hashes. Full-desktop originals remain private and ignored. [Terminal session metadata](terminal-session.json) records the fresh execution time and the historical/live distinction. [PDF practical-step audit](pdf-practical-audit.md) checks all 44 numbered steps and identifies the exact-procedure differences honestly.

Historical JSON snapshots remain unchanged, including their then-current notification-verification fields. The later recipient confirmation is recorded in [notification-verification.json](notification-verification.json), separately from any claim of independent mailbox inspection.

## Demonstrated runs

| Job/build | Trigger | Result | Evidence |
| --- | --- | --- | --- |
| Hello World #1 and #2 | Manual | SUCCESS | [#1 log](logs/hello-world-job-1.txt), [#2 log](logs/hello-world-job-2.txt), [screenshot](screenshots/01-hello-world.png) |
| Calculator #1 | Manual | SUCCESS; 2 tests passed; JAR archived | [log](logs/java-maven-freestyle-1.txt), [build screenshot](screenshots/02-maven-build-success.png), [two tests screenshot](screenshots/03-junit-two-passing-tests.png), [JUnit JSON](initial-test-results.json) |
| Calculator #2 | SCM change | SUCCESS; changed output; deployment started | [log](logs/java-maven-freestyle-2.txt), [polling log](scm-polling.txt), [screenshot](screenshots/04-automatic-scm-build.png) |
| Calculator #3 | SCM change | FAILURE; 1 of 2 tests failed; no archive/deploy | [log](logs/java-maven-freestyle-3.txt), [failed assertion](screenshots/08-intentional-test-failure.png), [no-artifact build page](screenshots/09-failure-build-no-artifact.png), [gate verification](failure-deployment-gate.json) |
| Calculator #4 | SCM change | SUCCESS; both tests pass; recovery mail sent; deploy resumed | [log](logs/java-maven-freestyle-4.txt) |
| Calculator #5 | SCM change | FAILURE; failure mail sent without SMTP error; no archive/deploy | [log](logs/java-maven-freestyle-5.txt), [tests screenshot](screenshots/10-notification-failure-tests.png), [test JSON](failure-email-test-results.json), [gate verification](failure-email-deployment-gate.json) |
| Calculator #6 | SCM change | SUCCESS; 2 tests pass; JAR archived; recovery mail sent; deploy resumed | [log](logs/java-maven-freestyle-6.txt), [recovery screenshot](screenshots/11-recovery-success.png), [two passing tests](screenshots/12-recovery-tests.png), [JUnit JSON](recovery-test-results.json), [polling log](scm-polling-recovery.txt) |
| Deploy #1 | Calculator #1 upstream | SUCCESS, defaults: dev / true / 1.0 | [log](logs/deploy-job-1.txt), [build JSON](logs/deploy-job-1.json) |
| Deploy #2 | Manual parameter demonstration | SUCCESS, staging / true / 1.0 | [log](logs/deploy-job-2.txt), [screenshot](screenshots/05-staging-deployment.png) |
| Deploy #3 | Calculator #2 upstream | SUCCESS, defaults | [log](logs/deploy-job-3.txt), [upstream screenshot](screenshots/06-upstream-deployment.png) |
| Deploy #4 | Manual parameter demonstration | SUCCESS, prod / false / 1.0; smoke tests skipped | [log](logs/deploy-job-4.txt), [screenshot](screenshots/07-prod-without-smoke-tests.png) |
| Deploy #5 | Calculator #4 upstream | SUCCESS, recovery reopens success gate | [log](logs/deploy-job-5.txt) |
| Deploy #6 | Calculator #6 upstream | SUCCESS, recovery reopens success gate again | [log](logs/deploy-job-6.txt), [build JSON](logs/deploy-job-6.json) |

The console for an upstream deployment prints both the upstream cause and its originating SCM/manual cause. The build JSON records the explicit `UpstreamCause` and build number.

The [parameter screenshot](screenshots/14-deployment-parameters.png) records the actual staging build's three parameter values.

## Source history

| Commit | Exercise |
| --- | --- |
| `37a9370c7c4a79d847317802aa4bc24555ced1a7` | Initial calculator with two correct tests |
| `ae8df3bc1263d96fb955a07aba5809825158f0be` | Changed calculator output; automatically built as #2 |
| `b26dbb67017276f64060bba0ab02992b0e073f5b` | Deliberately expected 6 instead of 5; failed as #3 |
| `e52b24e992c95e8e09f3ab5dc44ef76ef893caf6` | Restored correct expectation; recovery #4 |
| `aa9dea21dc5489501a3b33fda517ba75d750dbcf` | Repeated failure after Gmail authentication was fixed; #5 |
| `2d9206ed3285a82fb1a2346da2dfd818c9cc5187` | Restored passing tests for notification recovery #6 |

## Notification evidence and limits

The first SMTP configuration attempt connected to Gmail but returned `535 5.7.8` (bad credentials). Consequently calculator #3 attempted notification but could not send it. The user entered a Gmail App Password locally; the configuration test was then accepted. A subsequent live SMTP diagnostic also returned `SMTP_ACCEPTED` without revealing the secret. Calculator #4's recovery and #5's failure logs show sending email with no SMTP exception. The deliberate failure was repeated so notification verification does not rely on the earlier rejected attempt.

Calculator #6 then passed both tests, archived its JAR, sent the recovery notification without an SMTP exception, and triggered successful deployment #6. [notification-verification.json](notification-verification.json) records the successful mail attempts and the earlier rejected attempt.

The Jenkins logs record SMTP submission. In the follow-up request the user explicitly confirmed: **“I confirm that the notification emails arrived.”** This is recipient confirmation, separate from the recorded SMTP evidence; the assistant did not independently inspect the inbox. No inbox screenshot is fabricated or included. The Gmail App Password and Jenkins admin password remain in ignored local runtime storage and are absent from this repository.

## Artifacts and environment

- [Actual archived JAR from calculator #1](artifacts/jenkins-demo-1.0.jar), with [SHA-256 checksum](artifacts/SHA256SUMS).
- [Actual archived recovery JAR from calculator #6](artifacts/recovery-build-6/jenkins-demo-1.0.jar), with [SHA-256 checksum](artifacts/recovery-build-6/SHA256SUMS). Run it with `java -jar evidence/artifacts/recovery-build-6/jenkins-demo-1.0.jar`.
- [Actual Ubuntu/tool/service/disk output](environment.txt).
- [Assignment PDF identity](source-instructions.txt); the source PDF is not republished.
- [Plugin versions and checksums](../jenkins/plugins-lock.json).
- [Initial Jenkins startup screenshot](screenshots/00-jenkins-start.png).
- [Final dashboard screenshot](screenshots/13-final-dashboard.png).

The final polling schedule is `H/5 * * * *`. The live Jenkins parser confirmed the matching minutes as `03, 08, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58` for this job. No build starts when a poll finds no change. Faster polling was used only while collecting lab evidence.

Calculator builds run on the local Ubuntu user's account (`mirza`) through a localhost-only user systemd service. The `Running as SYSTEM` line is Jenkins's internal authorization identity, not the Unix root account.
