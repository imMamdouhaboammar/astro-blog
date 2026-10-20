export type Site = {
  website: string;
  author: string;
  desc: string;
  title: string;
  ogImage?: string;
  lightAndDarkMode?: boolean;
  postPerPage: number;
  scheduledPostMargin: number;
};

export type PixelIconName =
  | "home"
  | "facebook"
  | "linkedin"
  | "github"
  | "instagram"
  | "x"
  | "whatsapp"
  | "search";
