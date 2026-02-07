#!/usr/bin/env python3
"""Fix article link and emphasis colors - make them more readable"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

# CSS fixes to add
LINK_CSS_FIX = """
        /* Article link styling - subtle, readable */
        article a {
            color: #60a5fa;
            text-decoration: underline;
            text-decoration-color: rgba(96, 165, 250, 0.3);
            text-underline-offset: 2px;
        }
        article a:hover {
            color: #93c5fd;
            text-decoration-color: rgba(96, 165, 250, 0.6);
        }
        article a:visited {
            color: #a78bfa;
        }
"""

def fix_article(filepath):
    """Fix link colors in article"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already fixed
    if 'article a {' in content and 'text-underline-offset' in content:
        return False
    
    # Fix em color - change from accent to just italic
    content = re.sub(
        r'article em \{\s*color: var\(--accent\);\s*font-style: normal;\s*\}',
        'article em {\n            font-style: italic;\n            color: var(--text-primary);\n        }',
        content
    )
    
    # Add link styling after article strong rule
    if 'article strong {' in content and 'article a {' not in content:
        content = re.sub(
            r'(article strong \{[^}]+\})',
            r'\1' + LINK_CSS_FIX,
            content
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("Fixing article link and emphasis colors...")
    
    fixed_count = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        if fix_article(filepath):
            print(f"  ✓ {filepath.name}")
            fixed_count += 1
    
    print(f"\n  Fixed {fixed_count} articles")

if __name__ == '__main__':
    main()
