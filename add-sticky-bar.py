#!/usr/bin/env python3
"""
Add sticky newsletter bar to all articles.
The bar appears after 30% scroll and stays fixed at bottom.
"""

import os
import re
from pathlib import Path

# Read the component
component_path = Path(__file__).parent / "components" / "sticky-cta-bar.html"
with open(component_path, 'r') as f:
    sticky_component = f.read()

# Remove the HTML comment header from component for cleaner insertion
sticky_component = sticky_component.strip()

articles_dir = Path(__file__).parent / "articles"
updated_count = 0
skipped_count = 0

for article_path in articles_dir.glob("*.html"):
    if article_path.name == "_TEMPLATE.html":
        continue
    
    with open(article_path, 'r') as f:
        content = f.read()
    
    # Skip if already has sticky bar
    if 'sticky-cta-bar' in content:
        print(f"⏭️  Skipped (already has sticky bar): {article_path.name}")
        skipped_count += 1
        continue
    
    # Insert before </body>
    if '</body>' in content:
        new_content = content.replace('</body>', f'\n    <!-- Sticky Newsletter Bar -->\n{sticky_component}\n</body>')
        
        with open(article_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Added sticky bar: {article_path.name}")
        updated_count += 1
    else:
        print(f"⚠️  No </body> found: {article_path.name}")

print(f"\n📊 Summary: {updated_count} articles updated, {skipped_count} skipped")
