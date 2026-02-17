# Self-Hosted Runner Cache Mount
 
- Mount a cache directory on your self-hosted runner

#### Use Case
 
```yaml
jobs:
  cache-mount:
    name: Cache mount on self-hosted runner
    runs-on: ubuntu-latest
    steps:
      - ...
      - name: Mount Cache
        uses: greenbone/actions/self-hosted-runner-cache-mount@v3
      - ...
``` 
## Action Configuration
 
| Input Variable | Description                                                   | Default Value         |
| ---------------| ------------------------------------------------------------- | --------------------- |
| server         | NFS Server IP/Domain to mount.                                | 10.0.0.1              |
| path           | Mount Path on the runner where the cache will be mounted.     | /repository-cache     |
