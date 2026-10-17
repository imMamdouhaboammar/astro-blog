import { describe, expect, it } from "bun:test";
import {
  CATEGORIES,
  FALLBACK_CATEGORY,
  PLAYBOOKS,
  getCategory,
  getCategoryForPost,
  getCategoryPosts,
  getCategoriesWithCounts,
} from "../src/utils/categories";

describe("Category Registry and Taxonomy", () => {
  it("defines 15 donor categories plus the fallback 'general' category", () => {
    expect(CATEGORIES.length).toBe(16);
    const slugs = CATEGORIES.map(c => c.slug);
    expect(slugs).toContain("api-web-development");
    expect(slugs).toContain("real-world-case-studies");
    expect(slugs).toContain("ai-machine-learning");
    expect(slugs).toContain("database-storage");
    expect(slugs).toContain("technical-interviews");
    expect(slugs).toContain("caching-performance");
    expect(slugs).toContain("payment-fintech");
    expect(slugs).toContain("software-architecture");
    expect(slugs).toContain("devtools-productivity");
    expect(slugs).toContain("software-development");
    expect(slugs).toContain("cloud-distributed-systems");
    expect(slugs).toContain("how-it-works");
    expect(slugs).toContain("devops-cicd");
    expect(slugs).toContain("security");
    expect(slugs).toContain("computer-fundamentals");
    expect(slugs).toContain("general");
  });

  it("provides 'general' with Arabic label 'عام' as fallback for missing or unknown category", () => {
    expect(FALLBACK_CATEGORY.slug).toBe("general");
    expect(FALLBACK_CATEGORY.name).toBe("عام");

    expect(getCategory(undefined)).toEqual(FALLBACK_CATEGORY);
    expect(getCategory("")).toEqual(FALLBACK_CATEGORY);
    expect(getCategory("unknown-random-slug")).toEqual(FALLBACK_CATEGORY);
    expect(getCategory("software-development").slug).toBe("software-development");
  });

  it("resolves category for posts with or without explicit category field", () => {
    const postWithCat = {
      slug: "post-1",
      data: { title: "P1", category: "devtools-productivity" },
    } as any;
    const postWithoutCat = {
      slug: "post-2",
      data: { title: "P2" },
    } as any;

    expect(getCategoryForPost(postWithCat).slug).toBe("devtools-productivity");
    expect(getCategoryForPost(postWithoutCat).slug).toBe("general");
  });

  it("calculates accurate post counts per category and filters posts", () => {
    const posts = [
      { slug: "p1", data: { title: "P1", category: "devtools-productivity" } },
      { slug: "p2", data: { title: "P2", category: "devtools-productivity" } },
      { slug: "p3", data: { title: "P3" } }, // fallback general
      { slug: "p4", data: { title: "P4", category: "software-development" } },
    ] as any;

    const counts = getCategoriesWithCounts(posts);
    const devtools = counts.find(c => c.slug === "devtools-productivity");
    const general = counts.find(c => c.slug === "general");
    const database = counts.find(c => c.slug === "database-storage");

    expect(devtools?.count).toBe(2);
    expect(general?.count).toBe(1);
    expect(database?.count).toBe(0);

    const devtoolsPosts = getCategoryPosts(posts, "devtools-productivity");
    expect(devtoolsPosts.map(p => p.slug)).toEqual(["p1", "p2"]);

    const generalPosts = getCategoryPosts(posts, "general");
    expect(generalPosts.map(p => p.slug)).toEqual(["p3"]);
  });

  it("exposes active PLAYBOOKS registry containing PyMC Marketing as the sole playbook", () => {
    expect(PLAYBOOKS.length).toBe(1);
    expect(PLAYBOOKS[0].id).toBe("pymc-marketing");
    expect(PLAYBOOKS[0].title).toBe("اتعلم PyMC Marketing بالعربي");
    expect(PLAYBOOKS[0].url).toBe("/categories/ai-machine-learning/");
    expect(PLAYBOOKS[0].icon).toBe("/icons/brain.png");
  });
});
