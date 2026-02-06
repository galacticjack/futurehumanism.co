#!/usr/bin/env python3
"""
Add exit-intent popup to all article pages.
This injects the popup component before </body> on each article.
"""

import os
import glob

# Get the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_DIR = os.path.join(PROJECT_ROOT, 'articles')
COMPONENT_PATH = os.path.join(PROJECT_ROOT, 'components', 'exit-popup.html')

# Read the popup component
with open(COMPONENT_PATH, 'r') as f:
    popup_html = f.read()

# Marker to check if already added
MARKER = 'id="exit-popup"'

# Process all article HTML files
articles = glob.glob(os.path.join(ARTICLES_DIR, '*.html'))
updated = 0
skipped = 0

for article_path in articles:
    filename = os.path.basename(article_path)
    
    # Skip template
    if filename.startswith('_'):
        continue
        
    with open(article_path, 'r') as f:
        content = f.read()
    
    # Check if already has popup
    if MARKER in content:
        print(f"  Skipped (already has popup): {filename}")
        skipped += 1
        continue
    
    # Insert before </body>
    if '</body>' in content:
        new_content = content.replace('</body>', f'\n\n{popup_html}\n</body>')
        
        with open(article_path, 'w') as f:
            f.write(new_content)
        
        print(f"  Added popup to: {filename}")
        updated += 1
    else:
        print(f"  Warning: No </body> found in {filename}")

print(f"\nDone! Updated {updated} articles, skipped {skipped}")
