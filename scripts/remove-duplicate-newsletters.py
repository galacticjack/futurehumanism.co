#!/usr/bin/env python3
"""
Remove duplicate newsletter sections from articles.
Keep ONLY the sticky bottom bar, remove inline newsletter CTAs.
"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

def clean_article(filepath):
    """Remove duplicate newsletter sections"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # Remove inline newsletter CTAs (keep only the sticky bar)
    # These appear mid-article and are the duplicates
    content = re.sub(
        r'<div class="inline-newsletter-cta"[^>]*>.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove standalone inline newsletter
    content = re.sub(
        r'<div class="inline-newsletter"[^>]*>.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Clean up any resulting extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if len(content) != original_len:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("Removing duplicate newsletter sections...")
    
    cleaned = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        if clean_article(filepath):
            print(f"  ✓ {filepath.name}")
            cleaned += 1
    
    print(f"\nCleaned {cleaned} articles")

if __name__ == '__main__':
    main()
