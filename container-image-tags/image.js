const utils = require("./utils");

const createImageTag = (name, tag) => `${name}:${tag}`;

const createImageTags = ({
  imageName,
  currentBranch,
  targetBranch,
  headBranch,
  stripTagPrefix,
  isPullRequest = utils.isPullRequest,
}) => {
  const imageTags = [];
  if (targetBranch === "main") {
    // use unstable as name for main
    targetBranch = "unstable";
  }

  if (isPullRequest()) {
    // pull request
    imageTags.push(createImageTag(imageName, `${targetBranch}-${headBranch}`));
  } else if (utils.isTag(currentBranch)) {
    // tag
    imageTags.push(
      createImageTag(imageName, utils.getTagName(currentBranch, stripTagPrefix))
    );
  } else {
    // push into a branch
    if (targetBranch == "stable") {
      // also tag stable as latest
      imageTags.push(
        createImageTag(imageName, targetBranch),
        createImageTag(imageName, "latest")
      );
    } else {
      imageTags.push(createImageTag(imageName, targetBranch));
    }
  }
  return imageTags.join(",");
};

module.exports = {
  createImageTags,
  createImageTag,
};
