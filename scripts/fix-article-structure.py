#!/usr/bin/env python3
"""Fix article structure - ensure proper footer and closing tags"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

FOOTER_HTML = '''
    <footer>
        <p>© 2026 <a href="/">Future Humanism</a> · <a href="https://twitter.com/FutureHumanism" target="_blank">Twitter</a> · <a href="/subscribe.html">Newsletter</a></p>
    </footer>
</body>
</html>'''

def fix_article(filepath):
    """Fix article structure"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    issues_fixed = []
    
    # Check if missing </footer>
    has_footer = '</footer>' in content
    has_body_close = '</body>' in content
    has_html_close = '</html>' in content
    
    if not has_footer or not has_body_close or not has_html_close:
        # Remove any partial closing tags
        content = re.sub(r'\s*</body>\s*$', '', content)
        content = re.sub(r'\s*</html>\s*$', '', content)
        content = content.rstrip()
        
        # Find where to insert footer
        # Should be after </article> or after last content div
        
        if '</article>' in content:
            # Insert footer after </article>
            last_article = content.rfind('</article>')
            if last_article != -1:
                content = content[:last_article + len('</article>')] + '\n' + FOOTER_HTML
                issues_fixed.append('added_footer_after_article')
        else:
            # No </article> tag, add footer at end
            content = content + '\n' + FOOTER_HTML
            issues_fixed.append('added_footer_at_end')
    
    # Ensure proper closing
    if not content.strip().endswith('</html>'):
        content = content.rstrip()
        if not content.endswith('</body>'):
            content += '\n</body>'
        if not content.endswith('</html>'):
            content += '\n</html>'
        issues_fixed.append('fixed_closing_tags')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return issues_fixed
    
    return []

def main():
    print("Fixing article structure (footer, closing tags)...")
    print("")
    
    fixed_count = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        issues = fix_article(filepath)
        if issues:
            print(f"  ✓ {filepath.name}: {', '.join(issues)}")
            fixed_count += 1
    
    print(f"\n  Fixed {fixed_count} articles")

if __name__ == '__main__':
    main()
