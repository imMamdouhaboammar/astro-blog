import { describe, expect, it } from "bun:test";
import { formatPageTitle } from "../src/utils/formatPageTitle";

describe("page titles and social metadata", () => {
  const site = "بلاي بوك ممدوح";
  it("keeps the home title once", () => {
    expect(formatPageTitle(site, site)).toBe(site);
  });
  it("appends the site title to simple page titles", () => {
    expect(formatPageTitle("البحث", site)).toBe("البحث | بلاي بوك ممدوح");
  });
  it("does not append the same suffix twice", () => {
    expect(formatPageTitle("البحث | بلاي بوك ممدوح", site)).toBe("البحث | بلاي بوك ممدوح");
  });
  it("does not mistake other positions for a suffix", () => {
    expect(formatPageTitle("بلاي بوك ممدوح | موضوع", site)).toBe("بلاي بوك ممدوح | موضوع | بلاي بوك ممدوح");
  });
});
