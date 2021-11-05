const image = require("./image");

describe("createImageTag", () => {
  it("should create an image tag", () => {
    expect(image.createImageTag("foo", "latest")).toEqual("foo:latest");
    expect(image.createImageTag("foo", "1.2.3")).toEqual("foo:1.2.3");
  });
});

describe("createImageTags", () => {
  it("should create image tags for git tags", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      currentBranch: "refs/tags/v1.2.3",
      isPullRequest: () => false,
    });

    expect(imageTags).toEqual("foo:v1.2.3");
  });

  it("should create stripped image tags for git tags", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      currentBranch: "refs/tags/v1.2.3",
      stripTagPrefix: "v",
      isPullRequest: () => false,
    });

    expect(imageTags).toEqual("foo:1.2.3");
  });

  it("should create image tags for PRs targeting main branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      headBranch: "feature-x",
      targetBranch: "main",
      stripTagPrefix: "v",
      isPullRequest: () => true,
    });

    expect(imageTags).toEqual("foo:unstable-feature-x");
  });

  it("should create image tags for PRs targeting stable branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      headBranch: "feature-x",
      targetBranch: "stable",
      stripTagPrefix: "v",
      isPullRequest: () => true,
    });

    expect(imageTags).toEqual("foo:stable-feature-x");
  });

  it("should create image tags for PRs targeting unstable branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      headBranch: "feature-x",
      targetBranch: "unstable",
      stripTagPrefix: "v",
      isPullRequest: () => true,
    });

    expect(imageTags).toEqual("foo:unstable-feature-x");
  });

  it("should create image tags for pushes to main branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      targetBranch: "main",
      stripTagPrefix: "v",
      isPullRequest: () => false,
    });

    expect(imageTags).toEqual("foo:unstable");
  });

  it("should create image tags for pushes to stable branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      targetBranch: "stable",
      stripTagPrefix: "v",
      isPullRequest: () => false,
    });

    expect(imageTags).toEqual("foo:stable,foo:latest");
  });

  it("should create image tags for pushes to oldstable branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      targetBranch: "oldstable",
      stripTagPrefix: "v",
      isPullRequest: () => false,
    });

    expect(imageTags).toEqual("foo:oldstable");
  });
});
