#!/usr/bin/env python3
"""Fix corrupted article files - truncate after mobileMenuBtn script"""

import os
import re
from pathlib import Path

articles_dir = Path(__file__).parent.parent / "articles"

def fix_article(filepath):
    """Fix by finding the proper ending point"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # Count "Keep Reading" - if more than 1, file is corrupted
    keep_reading_count = content.count('Keep Reading')
    
    if keep_reading_count <= 1:
        return False
    
    print(f"  {filepath.name}: {keep_reading_count} 'Keep Reading' sections")
    
    # Find the proper end: after mobileMenuBtn script
    # Pattern: mobileMenuBtn.addEventListener('click', openMobileMenu); ... </script>
    
    pattern = r"mobileMenuBtn\.addEventListener\('click',\s*openMobileMenu\);\s*}\s*</script>"
    matches = list(re.finditer(pattern, content))
    
    if matches:
        # Use the FIRST match
        first_match_end = matches[0].end()
        new_content = content[:first_match_end] + '\n</body>\n</html>'
        
        bytes_removed = original_len - len(new_content)
        
        if bytes_removed > 100:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    FIXED (mobileMenu): removed {bytes_removed} bytes")
            return True
    
    # Alternative: Find closing </script> after closeMobileMenu function
    pattern2 = r"function closeMobileMenu\(\)[\s\S]*?</script>"
    matches2 = list(re.finditer(pattern2, content))
    
    if matches2:
        first_match_end = matches2[0].end()
        new_content = content[:first_match_end] + '\n</body>\n</html>'
        
        bytes_removed = original_len - len(new_content)
        
        if bytes_removed > 100:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    FIXED (closeMobile): removed {bytes_removed} bytes")
            return True
    
    print(f"    WARNING: Could not find proper end pattern")
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
