#!/usr/bin/env python3
"""Fix logo markup across all article pages."""
import os
import re
import glob

ARTICLES_DIR = "/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co/articles"

# The correct logo HTML for articles (relative path)
CORRECT_LOGO = '''<a href="../" class="logo">
                <div class="logo-icon"><img src="../images/profile.jpg" alt="Future Humanism"></div>
                <div class="logo-text">Future<span>Humanism</span></div>
            </a>'''

# Patterns to match various broken logo formats
LOGO_PATTERNS = [
    r'<a href="[^"]*" class="logo">Future Humanism</a>',
    r'<a href="[^"]*" class="logo">Future <span>Humanism</span></a>',
    r'<a href="[^"]*" class="logo">Future<span[^>]*>Humanism</span></a>',
    r'<a href="[^"]*" class="logo">\s*</a>',
    r'<a href="[^"]*" class="logo">\s*\n\s*</a>',
]

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    for pattern in LOGO_PATTERNS:
        content = re.sub(pattern, CORRECT_LOGO, content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    fixed = 0
    skipped = 0
    
    for filepath in glob.glob(os.path.join(ARTICLES_DIR, "*.html")):
        if "_TEMPLATE" in filepath:
            continue
        
        filename = os.path.basename(filepath)
        
        # Check if already has correct logo
        with open(filepath, 'r') as f:
            content = f.read()
        
        if 'logo-icon"><img src="../images/profile.jpg"' in content:
            print(f"✓ {filename} - already correct")
            skipped += 1
            continue
        
        if fix_file(filepath):
            print(f"✓ {filename} - FIXED")
            fixed += 1
        else:
            print(f"? {filename} - no match found, needs manual check")
    
    print(f"\nDone: {fixed} fixed, {skipped} already correct")

if __name__ == "__main__":
    main()
