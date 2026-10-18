import { describe, expect, it } from "bun:test";
import postFilter from "../src/utils/postFilter";
import getSortedPosts from "../src/utils/getSortedPosts";
import {
  CATEGORIES,
  getCategoryForPost,
  postUrl,
  categoryUrl,
} from "../src/utils/categories";

describe("Routing and Content Collection Invariants", () => {
  const samplePosts = [
    {
      slug: "post-1",
      data: {
        title: "First Post",
        description: "First description",
        pubDatetime: new Date("2024-01-01"),
        draft: false,
        tags: ["web", "api"],
        category: "api-web-development",
      },
    },
    {
      slug: "post-2",
      data: {
        title: "Draft Post",
        description: "Draft description",
        pubDatetime: new Date("2024-01-02"),
        draft: true,
        tags: ["internal"],
      },
    },
    {
      slug: "post-3",
      data: {
        title: "General Post",
        description: "No explicit category",
        pubDatetime: new Date("2024-01-03"),
        draft: false,
        tags: ["general"],
      },
    },
  ] as any[];

  it("only exposes published, non-draft articles through postFilter", () => {
    const visible = samplePosts.filter(postFilter);
    expect(visible.length).toBe(2);
    expect(visible.some(p => p.data.draft === true)).toBe(false);
  });

  it("canonical post URLs always follow /posts/{slug}/ format without /guides/ prefix", () => {
    const visible = getSortedPosts(samplePosts);
    for (const post of visible) {
      const url = postUrl(post);
      expect(url).toBe(`/posts/${post.slug}/`);
      expect(url.startsWith("/guides/")).toBe(false);
    }
  });

  it("category URLs follow /categories/{slug}/ format", () => {
    for (const cat of CATEGORIES) {
      const url = categoryUrl(cat);
      expect(url).toBe(`/categories/${cat.slug}/`);
    }
  });

  it("every visible post resolves to a valid Category with fallback support", () => {
    const visible = getSortedPosts(samplePosts);
    const cat1 = getCategoryForPost(visible[0]);
    const cat2 = getCategoryForPost(visible[1]);

    expect(cat1.slug).toBe("general");
    expect(cat2.slug).toBe("api-web-development");
  });

  it("preserves article tags without overwriting them with category", () => {
    const visible = getSortedPosts(samplePosts);
    for (const post of visible) {
      expect(Array.isArray(post.data.tags)).toBe(true);
      expect(post.data.tags.length).toBeGreaterThan(0);
    }
  });
});
