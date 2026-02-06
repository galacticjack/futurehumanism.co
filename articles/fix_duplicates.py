#!/usr/bin/env python3
"""
Fix duplicate CSS blocks in article HTML files.
Removes the first occurrence of duplicate Mobile Menu Overlay + Mobile responsive nav sections.
"""
import os
import re
import glob

# Pattern to match the first duplicate block that needs to be removed
# This matches from the first "/* Mobile Menu Overlay */" up to but not including 
# the second "/* Mobile Menu Overlay */" which comes after the duplicate SVG fixes

DUPLICATE_BLOCK_PATTERN = r'''
        /\* Mobile Menu Overlay \*/
        \.mobile-menu \{
            display: none;
            position: fixed;
            inset: 0;
            background: var\(--bg-primary\);
            z-index: 200;
            flex-direction: column;
            padding: 80px 24px 40px;
        \}

        \.mobile-menu\.open \{
            display: flex;
        \}

        \.mobile-menu a \{
            display: block;
            padding: 16px 0;
            font-size: 1\.2rem;
            color: var\(--text-primary\);
            text-decoration: none;
            border-bottom: 1px solid var\(--border\);
        \}

        \.mobile-menu \.close-btn \{
            position: absolute;
            top: 16px;
            right: 16px;
            background: none;
            border: none;
            color: var\(--text-primary\);
            font-size: 2rem;
            cursor: pointer;
        \}

        /\* Mobile responsive nav \*/
        svg \{ width: 20px !important; height: 20px !important; max-width: 24px !important; max-height: 24px !important; flex-shrink: 0 !important; \}
        \.chevron \{ width: 16px !important; height: 16px !important; \}
        \.logo-icon, \.logo-icon img \{ width: 36px !important; height: 36px !important; max-width: 36px !important; max-height: 36px !important; \}
        \.nav-search svg, \.share-dropdown svg \{ width: 18px !important; height: 18px !important; \}
        \.dropdown-menu a svg \{ width: 16px !important; height: 16px !important; \}
        \.mega-menu-item svg \{ width: 20px !important; height: 20px !important; \}
        

'''

def fix_file(filepath):
    """Remove duplicate CSS block from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it has duplicate mobile-menu blocks
    mobile_menu_count = content.count('/* Mobile Menu Overlay */')
    
    if mobile_menu_count <= 1:
        return False, "No duplicates found"
    
    # Find and remove the first duplicate block
    # The pattern is: after Nuclear SVG fix + SVG fixes, there's a duplicate Mobile Menu + SVG fixes block
    
    # Strategy: Find all occurrences of "/* Mobile Menu Overlay */"
    # Keep only the last one (which is followed by @media)
    
    # Find the first occurrence and remove the block up to the second occurrence
    first_idx = content.find('/* Mobile Menu Overlay */')
    if first_idx == -1:
        return False, "No Mobile Menu Overlay found"
    
    # Find the second occurrence
    second_idx = content.find('/* Mobile Menu Overlay */', first_idx + 1)
    if second_idx == -1:
        return False, "Only one Mobile Menu Overlay found"
    
    # Now find where to cut: we want to remove from first_idx to second_idx
    # But we need to find the exact boundary - go back a bit to include leading whitespace
    
    # Actually, let's look for the exact pattern and remove it
    new_content = content[:first_idx] + content[second_idx:]
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f"Removed duplicate (cut {second_idx - first_idx} chars)"
    
    return False, "No changes made"

def main():
    articles_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = glob.glob(os.path.join(articles_dir, '*.html'))
    
    fixed_count = 0
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        
        # Skip template and index
        if filename in ('_TEMPLATE.html', 'index.html'):
            continue
        
        fixed, message = fix_file(filepath)
        if fixed:
            fixed_count += 1
            print(f"✅ Fixed: {filename} - {message}")
        else:
            print(f"⏭️  Skipped: {filename} - {message}")
    
    print(f"\n📊 Total: {fixed_count} files fixed")

if __name__ == '__main__':
    main()
