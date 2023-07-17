# Npm build and push

- Build and Push npm package to registry.

#### Use Case

```yaml
jobs:
  npm-build-push:
    name: Build and push npm pkg
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push npm pkg
        uses: greenbone/actions/npm-build-push@v3
        with:
          scripts: "storybook:build build:source"
          registry-token: Registry user password/token
```

## Action Configuration

| Input Variable | Description                                                                                               |          |
|----------------|-----------------------------------------------------------------------------------------------------------|----------|
| version        | Node version to setup. Set to empty to not run a setup. Default: 18.x                                     | Optional |
| run-ci         | Run node ci. Default: false Options: true/false                                                           | Optional |
| scripts        | Space separated string of script names to run the build. If not set no package will build. Default: empty | Optional |
| registry-url   | The registry url used to push npm packages to. Default: https://npm.pkg.github.com                        | Optional |
| registry-token | Registry login password/token. If not set packages will not pushed to registry. Default: empty            | Optional |
