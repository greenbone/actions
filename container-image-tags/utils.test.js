const utils = require("./utils");

describe("getBranchName", () => {
  it("should return a branch name from a ref", () => {
    expect(utils.getBranchName("refs/heads/foo")).toEqual("foo");
  });

  it("should ignore other non refs", () => {
    expect(utils.getBranchName("foo")).toEqual("foo");
  });

  it("should return empty string by default", () => {
    expect(utils.getBranchName()).toEqual("");
    expect(utils.getBranchName(null)).toEqual("");
  });
});

describe("getTagName", () => {
  it("should return a tag name from a ref", () => {
    expect(utils.getTagName("refs/tags/foo")).toEqual("foo");
    expect(utils.getTagName("refs/tags/1.2.3")).toEqual("1.2.3");
  });

  it("should ignore other non refs", () => {
    expect(utils.getTagName("foo")).toEqual("foo");
  });

  it("should return empty string by default", () => {
    expect(utils.getTagName()).toEqual("");
    expect(utils.getTagName(null)).toEqual("");
  });

  it("should strip tag prefixes", () => {
    expect(utils.getTagName("refs/tags/vfoo", "v")).toEqual("foo");
    expect(utils.getTagName("refs/tags/v1.2.3", "v")).toEqual("1.2.3");
    expect(utils.getTagName("refs/tags/bar1.2.3", "bar")).toEqual("1.2.3");
  });
});

describe("isTag", () => {
  it("should detect tags from ref", () => {
    expect(utils.isTag("refs/tags/v1.2.3")).toEqual(true);
    expect(utils.isTag("refs/tags/1.2.3")).toEqual(true);
    expect(utils.isTag("refs/tags/foo")).toEqual(true);
  });

  it("should return false for non tag refs", () => {
    expect(utils.isTag("refs/heads/foo")).toEqual(false);
  });
});
