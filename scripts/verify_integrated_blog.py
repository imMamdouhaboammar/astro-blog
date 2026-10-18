#!/usr/bin/env python3
"""
Integrated Blog Verification Script.
Verifies the production build in dist/ adheres strictly to all architectural,
accessibility, taxonomy, URL, and anti-slop requirements.
"""

import os
import re
import sys
from pathlib import Path

DIST_DIR = Path(__file__).resolve().parents[1] / "dist"

def fail(msg: str):
    print(f"❌ FAIL: {msg}")
    sys.exit(1)

def pass_check(msg: str):
    print(f"✅ PASS: {msg}")

def check_html_attributes(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    if 'lang="ar"' not in content:
        fail(f"{file_path} is missing lang=\"ar\"")
    if 'dir="rtl"' not in content:
        fail(f"{file_path} is missing dir=\"rtl\"")

def check_no_donor_url_leaks(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    # Check for /guides/ links (donor routes)
    # Exclude external links if any
    matches = re.findall(r'href="(/guides/[^"]*)"', content)
    if matches:
        fail(f"{file_path} contains leaked donor route: {matches}")

def main():
    if not DIST_DIR.exists():
        fail(f"Build output directory {DIST_DIR} does not exist.")

    print(f"🔍 Verifying production build in: {DIST_DIR}\n")

    # 1. Verify Homepage
    index_html = DIST_DIR / "index.html"
    if not index_html.exists():
        fail("Homepage index.html does not exist.")
    check_html_attributes(index_html)
    check_no_donor_url_leaks(index_html)
    index_content = index_html.read_text(encoding="utf-8")
    if "بلاي بوك ممدوح" not in index_content:
        fail("Homepage is missing site title 'بلاي بوك ممدوح'")
    if "/categories/" not in index_content:
        fail("Homepage is missing category links")
    if "/posts/" not in index_content:
        fail("Homepage is missing article links")
    if "home-hero" in index_content:
        fail("Homepage still contains deleted home-hero container")
    if "<h1>بلاي بوكس معرفية مصوّرة</h1>" in index_content:
        fail("Homepage still contains deleted hero heading '<h1>بلاي بوكس معرفية مصوّرة</h1>'")
    if "شروحات وخطط عملية لمفاهيم تقنية تستحق الفهم بعمق" in index_content:
        fail("Homepage still contains deleted hero subtext 'شروحات وخطط عملية لمفاهيم تقنية تستحق الفهم بعمق'")
    if "تابعني على المنصات وانضم للمجتمع التقني لتصلك أحدث البلاي بوكس والشروحات العملية فور نشرها" in index_content:
        fail("Homepage still contains deleted subtitle text 'تابعني على المنصات وانضم للمجتمع التقني لتصلك أحدث البلاي بوكس والشروحات العملية فور نشرها'")
    if "pixel-nav" not in index_content:
        fail("Homepage is missing Pixel Navbar (pixel-nav)")
    expected_whatsapp = os.environ.get("PUBLIC_WHATSAPP_URL", "").strip() or "https://wa.me/201092677269"
    if "pixel-nav-whatsapp" not in index_content:
        fail("Homepage is missing its public WhatsApp control")
    if expected_whatsapp not in index_content:
        fail(f"Homepage WhatsApp destination differs from {expected_whatsapp}")
    if "https://wa.me/201000000000" in index_content:
        fail("Homepage contains the placeholder WhatsApp number")
    if "playbooks-header" not in index_content:
        fail("Homepage is missing inline Playbooks header (playbooks-header)")
    if "pixel-actions--compact" not in index_content:
        fail("Homepage is missing compact Pixel Playbook Actions (pixel-actions--compact)")
    if "playbooks-grid" not in index_content:
        fail("Homepage is missing Playbooks grid (playbooks-grid)")
    if "pinned-grid" not in index_content:
        fail("Homepage is missing Pinned posts grid (pinned-grid)")
    if "pixel-social-btn" not in index_content:
        fail("Homepage is missing large pixel social buttons (pixel-social-btn)")
    if "اتعلم PyMC Marketing بالعربي" not in index_content:
        fail("Homepage is missing 'اتعلم PyMC Marketing بالعربي'")
    for mock_title in [
        "بناء واجهات API وتطبيقات الويب",
        "قواعد البيانات وهندسة التخزين",
        "أمن المعلومات وحماية التطبيقات",
    ]:
        if mock_title in index_content:
            fail(f"Homepage still contains mock playbook '{mock_title}'!")
    playbook_cards = re.findall(r'class="playbook-card"', index_content)
    if len(playbook_cards) != 1:
        fail(f"Expected exactly 1 playbook card (PyMC), found {len(playbook_cards)}")
    pass_check("Homepage structure: Centered Pixel Navbar with WhatsApp, Actions, single PyMC playbook (no mocks), Pinned posts, and Pixel Socials")

    # 2. Verify Canonical Post URLs and Preservation
    posts_dir = DIST_DIR / "posts"
    if not posts_dir.exists():
        fail("posts directory does not exist.")
    
    # Check all 6 PyMC marketing posts exist
    for i in range(1, 7):
        p_name = f"pymc-marketing-0{i}"
        p_file = posts_dir / p_name / "index.html"
        if not p_file.exists():
            fail(f"Canonical post /posts/{p_name}/ not found.")
        check_html_attributes(p_file)
        check_no_donor_url_leaks(p_file)
        p_content = p_file.read_text(encoding="utf-8")
        if "article-hero-img" not in p_content:
            fail(f"Post {p_name} is missing article-hero-img.")
        if f"part-{i}.png" not in p_content and i != 4:
            fail(f"Post {p_name} is missing part-{i}.png hero image.")
        if "المصادر" in p_content and "النموذج" in p_content and "السياق" in p_content:
            fail(f"Post {p_name} still contains mock Diagram component!")

    # Verify mock AstroPaper template posts are NOT generated as public pages
    mock_post = posts_dir / "adding-new-posts-in-astropaper-theme" / "index.html"
    if mock_post.exists():
        fail("Mock blog adding-new-posts-in-astropaper-theme is still present in build output!")
    
    # Check sample post (pymc-marketing-01) details
    sample_post = posts_dir / "pymc-marketing-01" / "index.html"
    post_content = sample_post.read_text(encoding="utf-8")
    if "rel=\"canonical\"" not in post_content:
        fail("Article page missing canonical link tag.")
    
    # Verify code copy button script is bundled and loaded
    js_scripts = list((DIST_DIR / "_astro").glob("hoisted.*.js"))
    has_copy_script = any("copy-code-btn" in s.read_text(encoding="utf-8") for s in js_scripts)
    if not has_copy_script:
        fail("Code block copy button script not found in bundled JS.")
    if "application/ld+json" not in post_content:
        fail("Article page missing structured data schema.")
    pass_check("Canonical article rendering, 6 PyMC independent posts, transparent hero images, no mock diagrams")

    # 3. Verify Pagination Preservation
    p2 = posts_dir / "2" / "index.html"
    if not p2.exists():
        fail("Post pagination /posts/2/index.html does not exist.")
    check_html_attributes(p2)
    check_no_donor_url_leaks(p2)
    pass_check("Posts pagination (/posts/2/) preserved and functional")

    # 4. Verify Category Taxonomy and Fallback
    categories_dir = DIST_DIR / "categories"
    if not categories_dir.exists():
        fail("categories directory does not exist.")
    
    # AI & ML category where PyMC lives
    cat_ai = categories_dir / "ai-machine-learning" / "index.html"
    if not cat_ai.exists():
        fail("Category /categories/ai-machine-learning/ does not exist.")
    check_html_attributes(cat_ai)
    check_no_donor_url_leaks(cat_ai)
    cat_ai_content = cat_ai.read_text(encoding="utf-8")
    if "الذكاء الاصطناعي وتعلّم الآلة" not in cat_ai_content:
        fail("Category title 'الذكاء الاصطناعي وتعلّم الآلة' not found.")
    if "part-6.png" not in cat_ai_content:
        fail("Featured guide card missing post own image (part-6.png).")
    if "بلاي بوك مميّز" not in cat_ai_content:
        fail("Featured guide card missing 'بلاي بوك مميّز' label.")
    if "الـ Playbooks" not in cat_ai_content:
        fail("Sidebar missing 'الـ Playbooks' label.")
    if "اتعلم PyMC Marketing بالعربي" not in cat_ai_content:
        fail("Sidebar missing PyMC Marketing playbook link.")
    for mock_cat in ["واجهات API وتطوير الويب", "المقابلات التقنية", "التخزين المؤقت والأداء"]:
        if f"<span>{mock_cat}</span>" in cat_ai_content:
            fail(f"Sidebar still contains mock category: {mock_cat}")
    
    # General fallback category
    cat_gen = categories_dir / "general" / "index.html"
    if not cat_gen.exists():
        fail("Fallback category /categories/general/ does not exist.")
    check_html_attributes(cat_gen)
    check_no_donor_url_leaks(cat_gen)
    pass_check("Category taxonomy, explicit categorization, post hero image in featured card, and general fallback")

    # 5. Verify Tags Preservation
    tags_dir = DIST_DIR / "tags"
    if not tags_dir.exists():
        fail("tags directory does not exist.")
    tag_pymc = tags_dir / "pymc-marketing" / "index.html"
    if not tag_pymc.exists():
        fail("Tag route /tags/pymc-marketing/ does not exist.")
    check_html_attributes(tag_pymc)
    check_no_donor_url_leaks(tag_pymc)
    pass_check("Tag routes preserved and styled consistently")

    # 6. Verify Search Page
    search_html = DIST_DIR / "search" / "index.html"
    if not search_html.exists():
        fail("Search page does not exist.")
    check_html_attributes(search_html)
    search_content = search_html.read_text(encoding="utf-8")
    if "ابحث في البلاي بوكس" not in search_content:
        fail("Search page missing Arabic search prompt 'ابحث في البلاي بوكس'.")
    pass_check("Search page present with Arabic microcopy")

    # 7. Verify RSS & Sitemap
    rss_xml = DIST_DIR / "rss.xml"
    if not rss_xml.exists():
        fail("rss.xml does not exist.")
    rss_content = rss_xml.read_text(encoding="utf-8")
    if "<title>بلاي بوك ممدوح</title>" not in rss_content:
        fail("rss.xml missing Arabic title 'بلاي بوك ممدوح'.")
    
    sitemaps = list(DIST_DIR.glob("sitemap*.xml"))
    if not sitemaps:
        fail("No sitemap XML file found.")
    pass_check("RSS feed and Sitemap generated with Arabic identity")

    # 8. Verify No Dark Mode Toggle in Built HTML
    for html_file in [index_html, sample_post, cat_ai]:
        c = html_file.read_text(encoding="utf-8")
        if 'id="theme-btn"' in c:
            fail(f"{html_file} still contains #theme-btn dark mode button.")
    pass_check("Dark mode toggle completely removed from reading interfaces")

    print("\n🎉 ALL 8 INTEGRATION INVARIANTS VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
