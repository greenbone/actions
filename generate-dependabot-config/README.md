# Script to generate a dependabot config

To manually rebuild and overwrite the mcurrent dependabot config for the repository at the parent directory seen from here, run:

```
poetry install
poetry run generate-dependabot-config
```

Then commit the changed .```github/dependabot.yml``` file.

If the file needs to be different, look at [dependabot.tmpl.yml.j2](action/templates/dependabot.tmpl.yml.j2) and
make necessary changes, and/or adjust the handling in [dependabot_config.py](action/dependabot_config_generator.py).
