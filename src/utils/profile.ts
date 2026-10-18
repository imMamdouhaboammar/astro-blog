/** Single source of truth for public profile and contact links. */
export const PROFILE = {
  name: "ممدوح أبو عمّار",
  englishName: "Mamdouh Aboammar",
  role: "Digital Director · Growth & AI Product Building",
  avatar: "/pixel-navbar/mamdouh-pixel.webp",
  email: "Hello@mamdouhaboammar.com",
  website: "https://mamdouhaboammar.com/",
  social: {
    facebook: "https://www.facebook.com/mamdouhboammar",
    linkedin: "https://www.linkedin.com/in/mamdouh-aboammar/",
    github: "https://github.com/imMamdouhaboammar",
    instagram: "https://www.instagram.com/imMamdouhaboammar",
    x: "https://x.com/imMamdouh",
    whatsapp: "https://wa.me/201092677269",
  },
} as const;

export const SOCIAL_CHANNELS = [
  { key: "linkedin", title: "LinkedIn", description: "تحليل ونقاشات عن التسويق والنمو والمنتجات" },
  { key: "facebook", title: "Facebook", description: "أفكار وتجارب من يوميات الشغل" },
  { key: "github", title: "GitHub", description: "المشاريع والأدوات مفتوحة المصدر" },
  { key: "x", title: "X", description: "ملاحظات وأفكار قصيرة" },
] as const;
