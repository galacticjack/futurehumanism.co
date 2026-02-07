#!/usr/bin/env python3
"""Move inline CTAs to the bottom 1/3 of articles"""

import os
import re
import glob

def fix_article_cta(filepath):
    """Move the inline CTA to 2/3 through the article content"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the inline CTA block by class name
    cta_pattern = r'(<div class="inline-newsletter-cta"[^>]*>.*?</form>\s*<p[^>]*>Read by[^<]*</p>\s*</div>)'
    cta_match = re.search(cta_pattern, content, re.DOTALL)
    
    if not cta_match:
        # Try alternative pattern
        cta_pattern = r'(<div[^>]*inline-newsletter-cta[^>]*>.*?Want more like this\?.*?</div>\s*</div>)'
        cta_match = re.search(cta_pattern, content, re.DOTALL)
    
    if not cta_match:
        print(f"  No CTA found in {os.path.basename(filepath)}")
        return False
    
    cta_block = cta_match.group(1)
    cta_start = cta_match.start()
    cta_end = cta_match.end()
    
    # Find article boundaries
    article_start = content.find('<article')
    article_end = content.find('</article>')
    
    if article_start == -1 or article_end == -1:
        print(f"  No article tags in {os.path.basename(filepath)}")
        return False
    
    article_content = content[article_start:article_end]
    
    # Find all h2 headings in the article
    h2_matches = list(re.finditer(r'<h2[^>]*>.*?</h2>', article_content, re.DOTALL))
    
    if len(h2_matches) < 3:
        # For short articles, place before the last h2
        if len(h2_matches) >= 2:
            target_h2 = h2_matches[-1]  # Last h2
            insert_pos = article_start + target_h2.start()
        else:
            print(f"  Only {len(h2_matches)} h2s in {os.path.basename(filepath)}, skipping")
            return False
    else:
        # Place CTA after the h2 that's about 2/3 through
        target_index = int(len(h2_matches) * 0.66)
        target_h2 = h2_matches[target_index]
        
        # Find the end of the paragraph/content after this h2
        h2_end_in_article = target_h2.end()
        remaining = article_content[h2_end_in_article:]
        
        # Find next h2 or end of article
        next_h2 = re.search(r'<h2[^>]*>', remaining)
        if next_h2:
            # Insert before the next h2
            insert_pos = article_start + h2_end_in_article + next_h2.start()
        else:
            insert_pos = article_end - 100  # Near end
    
    # Remove the CTA from its current position
    content_without_cta = content[:cta_start] + content[cta_end:]
    
    # Adjust insert position if it was after the CTA
    if insert_pos > cta_start:
        insert_pos -= (cta_end - cta_start)
    
    # Insert the CTA at the new position
    new_content = content_without_cta[:insert_pos] + '\n\n' + cta_block + '\n\n' + content_without_cta[insert_pos:]
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"  ✓ Moved CTA in {os.path.basename(filepath)}")
    return True

def main():
    articles_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    articles_dir = os.path.join(articles_dir, 'articles')
    
    fixed = 0
    for filepath in glob.glob(os.path.join(articles_dir, '*.html')):
        if 'index.html' in filepath or '_TEMPLATE' in filepath:
            continue
        if fix_article_cta(filepath):
            fixed += 1
    
    print(f"\nFixed {fixed} articles")

if __name__ == '__main__':
    main()
