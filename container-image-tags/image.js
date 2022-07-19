const utils = require("./utils");

const createImageTag = (name, tag, registry) =>
  registry ? `${registry}/${name}:${tag}` : `${name}:${tag}`;

const convertBranchName = (name) => (name === "main" ? "unstable" : name);

const createImageTags = ({
  imageName,
  currentRef,
  baseRef,
  headRef,
  stripTagPrefix,
  registry,
}) => {
  const imageTags = [];
  if (utils.isPullRequest()) {
    const targetBranch = convertBranchName(utils.getBranchName(baseRef));
    const headBranch = utils.getBranchName(headRef);
    // pull request
    imageTags.push(
      createImageTag(imageName, `${targetBranch}-${headBranch}`, registry)
    );
  } else if (utils.isTag(currentRef)) {
    // tag
    imageTags.push(
      createImageTag(
        imageName,
        utils.getTagName(currentRef, stripTagPrefix),
        registry
      )
    );
  } else {
    // push into a branch
    const currentBranch = convertBranchName(utils.getBranchName(currentRef));
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
