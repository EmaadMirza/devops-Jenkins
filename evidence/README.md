# Execution evidence

All logs, JSON test/build results, and images here came from the actual local Ubuntu Jenkins instance. Email addresses in saved console logs are replaced with `[configured-recipient]`; passwords and Jenkins authentication files are excluded entirely. Screenshots are unedited Firefox captures of real Jenkins pages rendered on Ubuntu, not mockups or full-desktop photographs.

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

The evidence proves SMTP submission from Jenkins; inbox receipt is not independently verified. No inbox screenshot is fabricated or included. The Gmail App Password and Jenkins admin password remain in ignored local runtime storage and are absent from this repository.

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
