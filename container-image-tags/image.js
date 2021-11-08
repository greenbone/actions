const utils = require("./utils");

const createImageTag = (name, tag, registry) =>
  registry ? `${registry}/${name}:${tag}` : `${name}:${tag}`;

const createImageTags = ({
  imageName,
  currentBranch,
  targetBranch,
  headBranch,
  stripTagPrefix,
  registry,
  isPullRequest = utils.isPullRequest,
}) => {
  const imageTags = [];
  if (targetBranch === "main") {
    // use unstable as name for main
    targetBranch = "unstable";
  }

  if (isPullRequest()) {
    // pull request
    imageTags.push(
      createImageTag(imageName, `${targetBranch}-${headBranch}`, registry)
    );
  } else if (utils.isTag(currentBranch)) {
    // tag
    imageTags.push(
      createImageTag(
        imageName,
        utils.getTagName(currentBranch, stripTagPrefix),
        registry
      )
    );
  } else {
    // push into a branch
    if (targetBranch == "stable") {
      // also tag stable as latest
      imageTags.push(
        createImageTag(imageName, targetBranch, registry),
        createImageTag(imageName, "latest", registry)
      );
    } else {
      imageTags.push(createImageTag(imageName, targetBranch, registry));
    }
  }
  return imageTags.join(",");
};

module.exports = {
  createImageTags,
  createImageTag,
};
