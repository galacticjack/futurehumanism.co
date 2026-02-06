#!/usr/bin/env python3
"""
Add inline newsletter CTA to all articles.
Inserts after the 3rd <p> tag in the main content area.
Skips if CTA already exists.
"""

import os
import re
from pathlib import Path

# The inline CTA HTML
INLINE_CTA = '''
        <!-- Inline Newsletter CTA -->
        <div class="inline-newsletter-cta" style="margin: 48px 0; padding: 32px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; border: 1px solid rgba(30, 144, 255, 0.3); text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 12px;">🚀</div>
            <h3 style="color: #ffffff; font-size: 1.4rem; font-weight: 700; margin-bottom: 8px;">Want more like this?</h3>
            <p style="color: #b0b0b0; font-size: 1rem; margin-bottom: 20px; max-width: 400px; margin-left: auto; margin-right: auto;">Join 2,000+ builders getting weekly AI insights, tools, and unfiltered takes. No spam, unsubscribe anytime.</p>
            <form action="https://app.beehiiv.com/forms/c7d45ea8-9b86-4677-8bd0-9e3b37e0b1c7/subscribe" method="POST" target="_blank" style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; max-width: 450px; margin: 0 auto;">
                <input type="email" name="email" placeholder="your@email.com" required style="padding: 14px 20px; border-radius: 8px; border: 1px solid #2a2a2a; background: #0a0a0a; color: #ffffff; font-size: 1rem; flex: 1; min-width: 200px;">
                <button type="submit" style="padding: 14px 28px; border-radius: 8px; border: none; background: #1E90FF; color: white; font-weight: 600; font-size: 1rem; cursor: pointer; transition: all 0.2s; white-space: nowrap;">Subscribe Free</button>
            </form>
            <p style="color: #707070; font-size: 0.85rem; margin-top: 16px;">Read by developers, founders, and AI enthusiasts</p>
        </div>
'''

def add_cta_to_article(filepath):
    """Add inline CTA after the 3rd paragraph in an article."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has inline CTA
    if 'inline-newsletter-cta' in content:
        print(f"  SKIP (already has CTA): {filepath.name}")
        return False
    
    # Skip template
    if filepath.name == '_TEMPLATE.html':
        print(f"  SKIP (template): {filepath.name}")
        return False
    
    # Find the article content area - look for <article> or main content section
    # We'll insert after the 3rd </p> tag that's inside the content area
    
    # Find all </p> tags
    p_tags = list(re.finditer(r'</p>', content))
    
    if len(p_tags) < 4:
        print(f"  SKIP (too short - {len(p_tags)} paragraphs): {filepath.name}")
        return False
    
    # Insert after the 4th </p> tag (giving readers 4 paragraphs first)
    insert_position = p_tags[3].end()
    
    # Insert the CTA
    new_content = content[:insert_position] + INLINE_CTA + content[insert_position:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ADDED CTA: {filepath.name}")
    return True

def main():
    articles_dir = Path(__file__).parent / 'articles'
    
    if not articles_dir.exists():
        print("Articles directory not found!")
        return
    
    html_files = list(articles_dir.glob('*.html'))
    print(f"Found {len(html_files)} HTML files in articles/\n")
    
    added = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        if add_cta_to_article(filepath):
            added += 1
        else:
            skipped += 1
    
    print(f"\n✅ Added CTA to {added} articles")
    print(f"⏭️  Skipped {skipped} articles")

if __name__ == '__main__':
    main()
