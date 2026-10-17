import { describe, expect, it } from "bun:test";
import postFilter from "../src/utils/postFilter";
import { SITE } from "../src/config";

describe("Post Filter and Visibility Invariant", () => {
  it("rejects draft posts unconditionally", () => {
    const draftPost = {
      slug: "draft-post",
      data: {
        title: "Draft Post",
        draft: true,
        pubDatetime: new Date(Date.now() - 100000),
      },
    } as any;

    expect(postFilter(draftPost)).toBe(false);
  });

  it("permits published posts with past publication dates", () => {
    const publishedPost = {
      slug: "published-post",
      data: {
        title: "Published Post",
        draft: false,
        pubDatetime: new Date(Date.now() - 3600000),
      },
    } as any;

    expect(postFilter(publishedPost)).toBe(true);
  });

  it("handles scheduled future posts correctly with respect to margin", () => {
    const futurePostFar = {
      slug: "future-far",
      data: {
        title: "Future Post",
        draft: false,
        pubDatetime: new Date(Date.now() + SITE.scheduledPostMargin + 3600000),
      },
    } as any;

    // In a test/prod environment where DEV is falsy or truthy:
    const isDev = Boolean(import.meta.env.DEV);
    if (!isDev) {
      expect(postFilter(futurePostFar)).toBe(false);
    }
  });
});
