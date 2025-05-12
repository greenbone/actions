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

### Workflow

```yaml
jobs:
  deploy:
    name: Deploy
    runs-on: self-hosted-generic
    steps:
      - name:
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

## Inputs

| Name                           | Description                                                                                                                   |          |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------|----------|
| ssh-key            | SSH key file data. Optional if file exist.                                                                                                | Required |
| vars               | Extra vars like passwords that can not be in the inventory file. As yaml. Optional if file exist.                                         | Required |
| ssh-known-hosts    | SSH fingerprints for dev servers.                                                                                                         | Required |
| inventory          | Inventory file data in yaml. Optional if file exist.                                                                                      | Required |
| inventory-path     | Inventory file path. Default is inventory.yml.                                                                                            | Optional |
| ssh-key-path       | SSH key file path. Default is ssh.key                                                                                                     | Optional |
| vars-path          | Vars file path. Default is vars.yml                                                                                                       | Optional |
| limit-hosts        | Limit deployment to hosts. Default is all.                                                                                                | Optional |
