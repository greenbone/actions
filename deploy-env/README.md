# Deploy environment

- Deploy a environment on a server

## Use Case

### Github vars

#### INVENTORY

```yaml
all:
  hosts:
    my_dev_system:
      ansible_host: <DOMAIN/IP>
      ansible_user: root
      ansible_python_interpreter: /usr/bin/python3
```

#### KNOWN_HOSTS_FILE

```yaml
ssh fingerprint ...
```

#### VARS

##### copy`

* **Purpose**: Specifies files or directories to be transferred as part of a deployment process.
* **Usage**: Commonly used to move necessary data, code, or configuration files into a target environment.

##### env

* **Purpose**: Defines **environment variables**, which are key-value pairs used with the cmd command.
* **Usage**: Often used to pass values like credentials, configuration options, or environment-specific settings into the cmd command.

##### cmd

* **Purpose**: Run any kind of shell/powershell scripts on the target environment.
* **Usage**: Executes shell (or system) commands, such as run deployments e.g compose, starting services, etc.

##### Example
```yaml
copy:
  - my_deployment_data_folder1
  - my_deployment_data_folder2
env:
  my_env: Hello world
cmd: |
  echo $my_env
  ls my_deployment_data_folder
  cd my_deployment_data_folder
  compose down
  compose up
  ...
```

### Workflow

#### Deploy with inventory file

```yaml
jobs:
  deploy:
    name: Deploy with inventory file
    runs-on: self-hosted-generic
    steps:
      - name: Deploy with inventory file
        uses: greenbone/actions/deploy-env@v3
        with:
          ssh-key: ${{ secrets.SSH_KEY }}
          ssh-known-hosts: ${{ vars.KNOWN_HOSTS_FILE }}
          inventory: ${{ vars.INVENTORY }}
          vars: |
            copy: my_deployment_data_folder
            env:
              my_env: Hello world
            cmd: |
              echo $my_env
              ls my_deployment_data_folder
```

#### Deploy on one node
```yaml
jobs:
  deploy:
    name: Deploy on one node
    runs-on: self-hosted-generic
    steps:
      - name: Deploy on one node
        uses: greenbone/actions/deploy-env@v3
        with:
          ssh-key: ${{ secrets.SSH_KEY }}
          ssh-known-hosts: ${{ vars.KNOWN_HOSTS_FILE }}
          inventory-path: 192.168.0.1,
          user: root
          vars: |
            copy: my_deployment_data_folder
            env:
              my_env: Hello world
            cmd: |
              echo $my_env
              ls my_deployment_data_folder
```

## Inputs

| Name                           | Description                                                                                                                                                                           |          |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| ssh-key                        | SSH key file data. Optional if file exist.                                                                                                                                            | Required |
| vars                           | Extra vars like passwords that can not be in the inventory file or the cmd command to run on the node. As yaml. Optional if file exist.                                               | Required |
| inventory                      | Inventory file data as yaml. Optional if file exist.                                                                                                                                  | Required |
| ssh-known-hosts                | SSH fingerprints for dev servers. Optional if file exist.                                                                                                                             | Optional |
| user                           | Username used for login. ONLY set this if you inventory-path is a comma(,) seperated list of IP/Domain names. If not please put the username in the inventory file. Default is empty. | Optional |
| inventory-path                 | Inventory file path, or a comma(,) seperated list of IP/Domain names, if it is a just one IP/Domain it needs a comma at the end. Default is inventory.yml.                            | Optional |
| ssh-key-path                   | SSH key file path, if user is set. Default is ssh.key                                                                                                                                 | Optional |
| vars-path                      | Vars file path. Default is vars.yml                                                                                                                                                   | Optional |
| limit-hosts                    | Limit deployment to hosts. Default is all.                                                                                                                                            | Optional |
| base-dir                       | The the base directory / working directory. Default is current working directory.                                                                                                     | Optional |
| os                             | OS on target. Default is linux. Support for linux and windows.                                                                                                                        | Optional |
| winrm-password                 | Winrm auth password, if user is set. Default is 5986.                                                                                                                                 | Optional |
| winrm-port                     | Winrm port, if user is set. Default is 5986.                                                                                                                                          | Optional |
| winrm-transport                | Winrm transport, if user is set. Default is basic.                                                                                                                                    | Optional |
| winrm-server-cert-validation   | Winrm cert validation, if user is set. Default is ignore.                                                                                                                             | Optional |
