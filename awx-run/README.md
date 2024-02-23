# Run AWX job or project

- Start and wait for an AWX job and or project update

## Use Case

```yaml
jobs:
  awx-run:
    name: Start a AWX job and or project update
    runs-on:
      - self-hosted
      - self-hosted-generic
    steps:
      - name: Start and wait for a AWX job template
        uses: ./.github/actions/awx-run
        with:
          controller-host: 192.168.1.1
          controller-username: TEST
          controller-password: PW
          job-template: Test workflow

```

## Inputs

| Name                      |                                                                                              |          |
|---------------------------|----------------------------------------------------------------------------------------------|----------|
| controller-host           | AWX DNS or IP address.                                                                       | Required |
| controller-username       | AWX User name to login.                                                                      | Required |
| controller-password       | AWX Password to login.                                                                       | Required |
| controller-validate-certs | Validate AWX tls certs. Default is false .                                                   | Optional |
| project-name              | AWX project to update. If not set no project will be updated. Default: empty.                | Optional |
| job-template              | AWX job to run. If not set no job will be started. Default: empty.                           | Optional |
| job-extra-vars            | Json string with extra vars for job template. Default is a empty json.                       | Optional |
| job-wait-retries          | Retries to check if a job still running. Default: is 240 .                                   | Optional |
| job-wait-retry-delay      | Delay between job wait retries. Default: is 30 .                                             | Optional |
| workflow-template         | AWX workflow to run. If not set no job will be started. Default: empty.                      | Optional |
| workflow-node             | AWX workflow node to wait for Default: empty.                                                | Optional |
| workflow-extra-vars       | Json string with extra vars for workflow template. Default is a empty json.                  | Optional |
| workflow-timeout          | Timeout to wait for an workflow or an workflow node to finish in seconds. Default: is 3600 . | Optional |
| python-version            | Python version to use for running the action. Default is 3.11 .                              | Optional |
| skip-installation-on      | Skip installation on selected runner. Default is self-hosted-generic.                        | Optional |
