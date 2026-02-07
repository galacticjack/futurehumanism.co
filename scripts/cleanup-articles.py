#!/usr/bin/env python3
"""
Clean up article HTML - remove duplicate closing tags and malformed content.
Preserves all article content while fixing structure.
"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

FOOTER_HTML = '''
    <footer>
        <p>© 2026 <a href="/">Future Humanism</a> · <a href="https://twitter.com/FutureHumanism" target="_blank">Twitter</a> · <a href="/subscribe.html">Newsletter</a></p>
    </footer>'''

def cleanup_article(filepath):
    """Fix article structure issues"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_p_count = content.count('<p>')
    
    # Remove malformed comment lines like "</body> in articles -->"
    content = re.sub(r'</body>\s*in\s*articles\s*-->', '', content)
    content = re.sub(r'</body>\s*-->', '', content)
    
    # Remove duplicate </body> and </html> tags
    # Keep only the LAST valid occurrence
    
    # First, strip all </body> and </html>
    content = re.sub(r'\s*</body>\s*', '', content)
    content = re.sub(r'\s*</html>\s*', '', content)
    
    # Clean up trailing whitespace
    content = content.rstrip()
    
    # Check if has footer
    has_footer = '</footer>' in content
    
    # Add footer if missing
    if not has_footer:
        content += '\n' + FOOTER_HTML
    
    # Add proper closing tags
    content += '\n</body>\n</html>'
    
    # Verify paragraph count preserved
    new_p_count = content.count('<p>')
    if new_p_count != original_p_count:
        print(f"  ⚠️  {filepath.name}: paragraph count changed {original_p_count} -> {new_p_count}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("Cleaning up article HTML structure...")
    print("")
    
    fixed = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        if cleanup_article(filepath):
            # Verify the fix
            with open(filepath, 'r') as f:
                c = f.read()
            body_count = c.count('</body>')
            footer = '</footer>' in c
            if body_count == 1 and footer:
                print(f"  ✓ {filepath.name}")
                fixed += 1
            else:
                print(f"  ⚠️  {filepath.name}: still has issues (body={body_count}, footer={footer})")
    
    print(f"\n  Fixed {fixed} articles")

if __name__ == '__main__':
    main()
