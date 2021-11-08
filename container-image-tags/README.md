# Container Image Tags Action

An action for creating container image tags from branch, tag and pull request
names.

## Inputs

### `strip-tag-prefix`
The tag prefix to strip i.e v1.2.3 -> 1.2.3 (default 'v') if GitHub reference is
a tag.

### `image-name`
The image name to use. By default it is derived from the repository name.

### `registry`
A container registry to use for naming the container image tags

## Outputs

### `image-tags`

A comma separated string for container image tag names that should be used for
the image.

## Build

For building this JavaScript action [@vercel/ncc](https://github.com/vercel/ncc)
is used. When changing the source files it is required to build a new
distributable bundle by running `npm run build` and add the files `dist/*` to
the git repository.
