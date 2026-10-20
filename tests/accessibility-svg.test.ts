import { describe, expect, it } from "bun:test";
import { readFileSync } from "node:fs";

describe("Decorative SVG icons", () => {
  it("hides decorative SVGs in UI components from assistive technology", () => {
    for (const path of [
      "src/components/Icon.astro",
      "src/components/PixelIcon.astro",
      "src/components/PixelPlaybookActions.astro",
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
