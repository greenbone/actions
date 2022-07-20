const core = require("@actions/core");
const github = require("@actions/github");
const image = require("./image");

async function run() {
  const baseRef = process.env.GITHUB_BASE_REF;
  const currentRef = process.env.GITHUB_REF;
  const headRef = process.env.GITHUB_HEAD_REF;
  const imageName =
    core.getInput("image-name") || process.env.GITHUB_REPOSITORY;
  const stripTagPrefix = core.getInput("strip-tag-prefix") || "";
  const registry = core.getInput("registry");

  core.startGroup("env");
  core.info(`GITHUB_BASE_REF: ${baseRef}`);
  core.info(`GITHUB_REF: ${currentRef}`);
  core.info(`GITHUB_HEAD_REF: ${headRef}`);
  core.info(`GITHUB_REPOSITORY: ${process.env.GITHUB_REPOSITORY}`);
  core.endGroup();

  if (core.isDebug()) {
    core.debug(`github: ${github}`);
  }

  const imageTags = image.createImageTags({
    imageName,
    baseRef,
    currentRef,
    headRef,
    stripTagPrefix,
    registry,
  });

  core.setOutput("image-tags", imageTags);
}

run();
