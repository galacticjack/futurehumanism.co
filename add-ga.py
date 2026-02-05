#!/usr/bin/env python3
"""Add Google Analytics to all HTML files that don't already have it."""

import os
import glob

GA_CODE = '''    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-W0SQN4JHN2"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-W0SQN4JHN2');
    </script>
    
'''

def add_ga_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has GA
    if 'G-W0SQN4JHN2' in content:
        return False
    
    # Find <head> and insert after it
    if '<head>' in content:
        content = content.replace('<head>\n', '<head>\n' + GA_CODE, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Find all HTML files
html_files = glob.glob('**/*.html', recursive=True)

added = 0
skipped = 0

for f in html_files:
    if add_ga_to_file(f):
        print(f"✅ Added GA to: {f}")
        added += 1
    else:
        print(f"⏭️  Skipped (already has GA): {f}")
        skipped += 1

print(f"\n📊 Summary: Added to {added} files, skipped {skipped}")
