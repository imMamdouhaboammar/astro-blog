import type { Site } from "./types";

export const SITE: Site = {
  website: "https://astro-blog.pages.dev/",
  author: "Mamdouh Aboammar",
  desc: "بلاي بوكس عربية مصوّرة في البرمجيات والأنظمة والذكاء الاصطناعي.",
  title: "بلاي بوك ممدوح",
  ogImage: "/og.png",
  lightAndDarkMode: false,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
};

export const LOCALE = {
  lang: "ar", // html lang code. Set this empty and default will be "en"
  langTag: ["ar-AR"], // BCP 47 Language Tags. Set this empty [] to use the environment default
} as const;
