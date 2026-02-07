#!/usr/bin/env python3
"""
Remove duplicate sticky CTA bars from articles.
Keep only the LAST occurrence of the sticky bar (the one at the very end).
"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

def fix_duplicates(filepath):
    """Remove first occurrence of duplicate sticky CTA, keep the last one"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern for the complete sticky CTA section (CSS + HTML + JS)
    # We want to find if there are TWO of these and remove the first one
    
    # Count occurrences of the sticky bar HTML
    sticky_divs = list(re.finditer(r'<div class="sticky-cta-bar" id="stickyCta">', content))
    
    if len(sticky_divs) >= 2:
        # Find the FIRST complete sticky section and remove it
        # The section starts with <style> containing .sticky-cta-bar and ends after the </script> for that component
        
        # Find the first sticky-cta-bar style block and remove everything from there to just before the second one
        first_style_start = content.find('<style>\n.sticky-cta-bar {')
        if first_style_start == -1:
            first_style_start = content.find('<style>\r\n.sticky-cta-bar {')
        
        if first_style_start != -1:
            # Find where the second sticky-cta-bar style starts
            second_style_start = content.find('<style>\n.sticky-cta-bar {', first_style_start + 100)
            if second_style_start == -1:
                second_style_start = content.find('<style>\r\n.sticky-cta-bar {', first_style_start + 100)
            
            if second_style_start != -1:
                # Remove from first_style_start to second_style_start
                content = content[:first_style_start] + content[second_style_start:]
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("Removing duplicate sticky CTA bars...")
    
    fixed = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        if fix_duplicates(filepath):
            print(f"  ✓ {filepath.name}")
            fixed += 1
    
    print(f"\nFixed {fixed} articles")

if __name__ == '__main__':
    main()
