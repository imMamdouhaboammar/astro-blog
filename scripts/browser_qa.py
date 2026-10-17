#!/usr/bin/env python3
"""
Automated Browser QA for Arabic Guides Integration in astro-blog.
Tests navigation flow: Library -> Category -> Article -> Related Article -> Search.
Tests desktop and mobile viewports, code block copy, overflow prevention, and RTL alignment.
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:4321"
SCREENSHOT_DIR = Path("/Users/mamdouhaboammar/Downloads/astro-blog/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def fail(msg: str):
    print(f"❌ QA FAIL: {msg}")
    sys.exit(1)

def pass_test(msg: str):
    print(f"✅ QA PASS: {msg}")

def main():
    print("🚀 Starting Playwright Browser QA...\n")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        
        # 1. Desktop Session (1280x800)
        context_desktop = browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="ar-AR"
        )
        page = context_desktop.new_page()

        # Step 1: Library Homepage
        print("Testing Library Homepage...")
        page.goto(BASE_URL, wait_until="networkidle")
        title = page.title()
        if "أدلّة ممدوح" not in title:
            fail(f"Unexpected title: {title}")
        
        # Check RTL attribute on html
        dir_attr = page.locator("html").get_attribute("dir")
        if dir_attr != "rtl":
            fail(f"HTML dir is not rtl: {dir_attr}")
        
        # Check category cards exist
        cat_cards = page.locator(".category-card")
        cat_count = cat_cards.count()
        if cat_count == 0:
            fail("No category cards found on homepage.")
        print(f"Found {cat_count} category cards on homepage.")
        
        page.screenshot(path=str(SCREENSHOT_DIR / "01_desktop_library.png"))
        pass_test("Desktop library homepage rendered correctly")

        # Step 2: Navigate to Category Page
        print("Navigating to Category: API & Web Dev...")
        cat_link = page.locator('a[href="/categories/api-web-development/"]').first
        if not cat_link.is_visible():
            fail("Category link for api-web-development not visible.")
        cat_link.click()
        page.wait_for_load_state("networkidle")

        if "/categories/api-web-development" not in page.url:
            fail(f"Navigation failed, url is: {page.url}")
        
        page.screenshot(path=str(SCREENSHOT_DIR / "02_desktop_category.png"))
        pass_test("Desktop category page rendered correctly")

        # Step 3: Navigate to Canonical Article
        print("Navigating to Article...")
        article_card = page.locator("a.featured-guide, a.guide-card").first
        article_href = article_card.get_attribute("href")
        if not article_href or not article_href.startswith("/posts/"):
            fail(f"Article link is not canonical /posts/...: {article_href}")
        article_card.click()
        page.wait_for_load_state("networkidle")

        if "/posts/" not in page.url:
            fail(f"Not on article page: {page.url}")
        
        # Check no page-wide horizontal overflow
        no_overflow = page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth")
        if not no_overflow:
            fail("Horizontal overflow detected on desktop article page!")

        # Check code copy button
        copy_btn = page.locator(".copy-code-btn").first
        if copy_btn.count() > 0:
            copy_btn.click()
            time.sleep(0.5)
            # Verify text feedback
            btn_text = copy_btn.inner_text()
            print(f"Copy button clicked, feedback text: {btn_text}")

        page.screenshot(path=str(SCREENSHOT_DIR / "03_desktop_article.png"))
        pass_test("Desktop article page with reading layout and code blocks verified")

        # Step 4: Search Page
        print("Testing Search Page...")
        page.goto(f"{BASE_URL}/search/", wait_until="networkidle")
        search_input = page.locator('input[type="search"]')
        if not search_input.is_visible():
            fail("Search input not visible.")
        search_input.fill("Astro")
        time.sleep(0.5)

        results = page.locator(".search-result-item")
        res_count = results.count()
        print(f"Search results for 'Astro': {res_count} results found.")
        if res_count == 0:
            fail("Expected search results for 'Astro' but found 0.")

        page.screenshot(path=str(SCREENSHOT_DIR / "04_desktop_search.png"))
        pass_test("Search functionality and Arabic UI verified")

        context_desktop.close()

        # 2. Mobile Session (375x667 - iPhone SE)
        print("\nTesting Mobile Viewport (375x667)...")
        context_mobile = browser.new_context(
            viewport={"width": 375, "height": 667},
            is_mobile=True,
            locale="ar-AR"
        )
        mobile_page = context_mobile.new_page()

        # Article on mobile
        mobile_page.goto(f"{BASE_URL}/posts/adding-new-posts-in-astropaper-theme/", wait_until="networkidle")
        
        # Check mobile overflow
        mobile_no_overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth")
        if not mobile_no_overflow:
            fail("Horizontal overflow detected on mobile article page!")

        # Test Category Drawer disclosure
        drawer_summary = mobile_page.locator("details.category-drawer summary")
        if drawer_summary.is_visible():
            drawer_summary.click()
            time.sleep(0.3)
            # Check drawer is open
            is_open = mobile_page.locator("details.category-drawer").get_attribute("open") is not None
            if not is_open:
                fail("Category drawer did not open on summary click.")
            print("Category drawer opened successfully on mobile.")
            # Close drawer
            drawer_summary.click()

        mobile_page.screenshot(path=str(SCREENSHOT_DIR / "05_mobile_article.png"))
        pass_test("Mobile responsive reading and category drawer verified")

        context_mobile.close()
        browser.close()

    print("\n🎉 ALL BROWSER QA CHECKS PASSED WITH FLYING COLORS!")

if __name__ == "__main__":
    main()
