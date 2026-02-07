#!/usr/bin/env python3
"""Tighten vertical spacing in article files"""

import re
from pathlib import Path

articles_dir = Path(__file__).parent.parent / "articles"

def tighten_spacing(filepath):
    """Reduce excessive margins and padding"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Author bio: margin 48px -> 24px
    content = re.sub(
        r'(\.author-bio\s*\{[^}]*margin:\s*)48px(\s*0)',
        r'\g<1>24px\2',
        content
    )
    
    # Related articles: margin 60px -> 32px
    content = re.sub(
        r'(\.related-articles\s*\{[^}]*margin:\s*)60px(\s*auto)',
        r'\g<1>32px\2',
        content
    )
    
    # Related articles h3: margin-bottom 32px -> 16px
    content = re.sub(
        r'(\.related-articles h3\s*\{[^}]*margin-bottom:\s*)32px',
        r'\g<1>16px',
        content
    )
    
    # Article padding: 60px -> 40px
    content = re.sub(
        r'(article\s*\{[^}]*padding:\s*)60px(\s+24px)',
        r'\g<1>40px\2',
        content
    )
    
    # Share section margin: 48px -> 24px
    content = re.sub(
        r'(\.share-section\s*\{[^}]*margin:\s*)48px(\s*0)',
        r'\g<1>24px\2',
        content
    )
    
    # Callout margin: 32px -> 20px
    content = re.sub(
        r'(\.callout\s*\{[^}]*margin:\s*)32px(\s*0)',
        r'\g<1>20px\2',
        content
    )
    
    # h2 margin-top: 48px -> 32px
    content = re.sub(
        r'(article h2\s*\{[^}]*margin:\s*)48px(\s+0\s+20px)',
        r'\g<1>32px\2',
        content
    )
    
    # Mobile author-bio padding: 24px -> 20px (if present)
    # Mobile related-articles margin (if separate rule exists)
    content = re.sub(
        r'(@media[^{]*\{[^}]*\.related-articles\s*\{[^}]*margin:\s*)48px',
        r'\g<1>24px',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed_count = 0
    
    for filepath in sorted(articles_dir.glob('*.html')):
        if filepath.name.startswith('_'):
            continue
        
        if tighten_spacing(filepath):
            print(f"  Tightened: {filepath.name}")
            fixed_count += 1
    
    print(f"\nUpdated {fixed_count} articles")

if __name__ == '__main__':
    main()
