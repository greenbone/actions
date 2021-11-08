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

  core.startGroup("env");
  core.info(`GITHUB_BASE_REF: ${process.env.GITHUB_BASE_REF}`);
  core.info(`GITHUB_REF: ${process.env.GITHUB_REF}`);
  core.info(`GITHUB_HEAD_REF: ${process.env.GITHUB_HEAD_REF}`);
  core.info(`GITHUB_REPOSITORY: ${process.env.GITHUB_REPOSITORY}`);
  core.endGroup();

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
