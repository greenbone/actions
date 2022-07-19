const utils = require("./utils");

const createImageTag = (name, tag, registry) =>
  registry ? `${registry}/${name}:${tag}` : `${name}:${tag}`;

const convertBranchName = (name) => (name === "main" ? "unstable" : name);

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
  if (utils.isPullRequest()) {
    targetBranch = convertBranchName(targetBranch);
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
    currentBranch = convertBranchName(currentBranch);
    imageTags.push(createImageTag(imageName, currentBranch, registry));

    if (currentBranch == "stable") {
      // also tag stable as latest
      imageTags.push(createImageTag(imageName, "latest", registry));
    }
  }
  return imageTags.join(",");
};

module.exports = {
  createImageTags,
  createImageTag,
};
