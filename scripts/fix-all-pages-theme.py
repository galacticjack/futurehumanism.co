#!/usr/bin/env python3
"""
Fix all pages to have consistent header, logo, and footer
Matches the main site dark theme with gradient logo
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Consistent header (simplified, no mega menu)
def get_header(img_path='images/profile.jpg'):
    return f'''
    <!-- Header -->
    <header>
        <div class="header-inner">
            <a href="/" class="logo">
                <div class="logo-icon"><img src="{img_path}" alt="Future Humanism"></div>
                <div class="logo-text">Future<span>Humanism</span></div>
            </a>
            <nav>
                <a href="/articles/">Stories</a>
                <a href="/tools/">Tools</a>
                <a href="/about.html">About</a>
                <a href="/subscribe.html" class="nav-cta">Subscribe</a>
            </nav>
        </div>
    </header>
'''

# Consistent footer
FOOTER_HTML = '''
    <!-- Footer -->
    <footer>
        <div class="footer-inner">
            <div class="footer-brand">
                <a href="/" class="footer-logo">Future<span>Humanism</span></a>
                <p>Where AI meets human potential.</p>
            </div>
            <div class="footer-links">
                <div class="footer-col"><h5>Content</h5><a href="/articles/">Stories</a><a href="/about.html">About</a></div>
                <div class="footer-col"><h5>Tools</h5><a href="/tools/">All Tools</a></div>
                <div class="footer-col"><h5>Connect</h5><a href="https://x.com/FutureHumanism" target="_blank">Twitter</a></div>
            </div>
        </div>
        <div class="footer-bottom"><p>&copy; 2026 Future Humanism</p></div>
    </footer>
'''

# CSS for header and footer (dark theme)
THEME_CSS = '''
        /* === SITE THEME === */
        :root {
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --text-muted: #707070;
            --bg-primary: #0a0a0a;
            --bg-secondary: #141414;
            --bg-card: #1a1a1a;
            --accent: #1E90FF;
            --accent-hover: #3BA0FF;
            --border: #2a2a2a;
        }
        
        body {
            background: var(--bg-primary);
            color: var(--text-secondary);
        }
        
        /* Header */
        header {
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            background: rgba(10,10,10,0.95);
            backdrop-filter: blur(10px);
            z-index: 100;
        }
        
        .header-inner {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text-primary);
        }
        
        .logo-icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            overflow: hidden;
        }
        
        .logo-icon img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .logo-text {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        .logo-text span {
            font-weight: 400;
            opacity: 0.6;
        }
        
        nav {
            display: flex;
            align-items: center;
            gap: 24px;
        }
        
        nav a {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        nav a:hover {
            color: var(--accent);
        }
        
        .nav-cta {
            background: var(--accent) !important;
            color: white !important;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600 !important;
        }
        
        .nav-cta:hover {
            background: var(--accent-hover) !important;
        }
        
        /* Footer */
        footer {
            background: #000;
            border-top: 1px solid var(--border);
            padding: 48px 24px 24px;
            margin-top: 60px;
        }
        
        .footer-inner {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            gap: 40px;
            flex-wrap: wrap;
        }
        
        .footer-brand {
            max-width: 280px;
        }
        
        .footer-logo {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-primary);
            text-decoration: none;
            display: block;
            margin-bottom: 12px;
        }
        
        .footer-logo span {
            font-weight: 400;
            opacity: 0.6;
        }
        
        .footer-brand p {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        
        .footer-links {
            display: flex;
            gap: 48px;
        }
        
        .footer-col h5 {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-primary);
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        
        .footer-col a {
            display: block;
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-decoration: none;
            margin-bottom: 8px;
        }
        
        .footer-col a:hover {
            color: var(--accent);
        }
        
        .footer-bottom {
            max-width: 1200px;
            margin: 32px auto 0;
            padding-top: 16px;
            border-top: 1px solid var(--border);
            text-align: center;
        }
        
        .footer-bottom p {
            font-size: 0.8rem;
            color: var(--text-muted);
        }
        
        @media (max-width: 768px) {
            nav {
                gap: 12px;
            }
            nav a:not(.nav-cta) {
                display: none;
            }
            .footer-inner {
                flex-direction: column;
            }
            .footer-links {
                gap: 32px;
            }
        }
        /* === END SITE THEME === */
'''


def get_img_path(filepath):
    """Determine correct image path based on file location"""
    if '/tools/' in str(filepath):
        return '../images/profile.jpg'
    elif '/articles/' in str(filepath):
        return '../images/profile.jpg'
    elif '/free-guide/' in str(filepath):
        return '../images/profile.jpg'
    else:
        return 'images/profile.jpg'


def fix_page(filepath):
    """Fix a page to have consistent theme"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    img_path = get_img_path(filepath)
    
    # Skip if it's the main index.html (already has full nav)
    if filepath.name == 'index.html' and filepath.parent == PROJECT_ROOT:
        return False
    
    # 1. Add CSS theme if not present
    if '=== SITE THEME ===' not in content:
        match = re.search(r'<style>', content)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + THEME_CSS + content[insert_pos:]
    
    # 2. Replace header
    header_patterns = [
        r'<header[^>]*>.*?</header>',
        r'<!-- Header -->.*?</header>',
    ]
    
    header_html = get_header(img_path)
    header_found = False
    for pattern in header_patterns:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(pattern, header_html.strip(), content, count=1, flags=re.DOTALL | re.IGNORECASE)
            header_found = True
            break
    
    if not header_found and '<body' in content:
        content = re.sub(r'<body[^>]*>', lambda m: m.group(0) + header_html, content, count=1)
    
    # 3. Replace footer
    footer_patterns = [
        r'<footer[^>]*>.*?</footer>',
        r'<!-- Footer -->.*?</footer>',
    ]
    
    footer_found = False
    for pattern in footer_patterns:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(pattern, FOOTER_HTML.strip(), content, count=1, flags=re.DOTALL | re.IGNORECASE)
            footer_found = True
            break
    
    if not footer_found and '</body>' in content:
        content = content.replace('</body>', FOOTER_HTML + '\n</body>')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("Fixing ALL pages theme...")
    print("=" * 50)
    
    # Get all HTML files
    pages = []
    
    # Root pages
    for f in PROJECT_ROOT.glob('*.html'):
        if f.name not in ('index.html',):  # Skip main index
            pages.append(f)
    
    # Tools
    for f in (PROJECT_ROOT / 'tools').glob('*.html'):
        pages.append(f)
    
    # Free guide
    for f in (PROJECT_ROOT / 'free-guide').glob('*.html'):
        pages.append(f)
    
    # Articles index
    articles_index = PROJECT_ROOT / 'articles' / 'index.html'
    if articles_index.exists():
        pages.append(articles_index)
    
    print(f"Found {len(pages)} pages to check")
    
    fixed = 0
    for page in sorted(pages):
        try:
            if fix_page(page):
                print(f"✓ Fixed: {page.relative_to(PROJECT_ROOT)}")
                fixed += 1
        except Exception as e:
            print(f"✗ Error: {page.name} - {e}")
    
    print(f"\nDone! Fixed {fixed}/{len(pages)} pages")


if __name__ == '__main__':
    main()
