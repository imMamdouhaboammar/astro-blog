#!/usr/bin/env python3
"""
Imports the PyMC-Marketing series into astro-blog/src/content/blog/
with proper frontmatter, category assignment, ogImages, and hero illustrations.
"""

import argparse
import re
from pathlib import Path

DEST_DIR = Path(__file__).resolve().parents[1] / "src" / "content" / "blog"

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

def process_file(filename: str, source_dir: Path):
    src_file = source_dir / filename
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
        f'heroImage: "{cfg["heroImage"]}"',
    ]
    
    frontmatter = frontmatter.rstrip() + "\n" + "\n".join(additions) + "\n"
    
    # The page layout renders heroImage; avoid duplicating it in Markdown.
    body = body.lstrip()
    first_line = body.splitlines()[0] if body else ""
    if first_line.startswith("![") and first_line.endswith(f"]({cfg['heroImage']})"):
        body = body[len(first_line):].lstrip()
    
    # If part 4, also embed part-7 (connector mismatch) where contract drift is explained
    if filename == "pymc-marketing-04.md":
        target = "وبعد الحنكشة دي كلها، طلع عندي **Public Contract**"
        replacement = "![Pixel mascot spots a connector mismatch](/assets/pymc-marketing/part-7.png)\n\nوبعد الحنكشة دي كلها، طلع عندي **Public Contract**"
        body = body.replace(target, replacement)
    
    new_content = f"---{frontmatter}---{body}"
    dest_file.write_text(new_content, encoding="utf-8")
    print(f"✅ Imported {filename} -> {dest_file.relative_to(DEST_DIR.parent)}")

def main():
    parser = argparse.ArgumentParser(description="Import PyMC guides into this checkout")
    parser.add_argument("source_dir", type=Path, help="Directory containing six source Markdown files")
    args = parser.parse_args()
    source_dir = args.source_dir.expanduser().resolve()
    if not source_dir.is_dir():
        parser.error(f"Source directory does not exist: {source_dir}")
    for filename in POST_CONFIG:
        if not (source_dir / filename).is_file():
            parser.error(f"Missing source: {source_dir / filename}")
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    print("🚀 Importing PyMC Marketing guides...")
    for filename in sorted(POST_CONFIG.keys()):
        process_file(filename, source_dir)
    print("🎉 All 6 PyMC Marketing guides imported successfully!")

if __name__ == "__main__":
    main()
