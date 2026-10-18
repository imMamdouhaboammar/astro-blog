import type { CollectionEntry } from "astro:content";

export interface Category {
  slug: string;
  name: string;
  icon: string;
  color: string;
  description: string;
}

export const FALLBACK_CATEGORY: Category = {
  slug: "general",
  name: "عام",
  icon: "book",
  color: "#eef2f6",
  description: "بلاي بوكس ومقالات عامة متنوعة في البرمجيات والأنظمة والتقنية.",
};

export const CATEGORIES: readonly Category[] = [
  {
    slug: "api-web-development",
    name: "واجهات API وتطوير الويب",
    icon: "api",
    color: "#fbd7ec",
    description:
      "كيف تتواصل تطبيقات الويب؟ بلاي بوكس في تصميم الواجهات والبروتوكولات واختبارها.",
  },
  {
    slug: "real-world-case-studies",
    name: "دراسات حالة من الواقع",
    icon: "earth-planet",
    color: "#daddfc",
    description: "قراءة في القرارات التقنية التي تقف خلف المنتجات والخدمات.",
  },
  {
    slug: "ai-machine-learning",
    name: "الذكاء الاصطناعي وتعلّم الآلة",
    icon: "brain",
    color: "#b9f7ec",
    description: "من البيانات إلى النماذج: فهم عملي للمفاهيم الأساسية.",
  },
  {
    slug: "database-storage",
    name: "قواعد البيانات والتخزين",
    icon: "database",
    color: "#ffeca0",
    description: "كيف تُحفظ البيانات، وكيف تصل إليها التطبيقات بكفاءة؟",
  },
  {
    slug: "technical-interviews",
    name: "المقابلات التقنية",
    icon: "tower",
    color: "#edddfc",
    description: "بلاي بوكس للتفكير بصوت واضح وشرح الحلول أثناء المقابلات.",
  },
  {
    slug: "caching-performance",
    name: "التخزين المؤقت والأداء",
    icon: "order",
    color: "#fbd5d5",
    description: "فهم زمن الاستجابة والاختناقات وأماكن التخزين المؤقت.",
  },
  {
    slug: "payment-fintech",
    name: "المدفوعات والتقنية المالية",
    icon: "medal",
    color: "#cce6fc",
    description: "ماذا يحدث بين طلب الدفع وتأكيد العملية؟",
  },
  {
    slug: "software-architecture",
    name: "معمارية البرمجيات",
    icon: "image",
    color: "#d5efd0",
    description: "تنظيم أجزاء النظام واختيار الحدود المناسبة بينها.",
  },
  {
    slug: "devtools-productivity",
    name: "أدوات المطوّرين والإنتاجية",
    icon: "supplement-bottle",
    color: "#fce2bf",
    description: "أدوات وممارسات تخفّف العمل المتكرر وتوضّح المشكلات.",
  },
  {
    slug: "software-development",
    name: "تطوير البرمجيات",
    icon: "code",
    color: "#dce9fd",
    description: "من كتابة الشفرة إلى مراجعتها وصيانتها.",
  },
  {
    slug: "cloud-distributed-systems",
    name: "السحابة والأنظمة الموزّعة",
    icon: "cloud",
    color: "#eadffc",
    description: "أنظمة تعمل عبر أكثر من جهاز: الاتساق والاعتمادية والتوسّع.",
  },
  {
    slug: "how-it-works",
    name: "كيف تعمل الأشياء؟",
    icon: "question-mark",
    color: "#d1f3e5",
    description: "نظرة من الداخل على الخدمات التي نستخدمها كل يوم.",
  },
  {
    slug: "devops-cicd",
    name: "DevOps والتكامل المستمر",
    icon: "refresh",
    color: "#fbe0e7",
    description: "من تغيير صغير في الشفرة إلى إصدار يمكن الوثوق به.",
  },
  {
    slug: "security",
    name: "أمن المعلومات",
    icon: "lock",
    color: "#dbedfc",
    description: "مفاهيم تساعد على حماية الأنظمة والبيانات والمستخدمين.",
  },
  {
    slug: "computer-fundamentals",
    name: "أساسيات الحاسوب",
    icon: "laptop",
    color: "#f5edc9",
    description: "العمليات والذاكرة والشبكات، دون افتراض معرفة مسبقة.",
  },
  FALLBACK_CATEGORY,
] as const;

export const CATEGORY_SLUGS = CATEGORIES.map(c => c.slug);

export interface Playbook {
  id: string;
  slug: string;
  title: string;
  countText: string;
  image: string;
  icon: string;
  url: string;
}

export const PLAYBOOKS: readonly Playbook[] = [
  {
    id: "pymc-marketing",
    slug: "ai-machine-learning",
    title: "اتعلم PyMC Marketing بالعربي",
    countText: "6 بوستات",
    icon: "/icons/brain.png",
    image: "/assets/pymc-marketing/cover.jpeg",
    url: "/categories/ai-machine-learning/",
  },
];

export function getCategory(slug?: string): Category {
  if (!slug) return FALLBACK_CATEGORY;
  const match = CATEGORIES.find(c => c.slug === slug);
  return match ?? FALLBACK_CATEGORY;
}

export function getCategoryForPost(post: CollectionEntry<"blog">): Category {
  const rawCat = (post.data as { category?: string }).category;
  return getCategory(rawCat);
}

export function getCategoryPosts(
  posts: CollectionEntry<"blog">[],
  categorySlug: string
): CollectionEntry<"blog">[] {
  const targetCategory = getCategory(categorySlug);
  return posts.filter(
    post => getCategoryForPost(post).slug === targetCategory.slug
  );
}

export function getCategoriesWithCounts(
  posts: CollectionEntry<"blog">[]
): (Category & { count: number })[] {
  return CATEGORIES.map(category => {
    const matching = getCategoryPosts(posts, category.slug);
    return {
      ...category,
      count: matching.length,
    };
  });
}

export function categoryUrl(category: Pick<Category, "slug">): string {
  return `/categories/${category.slug}/`;
}

export function postUrl(post: Pick<CollectionEntry<"blog">, "slug">): string {
  return `/posts/${post.slug}/`;
}

export function getPostImage(
  post: CollectionEntry<"blog">
): string | undefined {
  const d = post.data as {
    heroImage?: string;
    seriesImage?: string;
    ogImage?: string | { src: string };
  };
  if (d.heroImage) return d.heroImage;
  if (d.seriesImage) return d.seriesImage;
  if (!d.ogImage) return undefined;
  return typeof d.ogImage === "string" ? d.ogImage : d.ogImage.src;
}

export function getPostSeriesImage(
  post: CollectionEntry<"blog">
): string | undefined {
  const d = post.data as {
    seriesImage?: string;
    heroImage?: string;
    ogImage?: string | { src: string };
  };
  if (d.seriesImage) return d.seriesImage;
  if (d.heroImage) return d.heroImage;
  if (!d.ogImage) return undefined;
  return typeof d.ogImage === "string" ? d.ogImage : d.ogImage.src;
}
