const core = require("@actions/core");
const image = require("./image");
const utils = require("./utils");

async function run() {
  const targetBranch = utils.getBranchName(process.env.GITHUB_BASE_REF);
  const currentBranch = utils.getBranchName(process.env.GITHUB_REF);
  const headBranch = utils.getBranchName(process.env.GITHUB_HEAD_REF);
  const imageName =
    core.getInput("image-name") || process.env.GITHUB_REPOSITORY;
  const stripTagPrefix = core.getInput("strip-tag-prefix") || "";
  const registry = core.getInput("registry");

  const imageTags = image.createImageTags({
    imageName,
    targetBranch,
    currentBranch,
    headBranch,
    stripTagPrefix,
    registry,
  });

  core.setOutput("image-tags", imageTags);
}

run();
