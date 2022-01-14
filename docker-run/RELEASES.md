# addnab/docker-run-action Releases

### 4.x.x

- Added a single output to the `action.yml`. This enables you to capture output from the container
  using `::set-output name=container_output::somethinggoeshere` (Added
  by [Trevor Sullivan](https://github.com/pcgeek86))
- Added support for WORKDIR and ENV (Added by [Linas Daneliukas](https://github.com/LDaneliukas))
- Added some workaround fixes to ENV forwarding to the docker in docker [Josef Fröhle](https://github.com/Dexus-Forks/docker-run-action/tree/forward_env)

### 3.0.0

- Upgrade to docker 20.10 [#12](https://github.com/addnab/docker-run-action/pull/12)

### 2.0.0

- Added support for networking with other
  containers [#3](https://github.com/addnab/docker-run-action/pull/3) [#7](https://github.com/addnab/docker-run-action/pull/7)
- Added tests [#7](https://github.com/addnab/docker-run-action/pull/7)

### 1.0.0

- Initial release
