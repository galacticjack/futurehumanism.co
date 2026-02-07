#!/usr/bin/env python3
"""
Fix all tools pages to have consistent header, logo, and footer
Matches the main site dark theme with gradient logo
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / 'tools'

# Consistent header for tools
HEADER_HTML = '''
    <!-- Header -->
    <header>
        <div class="header-inner">
            <a href="/" class="logo">
                <div class="logo-icon"><img src="../images/profile.jpg" alt="Future Humanism"></div>
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
        /* Consistent site theme */
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
'''


def fix_tool_page(filepath):
    """Fix a tool page to have consistent theme"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Add/replace CSS theme variables and header/footer styles
    if '/* Consistent site theme */' not in content:
        # Find first style block and add our CSS at the start
        match = re.search(r'<style>', content)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + THEME_CSS + content[insert_pos:]
    
    # 2. Replace any existing header with consistent one
    # Look for various header patterns
    header_patterns = [
        r'<header[^>]*>.*?</header>',
        r'<!-- Header -->.*?</header>',
        r'<nav class="site-nav">.*?</nav>',
    ]
    
    header_found = False
    for pattern in header_patterns:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(pattern, HEADER_HTML.strip(), content, count=1, flags=re.DOTALL | re.IGNORECASE)
            header_found = True
            break
    
    # If no header found, add after <body>
    if not header_found:
        content = re.sub(r'<body[^>]*>', lambda m: m.group(0) + HEADER_HTML, content, count=1)
    
    # 3. Replace any existing footer with consistent one
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
    
    # If no footer found, add before </body>
    if not footer_found:
        content = content.replace('</body>', FOOTER_HTML + '\n</body>')
    
    # 4. Fix logo paths (../images/ for tools subdirectory)
    content = content.replace('src="images/', 'src="../images/')
    content = content.replace("src='images/", "src='../images/")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("Fixing tools pages theme...")
    print("=" * 50)
    
    tools = list(TOOLS_DIR.glob('*.html'))
    print(f"Found {len(tools)} tool pages")
    
    fixed = 0
    for tool in sorted(tools):
        try:
            if fix_tool_page(tool):
                print(f"✓ Fixed: {tool.name}")
                fixed += 1
            else:
                print(f"- Skipped: {tool.name}")
        except Exception as e:
            print(f"✗ Error: {tool.name} - {e}")
    
    print(f"\nDone! Fixed {fixed}/{len(tools)} tools")


if __name__ == '__main__':
    main()
