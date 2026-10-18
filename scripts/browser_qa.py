#!/usr/bin/env python3
"""Browser smoke tests against the built Arabic blog, including narrow RTL viewports."""

import os
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:4321").rstrip("/")
SCREENSHOTS = Path(os.getenv("BROWSER_QA_SCREENSHOTS", "test-artifacts/browser"))
ROUTES = ("/", "/search/", "/categories/ai-machine-learning/", "/posts/pymc-marketing-01/")


def wait_for_server():
    for _ in range(40):
        try:
            with urlopen(BASE_URL, timeout=2) as response:
                if response.status == 200:
                    return
        except (URLError, TimeoutError):
            time.sleep(1)
    raise AssertionError(f"Preview server did not become ready at {BASE_URL}")


def verify_viewport(page, width, route):
    assert page.locator("html").get_attribute("dir") == "rtl", f"{route}: not RTL"
    assert page.locator("#main").count() == 1, f"{route}: missing main content"
    assert page.locator(".pixel-nav-search").count() == 1, f"{route}: search unreachable"
    assert page.locator('a[href="/#login"]').count() == 0, "Broken login link is back"
    assert page.locator('a[href="https://wa.me/201000000000"]').count() == 0, "Placeholder WhatsApp link is back"
    actual = page.evaluate("document.documentElement.scrollWidth")
    assert actual <= width + 1, f"{route} at {width}px: horizontal overflow {actual}px"
    nav = page.locator(".pixel-nav-capsule").bounding_box()
    assert nav is not None and nav["x"] >= -1 and nav["x"] + nav["width"] <= width + 1, f"{route}: navbar clipped"
    for link in page.locator(".pixel-nav-capsule a").all():
        box = link.bounding_box()
        assert box is not None and box["x"] >= -1 and box["x"] + box["width"] <= width + 1, f"{route}: navigation link outside viewport"
        if width <= 375 and ("pixel-nav-icon" in (link.get_attribute("class") or "") or "pixel-nav-avatar" in (link.get_attribute("class") or "")):
            assert box["width"] >= 44 and box["height"] >= 44, f"{route}: small navigation touch target"


def main():
    wait_for_server()
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in (320, 375, 768, 1280):
                context = browser.new_context(viewport={"width": width, "height": 800}, locale="ar-EG")
                page = context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                for route in ROUTES:
                    response = page.goto(f"{BASE_URL}{route}", wait_until="networkidle")
                    assert response is not None and response.status == 200, f"{route}: expected 200, got {response.status if response else 'no response'}"
                    page.evaluate("document.fonts.ready")
                    verify_viewport(page, width, route)
                    if route == "/":
                        header = page.locator(".playbooks-header")
                        fits = header.evaluate("(el) => el.scrollWidth <= el.clientWidth + 1")
                        assert fits, f"Homepage action header overflows at {width}px"
                        page.screenshot(path=str(SCREENSHOTS / f"home-{width}.png"), full_page=True)
                    elif route.startswith("/posts/"):
                        page.screenshot(path=str(SCREENSHOTS / f"article-{width}.png"), full_page=True)
                assert "البحث" not in page.title(), "Post page should have the article title"
                page.goto(BASE_URL, wait_until="networkidle")
                assert page.locator(".playbook-card").count() > 0, "Home playbook is missing"
                page.locator(".pixel-nav-search").click()
                page.wait_for_url("**/search/")
                assert page.title().count("بلاي بوك ممدوح") == 1, "Duplicated site name in search title"
                search = page.locator('input[type="search"]')
                search.fill("PyMC")
                page.locator(".search-result-item").first.wait_for()
                assert page.locator(".search-result-item").count() >= 1, "Known published posts missing from search"
                search.fill("zz-nonexistent-topic-347120")
                assert page.locator(".search-empty").is_visible(), "No-results explanation is missing"
                search.fill("PyMC")
                page.locator(".search-result-item").first.wait_for()
                page.screenshot(path=str(SCREENSHOTS / f"search-{width}.png"), full_page=True)
                assert not errors, f"Browser console errors at {width}px: {errors}"
                print(f"PASS: RTL, navbar, search, category, article, overflow at {width}px")
                context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main()
