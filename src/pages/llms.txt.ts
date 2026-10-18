import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import getSortedPosts from "@utils/getSortedPosts";
import { postUrl } from "@utils/categories";
import postFilter from "@utils/postFilter";
import { SITE } from "@config";

export const GET: APIRoute = async () => {
  const posts = getSortedPosts((await getCollection("blog")).filter(postFilter));
  const lines = [
    `# ${SITE.title}`,
    "",
    `> ${SITE.desc}`,
    "",
    "المؤلف: ممدوح أبو عمّار (Mamdouh Aboammar)",
    "اللغة الأساسية: العربية",
    "",
    "## صفحات أساسية",
    `- [الرئيسية](${SITE.website})`,
    `- [عن المؤلف](${new URL("/about/", SITE.website).href})`,
    `- [الأرشيف](${new URL("/posts/", SITE.website).href})`,
    `- [RSS](${new URL("/rss.xml", SITE.website).href})`,
    "",
    "## المقالات المنشورة",
    ...posts.map(post =>
      `- [${post.data.title}](${new URL(postUrl(post), SITE.website).href}): ${post.data.description}`
    ),
    "",
    "المحتوى الكامل متاح على روابط المقالات أعلاه. هذا الملف فهرس وليس بديلًا عن النص الأصلي.",
  ];
  return new Response(lines.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
