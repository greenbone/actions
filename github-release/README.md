# Github release

- Create github release with tag

#### Use Case

```yaml
jobs:
  github-release:
    name: Create a github release
    runs-on:
      - self-hosted
      - self-hosted-generic
    steps:
      - uses: greenbone/actions/github-release@v1
        with:
          release-name:
          tag-name:
          create-tag: true/false default false
          draft: true/false default false
          prerelease: true/false default false
          github-user:
          github-user-mail:
          github-user-token:
```

