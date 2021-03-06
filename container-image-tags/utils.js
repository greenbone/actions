const github = require("@actions/github");

const isPullRequest = () => !!github.context.payload.pull_request;

const isTag = (name) => name && name.startsWith("refs/tags");

const getBranchName = (name) => {
  if (!name) {
    return "";
  }

  const regexp = new RegExp("refs/heads/(?<branch>.*)");
  const match = regexp.exec(name);
  if (match && match.groups && match.groups.branch) {
    // we must replace a / with something else (going with - for now)
    // to avoid invalid docker image tag names
    return match.groups.branch.replace(/\//, "-");
  }
  return name.replace(/\//, "-");
};

const getTagName = (name, stripTagPrefix = "") => {
  if (!name) {
    return "";
  }

  const regexp = new RegExp(`refs/tags/${stripTagPrefix}(?<tag>.*)`);
  const match = regexp.exec(name);
  if (match && match.groups && match.groups.tag) {
    return match.groups.tag;
  }
  return name;
};

module.exports = {
  isPullRequest,
  isTag,
  getBranchName,
  getTagName,
};
