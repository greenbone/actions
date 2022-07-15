# Sphinx rst files

- Generate sphinx rst files.

## Arguments

| Argument | Description |
| --- | --- |
| doc-dir | Doc folder folder |
| source-dir | Source code folder |
| output-dir | Rst files output folder |
| pip-sphinx-modules | Space separated list of pip modules to install, empty use pyproject.toml |
| unwanted-rst | Space separated list of rst files to remove |
| version | Update sphinx conf.py release version |


## Use Case

```yaml
jobs:
  example:
    name: example
    runs-on:
      - self-hosted
    steps:
      - uses: greenbone/actions/generate-sphinx-rst-files@v1
        with:
          doc-dir: ./docs
          source-dir: ../CODE_FOLDER
          output-dir: test123
          unwanted-rst: "modules.rst test.rst"
          version: 123
          pip-sphinx-modules: sphinx-autodoc-typehints
```
