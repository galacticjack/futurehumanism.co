#!/usr/bin/env python3
"""Fix corrupted article files - remove duplicate sections"""

import os
import re
from pathlib import Path

articles_dir = Path(__file__).parent.parent / "articles"

def fix_article(filepath):
    """Fix a single article by finding first proper structure end"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # Count "Keep Reading" - if more than 1, file is corrupted
    keep_reading_count = content.count('Keep Reading')
    
    if keep_reading_count <= 1:
        return False  # File is fine
    
    print(f"  {filepath.name}: {keep_reading_count} 'Keep Reading' sections found")
    
    # Find first occurrence of the related articles/Keep Reading section
    # Then find the FIRST </article> after main content
    
    # Strategy: Find first </article> tag, then first <footer or simple footer after it
    article_close = content.find('</article>')
    
    if article_close == -1:
        # Try alternative - find by footer
        # Look for simple footer pattern: <footer> ... </footer>
        footer_match = re.search(r'<footer[^>]*>.*?</footer>', content, re.DOTALL)
        if footer_match:
            # Take content up to end of first footer, then close properly
            end_pos = footer_match.end()
            new_content = content[:end_pos] + '\n</body>\n</html>'
        else:
            print(f"    WARNING: Cannot find structure in {filepath.name}")
            return False
    else:
        # Found </article>, look for footer after it
        after_article = content[article_close:]
        
        # Find first <footer or </footer
        footer_start = after_article.find('<footer')
        if footer_start == -1:
            footer_start = after_article.find('    <footer')  # indented
        
        if footer_start != -1:
            # Find </footer> after this
            footer_section = after_article[footer_start:]
            footer_end_match = re.search(r'</footer>', footer_section)
            
            if footer_end_match:
                end_pos = article_close + footer_start + footer_end_match.end()
                new_content = content[:end_pos] + '\n</body>\n</html>'
            else:
                # No footer end found, close after article
                new_content = content[:article_close + len('</article>')] + '\n</body>\n</html>'
        else:
            # No footer, close after article
            new_content = content[:article_close + len('</article>')] + '\n</body>\n</html>'
    
    bytes_removed = original_len - len(new_content)
    
    if bytes_removed > 100:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"    FIXED: removed {bytes_removed} bytes")
        return True
    
    return False

def main():
    fixed_count = 0
    
    for filepath in sorted(articles_dir.glob('*.html')):
        if filepath.name.startswith('_'):
            continue
            
        if fix_article(filepath):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} articles")

if __name__ == '__main__':
    main()
