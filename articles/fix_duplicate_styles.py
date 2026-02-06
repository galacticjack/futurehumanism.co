#!/usr/bin/env python3
"""
Fix duplicate CSS in article HTML files.
The files have Nuclear SVG fix and Mobile Menu Overlay styles duplicated 
in BOTH the main <style> block AND the exit-popup <style> block.
This removes the duplicate from the exit-popup style block.
"""
import os
import re
import glob

# Pattern to match the duplicate CSS block in the exit-popup style
# This should be inside a <style> block that comes AFTER the first </style>
DUPLICATE_CSS_PATTERN = r'''        /\* Nuclear SVG fix \*/
        svg \{ width: 20px !important; height: 20px !important; max-width: 24px !important; max-height: 24px !important; flex-shrink: 0 !important; \}
        \.chevron \{ width: 16px !important; height: 16px !important; \}
        \.logo-icon, \.logo-icon img \{ width: 36px !important; height: 36px !important; max-width: 36px !important; max-height: 36px !important; \}
        \.nav-search svg, \.share-dropdown svg \{ width: 18px !important; height: 18px !important; \}
        \.dropdown-menu a svg \{ width: 16px !important; height: 16px !important; \}
        \.mega-menu-item svg \{ width: 20px !important; height: 20px !important; \}
        

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
        @media \(max-width: 768px\) \{
            nav \{
                gap: 8px;
            \}

            nav > a:not\(\.nav-cta\):not\(\.nav-search\), \.nav-dropdown:not\(\.share-dropdown\) \{
                display: none;
            \}
            
            \.nav-search, \.nav-share-btn \{
                width: 32px;
                height: 32px;
            \}
            
            \.share-dropdown \.dropdown-menu \{
                right: 0;
                left: auto;
                transform: translateY\(10px\);
            \}
            
            \.share-dropdown:hover \.dropdown-menu \{
                transform: translateY\(4px\);
            \}

            \.nav-cta \{
                padding: 6px 12px;
                font-size: 0\.75rem;
                border-radius: 5px;
            \}

            \.mobile-menu-btn \{
                display: flex;
                align-items: center;
                justify-content: center;
                width: 32px;
                height: 32px;
                font-size: 1rem;
                background: var\(--bg-secondary\);
                border: 1px solid var\(--border\);
                border-radius: 5px;
            \}
            
            \.logo-icon \{
                width: 28px;
                height: 28px;
            \}

            \.logo-text \{
                font-size: 1rem;
            \}

            \.logo \{
                gap: 6px;
            \}
            
            \.header-inner \{
                padding: 0 12px;
            \}
        \}

'''

def fix_file(filepath):
    """Remove duplicate CSS from exit-popup style block."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all occurrences of "/* Nuclear SVG fix */"
    nuclear_positions = []
    pos = 0
    while True:
        idx = content.find('/* Nuclear SVG fix */', pos)
        if idx == -1:
            break
        nuclear_positions.append(idx)
        pos = idx + 1
    
    if len(nuclear_positions) < 2:
        return False, "Only one or zero Nuclear SVG fix found"
    
    # The second occurrence is the duplicate - remove it along with the mobile menu section
    # Find the end of the duplicate block (before the closing of the exit-popup style)
    second_nuclear = nuclear_positions[1]
    
    # Find where this duplicate block ends - it's before "    </style>" (exit popup style close)
    # Look for the pattern: indented closing brace and then a newline
    # The duplicate block ends after the @media block
    
    # Find the end marker: look for a line that starts with "    </style>" after the second nuclear
    end_marker = content.find('    </style>', second_nuclear)
    if end_marker == -1:
        return False, "Could not find end of duplicate block"
    
    # The duplicate starts at second_nuclear and goes until just before </style>
    # We need to be careful - find the exact boundary
    
    # Actually, let's find the content between second nuclear position and the </style>
    # but keep only the first newlines before </style>
    
    # Find where the duplicate block actually starts (the "/* Nuclear SVG fix */" comment)
    # and remove everything from there to just before </style>
    
    # Get line before second_nuclear - find the start of that line
    line_start = content.rfind('\n', 0, second_nuclear) + 1
    
    # The content we want to remove is from line_start to end_marker
    before = content[:line_start]
    after = content[end_marker:]
    
    new_content = before + after
    
    if new_content != content:
        removed_chars = len(content) - len(new_content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f"Removed {removed_chars} chars of duplicate CSS"
    
    return False, "No changes made"

def main():
    articles_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = glob.glob(os.path.join(articles_dir, '*.html'))
    
    fixed_count = 0
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        
        # Skip template and index
        if filename in ('_TEMPLATE.html', 'index.html', 'fix_duplicates.py', 'fix_duplicate_styles.py'):
            continue
        
        if not filename.endswith('.html'):
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
