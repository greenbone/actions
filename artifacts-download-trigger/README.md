# artifacts-download-trigger

This action is used to trigger workflows and download artifacts form another workflow.

# How to use download-trigger-downloader?

Please read [action.yml](https://github.com/greenbone/actions/blob/main/artifacts-download-trigger/action.yml) for more parameters.

```yaml
- name: Invoke 'timeout' workflow and wait for result using this action
  uses: greenbone/actions/artifacts-download-trigger
  with:
    workflow: artifacts-download-trigger-timeout.yml
    gh-token: ${{ secrets.GREENBONE_BOT_TOKEN }}
    path: ./
    wait-for-completion-interval: 10s
    wait-for-completion-timeout: 30s
```

# How to use Trigger?

Please read [bin/trigger/action.yml](https://github.com/greenbone/actions/blob/main/artifacts-download-trigger/bin/trigger/action.yml) for more parameters.

```yaml
- name: Invoke 'timeout' workflow and wait for result using this action
  uses: greenbone/actions/artifacts-download-trigger/bin/trigger
  with:
    workflow: artifacts-download-trigger-timeout.yml
    gh-token: ${{ secrets.GREENBONE_BOT_TOKEN }}
    display-workflow-run-url: 'true'
    wait-for-completion-interval: 10s
    wait-for-completion-timeout: 30s
```

# How to use Downloader?

Please read [bin/downloader/action.yml](https://github.com/greenbone/actions/blob/main/artifacts-download-trigger/bin/downloader/action.yml) for more parameters.

```yaml
- name: Invoke 'timeout' workflow and wait for result using this action
  uses: greenbone/actions/artifacts-download-trigger/bin/trigger
  with:
    workflow: artifacts-download-trigger-timeout.yml
    gh-token: ${{ secrets.GREENBONE_BOT_TOKEN }}
    path: ./
    artifact-name: artifact-name
```

For all options look to the workflows starting with `.github/workflows/artifacts-download-trigger-` or to the action.yml
in the `artifacts-download-trigger` folder.

#### Code reuse under MIT LICENSE from

- [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact)
    - [LICENSE](https://github.com/dawidd6/action-download-artifact/blob/master/LICENSE)
- [aurelien-baudet/workflow-dispatch](https://github.com/aurelien-baudet/workflow-dispatch)
    - [LICENSE](https://github.com/aurelien-baudet/workflow-dispatch/blob/master/LICENSE)
