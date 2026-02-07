#!/usr/bin/env python3
"""Fix light theme pages to use dark theme"""

import os
import re

# Pages to fix (in root directory)
PAGES_TO_FIX = [
    'about.html',
    'challenge.html', 
    'open-source-agents.html',
    'privacy.html',
    'quiz.html',
    'referrals.html',
    'resources.html',
    'search.html',
    'subscribe.html',
    'terms.html'
]

# Dark theme CSS variables that should be used
DARK_THEME_CSS = """        :root {
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --text-muted: #707070;
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --bg-card: #141414;
            --border: #2a2a2a;
            --accent: #1E90FF;
            --accent-hover: #3BA0FF;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-secondary);
            line-height: 1.6;
        }"""

# Standard dark header CSS
DARK_HEADER_CSS = """
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
        }"""

# Standard dark footer CSS
DARK_FOOTER_CSS = """
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
        }"""

def fix_page(filepath):
    """Fix a single page to use dark theme"""
    print(f"Fixing: {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Remove any existing light theme :root variables (keep only one dark set)
    # Pattern to find :root blocks with light colors
    light_root_patterns = [
        r':root\s*\{[^}]*--bg-primary:\s*#fff[^}]*\}',
        r':root\s*\{[^}]*--bg-primary:\s*#ffffff[^}]*\}',
        r':root\s*\{[^}]*--text-primary:\s*#1a1a1a[^}]*\}',
    ]
    
    for pattern in light_root_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Replace light background colors in body
    content = re.sub(r'body\s*\{[^}]*background:\s*var\(--bg-primary\);[^}]*color:\s*var\(--text-primary\);[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'background:\s*#f8f9fa', 'background: var(--bg-secondary)', content)
    content = re.sub(r'background:\s*#f0f4f8', 'background: var(--bg-secondary)', content)
    content = re.sub(r'background:\s*white', 'background: var(--bg-card)', content)
    content = re.sub(r'background:\s*#ffffff', 'background: var(--bg-card)', content)
    content = re.sub(r'background:\s*#fff(?![a-fA-F0-9])', 'background: var(--bg-card)', content)
    
    # Fix accent-light (light blue background) to use dark version
    content = re.sub(r'--accent-light:\s*#E8F4FD', '--accent-light: rgba(30,144,255,0.15)', content)
    content = re.sub(r'--success-light:\s*#dcfce7', '--success-light: rgba(34,197,94,0.15)', content)
    
    # Fix text colors for dark theme
    content = re.sub(r'color:\s*#1a1a1a(?![a-fA-F0-9])', 'color: var(--text-primary)', content)
    content = re.sub(r'color:\s*#555555', 'color: var(--text-secondary)', content)
    content = re.sub(r'color:\s*#888888', 'color: var(--text-muted)', content)
    
    # Fix border colors
    content = re.sub(r'border[^:]*:\s*[^;]*#e5e7eb', lambda m: m.group().replace('#e5e7eb', 'var(--border)'), content)
    content = re.sub(r'--border:\s*#e5e7eb', '--border: #2a2a2a', content)
    
    # Fix bg-card in CSS variables
    content = re.sub(r'--bg-card:\s*#ffffff', '--bg-card: #141414', content)
    content = re.sub(r'--bg-secondary:\s*#f8f9fa', '--bg-secondary: #1a1a1a', content)
    
    # Make sure there's a proper dark theme :root at the start
    # First, check if we already have a dark theme :root
    if '--bg-primary: #0a0a0a' not in content:
        # Find the <style> tag and inject dark theme
        style_match = re.search(r'<style>', content)
        if style_match:
            insert_pos = style_match.end()
            content = content[:insert_pos] + '\n' + DARK_THEME_CSS + '\n' + content[insert_pos:]
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    if content != original:
        print(f"  ✓ Updated {filepath}")
    else:
        print(f"  - No changes needed for {filepath}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for page in PAGES_TO_FIX:
        filepath = os.path.join(base_dir, page)
        if os.path.exists(filepath):
            fix_page(filepath)
        else:
            print(f"  ✗ File not found: {page}")

if __name__ == '__main__':
    main()
