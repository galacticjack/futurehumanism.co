#!/usr/bin/env python3
"""Move Next Story navigation to appear right before the CTA box"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

def fix_next_story_position(filepath):
    """Move next-story to before cta-box"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has both next-story and cta-box
    if 'class="next-story"' not in content:
        return False
    
    if 'class="cta-box"' not in content:
        return False
    
    # Extract the next-story block
    next_story_match = re.search(
        r'(\n\s*<!-- Next Story Navigation -->\s*\n\s*<a href="[^"]*" class="next-story">.*?</a>\s*\n)',
        content,
        re.DOTALL
    )
    
    if not next_story_match:
        return False
    
    next_story_html = next_story_match.group(1)
    
    # Remove it from current position
    content = content.replace(next_story_html, '\n')
    
    # Find the cta-box and insert before it
    cta_match = re.search(r'(\n\s*)(<div class="cta-box">)', content)
    
    if cta_match:
        insert_pos = cta_match.start(2)
        indent = cta_match.group(1)
        content = content[:insert_pos] + next_story_html.strip() + indent + content[insert_pos:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("Repositioning Next Story navigation...")
    
    fixed_count = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        if fix_next_story_position(filepath):
            print(f"  ✓ {filepath.name}")
            fixed_count += 1
    
    print(f"\n  Repositioned {fixed_count} articles")

if __name__ == '__main__':
    main()
