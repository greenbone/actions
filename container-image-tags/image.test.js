const image = require("./image");
const utils = require("./utils");

jest.mock("./utils", () => {
  const originalModule = jest.requireActual("./utils");

  //Mock the default export and named export 'foo'
  return {
    ...originalModule,
  };
});

describe("createImageTag", () => {
  it("should create an image tag", () => {
    expect(image.createImageTag("foo", "latest")).toEqual("foo:latest");
    expect(image.createImageTag("foo", "1.2.3")).toEqual("foo:1.2.3");
  });

  it("should create an image tag with registry", () => {
    expect(image.createImageTag("foo", "latest", "ghcr.io")).toEqual(
      "ghcr.io/foo:latest"
    );
    expect(image.createImageTag("foo", "1.2.3", "ghcr.io")).toEqual(
      "ghcr.io/foo:1.2.3"
    );
  });
});

describe("createImageTags", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it("should create image tags for git tags", () => {
    utils.isPullRequest = jest.fn(() => false);

    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/tags/v1.2.3",
    });

    expect(imageTags).toEqual("foo:v1.2.3");
  });

  it("should create stripped image tags for git tags", () => {
    utils.isPullRequest = jest.fn(() => false);

    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/tags/v1.2.3",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:1.2.3");
  });

  it("should create image tags for git tags with registry", () => {
    utils.isPullRequest = jest.fn(() => false);

    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/tags/v1.2.3",
      registry: "ghcr.io",
    });

    expect(imageTags).toEqual("ghcr.io/foo:v1.2.3");
  });

  it("should create image tags for PRs targeting main branch", () => {
    utils.isPullRequest = jest.fn(() => true);

    const imageTags = image.createImageTags({
      imageName: "foo",
      headRef: "feature-x",
      baseRef: "main",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:unstable-feature-x");
  });

  it("should create image tags for PRs targeting stable branch", () => {
    utils.isPullRequest = jest.fn(() => true);

    const imageTags = image.createImageTags({
      imageName: "foo",
      headRef: "feature-x",
      baseRef: "stable",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:stable-feature-x");
  });

  it("should create image tags for PRs targeting unstable branch", () => {
    utils.isPullRequest = jest.fn(() => true);

    const imageTags = image.createImageTags({
      imageName: "foo",
      headRef: "feature-x",
      baseRef: "unstable",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:unstable-feature-x");
  });

  it("should create image tags for PRs targeting a branch with a registry", () => {
    utils.isPullRequest = jest.fn(() => true);

    const imageTags = image.createImageTags({
      imageName: "foo",
      headRef: "feature-x",
      baseRef: "main",
      stripTagPrefix: "v",
      registry: "ghcr.io",
    });

    expect(imageTags).toEqual("ghcr.io/foo:unstable-feature-x");
  });

  it("should create image tags for pushes to main branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/heads/main",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:unstable");
  });

  it("should create image tags for pushes to stable branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/heads/stable",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:stable,foo:latest");
  });

  it("should create image tags for pushes to oldstable branch", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/heads/oldstable",
      stripTagPrefix: "v",
    });

    expect(imageTags).toEqual("foo:oldstable");
  });

  it("should create image tags for pushes to a branch with registry", () => {
    const imageTags = image.createImageTags({
      imageName: "foo",
      currentRef: "refs/heads/main",
      stripTagPrefix: "v",
      registry: "ghcr.io",
    });

    expect(imageTags).toEqual("ghcr.io/foo:unstable");
  });
});
