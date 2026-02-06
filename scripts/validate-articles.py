#!/usr/bin/env python3
"""
Validate all articles have consistent template elements.
Run this on every deploy to catch inconsistencies early.
"""

import re
import sys
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"
IMAGES_DIR = Path(__file__).parent.parent / "images"

REQUIRED_ELEMENTS = [
    ('GA4 tag', r'gtag.*G-W0SQN4JHN2'),
    ('twitter:card', r'twitter:card.*summary_large_image'),
    ('twitter:image', r'twitter:image'),
    ('og:image', r'og:image'),
    ('favicon', r'favicon'),
    ('logo-icon', r'logo-icon'),
    ('hero background image', r"url\(['\"]?https://images\.unsplash\.com"),
    ('share buttons', r'share-btn'),
    ('author bio', r'author-bio'),
    ('accent color #1E90FF', r'#1E90FF|--accent.*1E90FF'),
]

def validate_article(filepath):
    """Check article has all required elements"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    slug = filepath.stem
    
    # Check required elements
    for name, pattern in REQUIRED_ELEMENTS:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Missing: {name}")
    
    # Check OG image file exists
    og_image = IMAGES_DIR / f"og-{slug}.jpg"
    if not og_image.exists():
        issues.append(f"Missing OG image: og-{slug}.jpg")
    
    # Check for old accent colors
    if re.search(r'#6366F1|#ec4899', content, re.IGNORECASE):
        issues.append("Has old accent color (should be #1E90FF)")
    
    # Check for emojis in content (excluding schema)
    content_no_schema = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    if re.search(r'[\U0001F300-\U0001F9FF]', content_no_schema):
        issues.append("Contains emojis (not allowed)")
    
    return issues

def main():
    print("Validating articles...\n")
    
    all_valid = True
    
    for filepath in sorted(ARTICLES_DIR.glob("*.html")):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        issues = validate_article(filepath)
        
        if issues:
            all_valid = False
            print(f"❌ {filepath.name}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✓ {filepath.name}")
    
    print()
    if all_valid:
        print("All articles valid!")
        return 0
    else:
        print("Some articles have issues - fix before deploying!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
