import { describe, expect, it } from "bun:test";
import { readFileSync } from "node:fs";

describe("Decorative legacy SVG icons", () => {
  it("hides decorative SVGs in named controls and tag links from assistive technology", () => {
    for (const path of [
      "src/components/Header.astro",
      "src/components/Pagination.astro",
      "src/components/Tag.astro",
    ]) {
      const source = readFileSync(path, "utf8");
      const svgTags = [...source.matchAll(/<svg\b[^>]*>/gs)].map(match => match[0]);
      expect(svgTags.length).toBeGreaterThan(0);
      for (const openingTag of svgTags) {
        expect(openingTag).toMatch(/aria-hidden=["']true["']/);
      }
    }
  });
});
