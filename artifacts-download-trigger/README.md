# artifacts-download-trigger

This action is used to trigger workflows and download artifacts form the workflow.

# How to use?

```yaml
-   name: Invoke 'timeout' workflow and wait for result using this action
    uses: greenbone/actions/artifacts-download-trigger
    with:
      workflow: artifacts-download-trigger-timeout.yml
      gh_token: ${{ secrets.BOT_PAT_TOKEN }}
      wait-for-completion-interval: 10s
      wait-for-completion-timeout: 30s
```

For all options look to the workflows starting with `.github/workflows/artifacts-download-trigger-` or to the action.yml in the `artifacts-download-trigger` folder.

#### Code reuse under MIT LICENSE from
- [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact) - [LICENSE](https://github.com/dawidd6/action-download-artifact/blob/master/LICENSE)
- [aurelien-baudet/workflow-dispatch](https://github.com/aurelien-baudet/workflow-dispatch) - [LICENSE](https://github.com/aurelien-baudet/workflow-dispatch/blob/master/LICENSE)