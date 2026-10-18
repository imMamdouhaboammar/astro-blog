#!/usr/bin/env python3
"""Browser smoke tests against the built Arabic blog, including narrow RTL viewports."""

import json
import os
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:4321").rstrip("/")
SCREENSHOTS = Path(os.getenv("BROWSER_QA_SCREENSHOTS", "test-artifacts/browser"))
ROUTES = ("/", "/about/", "/search/", "/categories/ai-machine-learning/", "/posts/pymc-marketing-01/")


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
    assert page.locator(".editorial-footer").count() == 1, f"{route}: missing unified footer"
    assert page.locator('a[href="/about/"]').count() >= 1, f"{route}: About page undiscoverable"
    if route == "/about/":
        assert page.locator("main h1").count() == 1, "About page heading missing"
        assert page.locator(".about-portrait").is_visible(), "Profile portrait missing"
        assert page.locator(".about-post").count() > 0, "Selected posts missing"
        assert page.locator(".about-embed").count() >= 2, "Social embeds missing"
        assert page.locator(".about-embed-slot iframe").count() == 0, "Embeds loaded without consent"
        assert page.locator("[data-load-embed]").count() >= 2, "Embed controls are missing"
    if route.startswith("/posts/"):
        assert page.locator(".reading-index").count() == 1, "Article table of contents missing"
        assert page.locator(".reading-index a").count() >= 2, "Article lacks section links"
        for link in page.locator(".reading-index a").all():
            target_id = link.get_attribute("href")[1:]
            assert page.locator(f'[id="{target_id}"]').count() == 1, f"Broken reading anchor: {target_id}"
    json_ld = page.locator('script[type="application/ld+json"]').all_text_contents()
    assert json_ld, f"{route}: missing JSON-LD schema"
    for block in json_ld:
        try:
            schema = json.loads(block)
        except json.JSONDecodeError as error:
            raise AssertionError(f"{route}: malformed JSON-LD: {error}") from error
        assert isinstance(schema, dict) and schema.get("@context") == "https://schema.org", (
            f"{route}: invalid JSON-LD root or schema context"
        )
    if route == "/":
        heading = page.locator(".playbook-card .playbook-title").first
        assert heading.evaluate("(el) => el.tagName") == "H2", "Playbook heading skips level h2"

    for section in (".editorial-footer", ".about-page"):
        for link in page.locator(f'{section} a[target="_blank"]').all():
            accessible_warning = link.get_attribute("aria-label") or ""
            if link.locator(".sr-only").count():
                accessible_warning += " " + link.locator(".sr-only").all_text_contents()[0]
            assert "تبويب" in accessible_warning, f"{route}: new-tab link lacks screen-reader warning"

    if width == 1280:
        font_selector = ".footer-identity"
        if route == "/":
            font_selector = ".pixel-action"
        elif route == "/about/":
            font_selector = ".about-summary"
        original = page.locator(font_selector).first.evaluate(
            "(el) => parseFloat(getComputedStyle(el).fontSize)"
        )
        page.evaluate("document.documentElement.style.fontSize = '32px'")
        enlarged = page.locator(font_selector).first.evaluate(
            "(el) => parseFloat(getComputedStyle(el).fontSize)"
        )
        page.evaluate("document.documentElement.style.removeProperty('font-size')")
        assert enlarged >= original * 1.9, f"{route}: text does not respect larger root font size"

        page.emulate_media(reduced_motion="reduce")
        avatar = page.locator(".pixel-nav-avatar")
        assert avatar.evaluate("(el) => getComputedStyle(el).transitionDuration") == "0s", (
            f"{route}: navbar ignores reduced-motion preference"
        )
        avatar.hover()
        assert avatar.evaluate("(el) => getComputedStyle(el).transform") == "none", (
            f"{route}: navbar still moves on hover with reduced motion"
        )
        page.emulate_media(reduced_motion="no-preference")
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
                        if width >= 960 and page.locator(".playbooks-grid > .playbook-card").count() == 1:
                            card_width = page.locator(".playbook-card").first.bounding_box()["width"]
                            grid_width = page.locator(".playbooks-grid").bounding_box()["width"]
                            assert card_width >= grid_width * 0.8, "Single Playbook card leaves a large empty area"
                        assert page.locator(".pinned-thumb img").first.evaluate("(img) => img.complete && img.naturalWidth > 0"), "Pinned post icons failed to load"
                        if width <= 375:
                            compact = page.locator(".pixel-actions--compact .pixel-action").first.bounding_box()
                            assert compact is not None and compact["height"] >= 44, "Compact share button has an undersized touch target"
                        page.screenshot(path=str(SCREENSHOTS / f"home-{width}.png"), full_page=True)
                    elif route.startswith("/categories/"):
                        summary = page.locator(".category-disclosure summary")
                        expected_tabindex = "-1" if width > 960 else "0"
                        assert summary.get_attribute("tabindex") == expected_tabindex, "Sidebar disclosure is incorrectly keyboard focusable"
                    elif route == "/about/":
                        page.screenshot(path=str(SCREENSHOTS / f"about-{width}.png"), full_page=True)
                        if width == 1280:
                            page.route("https://www.linkedin.com/**", lambda req: req.abort())
                            page.locator("[data-load-embed]").first.click()
                            iframe = page.locator(".about-embed-slot iframe").first
                            assert iframe.count() == 1, "Social preview did not create an iframe on request"
                            assert (iframe.get_attribute("src") or "").startswith("https://www.linkedin.com/embed/"), "Untrusted embed origin"
                    elif route.startswith("/posts/"):
                        page.screenshot(path=str(SCREENSHOTS / f"article-{width}.png"), full_page=True)
                assert "البحث" not in page.title(), "Post page should have the article title"
                if width in (375, 1280):
                    response = page.goto(f"{BASE_URL}/posts/pymc-marketing-04/", wait_until="networkidle")
                    assert response is not None and response.status == 200, "Emoji regression article returned an error"
                    emoji = page.locator('.article-body p img[src^="data:image/"]').first
                    assert emoji.count() > 0, "Emoji image fixture is missing"
                    display = emoji.evaluate("(img) => getComputedStyle(img).display")
                    assert display == "inline-block", f"Inline emoji breaks prose: {display}"
                    assert emoji.bounding_box()["width"] <= 24, "Emoji appears as a large block illustration"
                page.goto(BASE_URL, wait_until="networkidle")
                assert page.locator(".playbook-card").count() > 0, "Home playbook is missing"
                page.locator(".pixel-nav-search").click()
                page.wait_for_url("**/search/")
                assert page.title().count("بلاي بوك ممدوح") == 1, "Duplicated site name in search title"
                # The search input is server-rendered; wait for React hydration before
                # interacting with the controlled field, or the first edit can be lost.
                islands = page.locator("astro-island")
                assert islands.count() >= 1, "Search component island is missing"
                page.locator("astro-island[ssr]").wait_for(state="detached", timeout=20000)
                search = page.locator('input[type="search"]')
                search.fill("PyMC")
                try:
                    page.locator(".search-result-item").first.wait_for(timeout=8000)
                except Exception:
                    print("SEARCH DIAGNOSTIC:", {
                        "url": page.url,
                        "input": search.input_value(),
                        "status": page.locator(".search-status").all_text_contents(),
                        "empty": page.locator(".search-empty").all_text_contents(),
                        "islands": page.locator("astro-island").count(),
                        "pageErrors": errors,
                        "scripts": page.locator('script[src]').evaluate_all("(els) => els.map(e => e.src)"),
                    }, flush=True)
                    page.screenshot(path=str(SCREENSHOTS / f"search-failed-{width}.png"), full_page=True)
                    raise
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
