import type { Site, SocialObjects } from "./types";

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

export const LOGO_IMAGE = {
  enable: false,
  svg: true,
  width: 216,
  height: 46,
};

export const SOCIALS: SocialObjects = [
  { name: "Github", href: "https://github.com/imMamdouhaboammar", linkTitle: "Mamdouh on GitHub", active: true },
  { name: "Facebook", href: "https://www.facebook.com/mamdouhboammar", linkTitle: "Mamdouh on Facebook", active: true },
  { name: "Instagram", href: "https://www.instagram.com/imMamdouhaboammar", linkTitle: "Mamdouh on Instagram", active: true },
  { name: "LinkedIn", href: "https://www.linkedin.com/in/mamdouh-aboammar/", linkTitle: "Mamdouh on LinkedIn", active: true },
  { name: "Twitter", href: "https://x.com/imMamdouh", linkTitle: "Mamdouh on X", active: true },
  { name: "WhatsApp", href: "https://wa.me/201092677269", linkTitle: "Mamdouh on WhatsApp", active: true },
  { name: "Mail", href: "mailto:Hello@mamdouhaboammar.com", linkTitle: "Email Mamdouh", active: true },
];
