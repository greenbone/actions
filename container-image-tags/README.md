# Container Image Tags Action

An action for creating container image tags from branch, tag and pull request
names.

## Inputs

### `strip-tag-prefix`
The tag prefix to strip i.e v1.2.3 -> 1.2.3 (default 'v') if GitHub reference is
a tag.

### `image-name`
The image name to use. By default it is derived from the repository name using
the schema (`<organization>/<repository>`).

### `registry`
A container registry to use for naming the container image tags

## Outputs

### `image-tags`

A string containing the tag for a container image using the following default
pattern `<image-name>:<target-branch>` or `<registry>/<image-name>:<target-branch>`
if a registry is provided.

Additional naming rules (hint: rules are shown without an input registry):

* Pushes targeting `main` branch

    `<image-name>:unstable`

* Pull Request targeting `main` branch

    `<image-name>:unstable-<pr-branch-name>`

* Pushes targeting `stable` branch

    `<image-name>:stable,<image-name>:latest`

* Pull Request targeting `stable` branch

    `<image-name>:stable-<pr-branch-name>`

* Pushes targeting `oldstable` branch

    `<image-name>:oldstable`

* Pull Request targeting `oldstable` branch

    `<image-name>:oldstable-<pr-branch-name>`

* Pushes for tags

    `<image-name>:<tag-name>`


## Build

For building this JavaScript action [@vercel/ncc](https://github.com/vercel/ncc)
is used. When changing the source files it is required to build a new
distributable bundle by running `npm run build` and add the files `dist/*` to
the git repository.
