#!/usr/bin/env python3
"""
Move inline newsletter CTA to bottom 1/3rd of each article
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / 'articles'

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


def move_cta_in_article(filepath):
    """Move inline CTA to bottom 1/3rd of article content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove existing inline CTAs
    cta_pattern = r'<!-- Inline Newsletter CTA -->.*?</div>\s*</div>\s*</div>'
    content = re.sub(cta_pattern, '', content, flags=re.DOTALL)
    
    # Also remove any without the comment marker
    cta_pattern2 = r'<div class="inline-newsletter-cta"[^>]*>.*?</form>\s*<p[^>]*>Read by.*?</p>\s*</div>'
    content = re.sub(cta_pattern2, '', content, flags=re.DOTALL)
    
    # Find the article content
    # Look for </article> or the share section
    article_end = content.find('</article>')
    if article_end == -1:
        # Try to find share section or bio section
        article_end = content.find('<!-- Share')
        if article_end == -1:
            article_end = content.find('<div class="share-box">')
    
    if article_end == -1:
        return False
    
    # Find all <h2> tags in the article to count sections
    article_content = content[:article_end]
    h2_matches = list(re.finditer(r'<h2[^>]*>', article_content))
    
    if len(h2_matches) < 2:
        # Short article, put CTA before the last section
        insert_pos = article_end
    else:
        # Put CTA after the 2/3 point (roughly bottom 1/3rd)
        target_index = int(len(h2_matches) * 0.66)
        if target_index >= len(h2_matches):
            target_index = len(h2_matches) - 1
        
        # Insert before this h2 tag
        insert_pos = h2_matches[target_index].start()
    
    # Insert the CTA
    content = content[:insert_pos] + INLINE_CTA + '\n\n' + content[insert_pos:]
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("Moving inline CTAs to bottom 1/3rd...")
    print("=" * 50)
    
    articles = list(ARTICLES_DIR.glob('*.html'))
    articles = [a for a in articles if a.stem not in ('_TEMPLATE', 'index')]
    
    print(f"Found {len(articles)} articles")
    
    fixed = 0
    for article in sorted(articles):
        try:
            if move_cta_in_article(article):
                print(f"✓ Moved CTA: {article.name}")
                fixed += 1
        except Exception as e:
            print(f"✗ Error: {article.name} - {e}")
    
    print(f"\nDone! Moved CTA in {fixed}/{len(articles)} articles")


if __name__ == '__main__':
    main()
