const github = require("@actions/github");

const isPullRequest = () => !!github?.context?.payload?.pull_request;

const isTag = (name) => name && name.startsWith("refs/tags");

const getBranchName = (name) => {
  if (!name) {
    return "";
  }

  const regexp = new RegExp("refs/heads/(?<branch>.*)");
  const match = regexp.exec(name);
  return match?.groups?.branch || name;
};

const getTagName = (name, stripTagPrefix = "") => {
  if (!name) {
    return "";
  }

  const regexp = new RegExp(`refs/tags/${stripTagPrefix}(?<tag>.*)`);
  const match = regexp.exec(name);
  return match?.groups?.tag || name;
};

module.exports = {
  isPullRequest,
  isTag,
  getBranchName,
  getTagName,
};
