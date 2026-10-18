import { describe, expect, it } from "bun:test";
import { PROFILE, SOCIAL_CHANNELS } from "../src/utils/profile";

describe("Public author profile links", () => {
  it("uses the public Facebook and WhatsApp destinations, not template placeholders", () => {
    expect(PROFILE.social.facebook).toBe("https://www.facebook.com/mamdouhboammar");
    expect(PROFILE.social.whatsapp).toBe("https://wa.me/201092677269");
    expect(PROFILE.social.github).toBe("https://github.com/imMamdouhaboammar");
  });

  it("has valid HTTPS links for every displayed social channel", () => {
    for (const channel of SOCIAL_CHANNELS) {
      const value = PROFILE.social[channel.key];
      expect(new URL(value).protocol).toBe("https:");
      expect(value).not.toContain("satnaing");
    }
  });

  it("keeps an existing local portrait in the pixel art directory", () => {
    expect(PROFILE.avatar).toBe("/pixel-navbar/mamdouh-pixel.webp");
  });
});
