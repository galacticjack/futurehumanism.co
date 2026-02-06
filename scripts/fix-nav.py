#!/usr/bin/env python3
"""Fix navigation across all FutureHumanism pages - add Free Guide button"""

import os
import re
from pathlib import Path

ROOT = Path("/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co")

# CSS to add for nav-cta-secondary
CSS_SECONDARY = """
        .nav-cta-secondary {
            background: transparent;
            border: 1px solid var(--accent);
            color: var(--accent) !important;
        }
        
        .nav-cta-secondary:hover {
            background: var(--accent);
            color: white !important;
        }
"""

def fix_file(filepath):
    """Add Free Guide button and CSS to a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Skip if already has Free Guide
    if 'Free Guide' in content:
        return False, "already has Free Guide"
    
    # Skip if no Subscribe nav-cta
    if 'class="nav-cta">Subscribe' not in content:
        return False, "no nav-cta Subscribe"
    
    # Add Free Guide button before Subscribe
    content = content.replace(
        '<a href="/subscribe.html" class="nav-cta">Subscribe</a>',
        '<a href="/free-guide" class="nav-cta nav-cta-secondary">Free Guide</a>\n                <a href="/subscribe.html" class="nav-cta">Subscribe</a>'
    )
    
    # Add nav-cta-secondary CSS if missing
    if '.nav-cta-secondary' not in content:
        # Find .nav-cta:hover block and add after it
        # Look for pattern like .nav-cta:hover { ... }
        pattern = r'(\.nav-cta:hover\s*\{[^}]+\})'
        match = re.search(pattern, content)
        if match:
            content = content.replace(
                match.group(1),
                match.group(1) + CSS_SECONDARY
            )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "fixed"
    
    return False, "no changes needed"

def main():
    fixed = 0
    skipped = 0
    
    for html_file in ROOT.rglob("*.html"):
        # Skip templates and node_modules
        if "_TEMPLATE" in str(html_file) or "node_modules" in str(html_file):
            continue
        
        rel_path = html_file.relative_to(ROOT)
        changed, reason = fix_file(html_file)
        
        if changed:
            print(f"✅ FIXED: {rel_path}")
            fixed += 1
        else:
            print(f"⏭️  SKIP ({reason}): {rel_path}")
            skipped += 1
    
    print(f"\n📊 Summary: {fixed} fixed, {skipped} skipped")

if __name__ == "__main__":
    main()
