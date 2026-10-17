#!/usr/bin/env python3
"""
Imports the PyMC-Marketing series into astro-blog/src/content/blog/
with proper frontmatter, category assignment, ogImages, and hero illustrations.
"""

import re
from pathlib import Path

SOURCE_DIR = Path("/Users/mamdouhaboammar/Downloads/arabic-guides/src/content/PyMC-Marketing")
DEST_DIR = Path("/Users/mamdouhaboammar/Downloads/astro-blog/src/content/blog")

POST_CONFIG = {
    "pymc-marketing-01.md": {
        "pubDatetime": "2026-10-17T16:30:00Z",
        "featured": True,
        "ogImage": "/assets/pymc-marketing/cover.jpeg",
        "heroImage": "/assets/pymc-marketing/cover.jpeg",
        "heroAlt": "PyMC Marketing - رحلة مع Marketing Science",
    },
    "pymc-marketing-02.md": {
        "pubDatetime": "2026-10-17T16:31:00Z",
        "featured": False,
        "ogImage": "/assets/pymc-marketing/part-2.png",
        "heroImage": "/assets/pymc-marketing/part-2.png",
        "heroAlt": "Looking beyond the dashboard",
    },
    "pymc-marketing-03.md": {
        "pubDatetime": "2026-10-17T16:32:00Z",
        "featured": False,
        "ogImage": "/assets/pymc-marketing/part-3.png",
        "heroImage": "/assets/pymc-marketing/part-3.png",
        "heroAlt": "Pixel mascot checks probabilities before the gate",
    },
    "pymc-marketing-04.md": {
        "pubDatetime": "2026-10-17T16:33:00Z",
        "featured": False,
        "ogImage": "/assets/pymc-marketing/part-4.png",
        "heroImage": "/assets/pymc-marketing/part-4.png",
        "heroAlt": "Orange Pixel Math Tool Bridge & Contract Drift",
    },
    "pymc-marketing-05.md": {
        "pubDatetime": "2026-10-17T16:34:00Z",
        "featured": False,
        "ogImage": "/assets/pymc-marketing/part-5.png",
        "heroImage": "/assets/pymc-marketing/part-5.png",
        "heroAlt": "Pixel mascot explains smarter budget choices",
    },
    "pymc-marketing-06.md": {
        "pubDatetime": "2026-10-17T16:35:00Z",
        "featured": False,
        "ogImage": "/assets/pymc-marketing/part-6.png",
        "heroImage": "/assets/pymc-marketing/part-6.png",
        "heroAlt": "Mascot compares twin warning boxes",
    },
}

def process_file(filename: str):
    src_file = SOURCE_DIR / filename
    dest_file = DEST_DIR / filename
    
    cfg = POST_CONFIG[filename]
    content = src_file.read_text(encoding="utf-8")
    
    # Split frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid frontmatter in {filename}")
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Update frontmatter fields
    frontmatter = re.sub(r'draft:\s*true', 'draft: false', frontmatter)
    frontmatter = re.sub(r'pubDatetime:.*', f'pubDatetime: {cfg["pubDatetime"]}', frontmatter)
    
    # Add category and ogImage and featured
    additions = [
        f'category: "ai-machine-learning"',
        f'featured: {"true" if cfg["featured"] else "false"}',
        f'ogImage: "{cfg["ogImage"]}"',
    ]
    
    frontmatter = frontmatter.rstrip() + "\n" + "\n".join(additions) + "\n"
    
    # Add hero image to top of body if not present
    hero_md = f"\n\n![{cfg['heroAlt']}]({cfg['heroImage']})\n\n"
    body = hero_md + body.lstrip()
    
    # If part 4, also embed part-7 (connector mismatch) where contract drift is explained
    if filename == "pymc-marketing-04.md":
        target = "وبعد الحنكشة دي كلها، طلع عندي **Public Contract**"
        replacement = "![Pixel mascot spots a connector mismatch](/assets/pymc-marketing/part-7.png)\n\nوبعد الحنكشة دي كلها، طلع عندي **Public Contract**"
        body = body.replace(target, replacement)
    
    new_content = f"---{frontmatter}---{body}"
    dest_file.write_text(new_content, encoding="utf-8")
    print(f"✅ Imported {filename} -> {dest_file.relative_to(DEST_DIR.parent)}")

def main():
    print("🚀 Importing PyMC Marketing guides...")
    for filename in sorted(POST_CONFIG.keys()):
        process_file(filename)
    print("🎉 All 6 PyMC Marketing guides imported successfully!")

if __name__ == "__main__":
    main()
