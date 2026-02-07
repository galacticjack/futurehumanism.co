#!/usr/bin/env python3
"""Add missing footers to articles - CAREFUL not to truncate content"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

FOOTER_HTML = '''
    <footer>
        <p>© 2026 <a href="/">Future Humanism</a> · <a href="https://twitter.com/FutureHumanism" target="_blank">Twitter</a> · <a href="/subscribe.html">Newsletter</a></p>
    </footer>'''

def add_footer(filepath):
    """Add footer if missing - preserve all content"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Already has footer - skip
    if '</footer>' in content:
        return False
    
    # Count paragraphs before - must match after
    p_before = content.count('<p>')
    
    # Find insertion point - right before </body> or </html>
    # Or at the very end if those are missing
    
    if '</body>' in content:
        # Insert before </body>
        content = content.replace('</body>', FOOTER_HTML + '\n</body>')
    elif '</html>' in content:
        # Insert before </html>
        content = content.replace('</html>', FOOTER_HTML + '\n</body>\n</html>')
    else:
        # Add at end
        content = content.rstrip() + FOOTER_HTML + '\n</body>\n</html>'
    
    # Verify we didn't lose content
    p_after = content.count('<p>')
    if p_after != p_before:
        print(f"    WARNING: Paragraph count changed from {p_before} to {p_after}!")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("Adding missing footers (preserving content)...")
    
    fixed = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        if add_footer(filepath):
            print(f"  ✓ {filepath.name}")
            fixed += 1
    
    print(f"\n  Added footers to {fixed} articles")

if __name__ == '__main__':
    main()
