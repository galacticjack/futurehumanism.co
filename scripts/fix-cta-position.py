#!/usr/bin/env python3
"""
Move inline CTAs to appear later in articles (around 50% through content).
"""

import os
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / 'articles'

# The CTA we're looking for
CTA_MARKER = '<!-- Inline Newsletter CTA -->'

def fix_cta_position(filepath):
    """Move the CTA to appear later in the article."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if CTA_MARKER not in content:
        return False
    
    # Extract the CTA block
    cta_pattern = r'<!-- Inline Newsletter CTA -->.*?</div>\s*</div>\s*</div>'
    cta_match = re.search(cta_pattern, content, re.DOTALL)
    
    if not cta_match:
        # Try simpler pattern
        cta_pattern = r'<div class="inline-newsletter-cta"[^>]*>.*?</div>\s*</div>'
        cta_match = re.search(cta_pattern, content, re.DOTALL)
    
    if not cta_match:
        print(f"  Could not extract CTA from {filepath.name}")
        return False
    
    cta_html = cta_match.group(0)
    
    # Remove the CTA from its current position
    content_without_cta = content[:cta_match.start()] + content[cta_match.end():]
    
    # Find all </p> tags in the article content (after <article> tag if present)
    article_start = content_without_cta.find('<article')
    if article_start == -1:
        article_start = 0
    
    # Count paragraphs in article body
    article_content = content_without_cta[article_start:]
    p_tags = list(re.finditer(r'</p>', article_content))
    
    if len(p_tags) < 6:
        # Article too short, put at 50%
        target_p = max(2, len(p_tags) // 2)
    else:
        # Put after ~50% of paragraphs, minimum 6
        target_p = max(6, len(p_tags) // 2)
    
    if target_p >= len(p_tags):
        target_p = len(p_tags) - 1
    
    # Find the actual position in full content
    insert_position = article_start + p_tags[target_p].end()
    
    # Insert CTA at new position
    new_content = content_without_cta[:insert_position] + '\n\n        ' + cta_html + '\n' + content_without_cta[insert_position:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Moved CTA in {filepath.name} (now after paragraph {target_p + 1})")
    return True

def main():
    count = 0
    for filepath in ARTICLES_DIR.glob('*.html'):
        if filepath.name == '_TEMPLATE.html':
            continue
        if fix_cta_position(filepath):
            count += 1
    
    print(f"\n✅ Fixed CTA position in {count} articles")

if __name__ == '__main__':
    main()
