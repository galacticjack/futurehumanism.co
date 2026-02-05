#!/usr/bin/env python3
"""Fix all articles to use the correct dark theme with indigo accent."""

import os
import re
from pathlib import Path

ARTICLES_DIR = Path.home() / "projects/futurehumanism/articles"

# The correct CSS template for dark theme articles
CORRECT_CSS = '''        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --bg-primary: #0a0a0a;
            --bg-secondary: #141414;
            --accent: #6366F1;
            --border: #2a2a2a;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
        }
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
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            font-weight: 700;
            font-size: 1.2rem;
            color: var(--text-primary);
            text-decoration: none;
        }
        .logo span { font-weight: 400; opacity: 0.6; }
        .back-link {
            color: var(--accent);
            text-decoration: none;
            font-weight: 500;
        }
        .hero {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(10,10,10,1)), url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200') center/cover;
            padding: 80px 24px;
            text-align: center;
        }
        .hero-tag {
            display: inline-block;
            background: var(--accent);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
        }
        .hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            margin-bottom: 16px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }
        .hero-meta {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        article {
            max-width: 700px;
            margin: 0 auto;
            padding: 60px 24px;
        }
        article h2 {
            font-size: 1.6rem;
            margin: 48px 0 20px;
            color: var(--text-primary);
        }
        article h3 {
            font-size: 1.25rem;
            margin: 32px 0 16px;
            color: var(--text-primary);
        }
        article p {
            margin-bottom: 20px;
            color: var(--text-secondary);
        }
        article ul, article ol {
            margin: 20px 0;
            padding-left: 24px;
            color: var(--text-secondary);
        }
        article li {
            margin-bottom: 12px;
        }
        article strong {
            color: var(--text-primary);
        }
        article em {
            color: var(--accent);
            font-style: normal;
        }
        blockquote {
            background: var(--bg-secondary);
            border-left: 4px solid var(--accent);
            padding: 24px;
            margin: 32px 0;
            border-radius: 0 8px 8px 0;
            color: var(--text-secondary);
            font-style: italic;
        }
        blockquote cite {
            display: block;
            margin-top: 12px;
            font-style: normal;
            color: var(--accent);
            font-size: 0.9rem;
        }
        .highlight-box, .tool-card, .automation-card, .mistake-box, .fix-box {
            background: var(--bg-secondary);
            border-left: 4px solid var(--accent);
            padding: 24px;
            margin: 32px 0;
            border-radius: 0 8px 8px 0;
        }
        .highlight-box p, .tool-card p {
            margin: 0;
            color: var(--text-primary);
        }
        .tool-card h4, .automation-card h4 {
            color: var(--accent);
            margin-bottom: 8px;
        }
        .tool-card h5, .automation-card h5 {
            color: var(--text-primary);
            margin-bottom: 12px;
        }
        .tool-card .price {
            color: var(--accent);
            font-weight: 600;
        }
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 32px 0;
        }
        .comparison-table th, .comparison-table td {
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        .comparison-table th {
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-weight: 600;
        }
        .comparison-table td {
            color: var(--text-secondary);
        }
        .winner {
            color: #66bb6a !important;
            font-weight: 600;
        }
        .cta-box {
            background: linear-gradient(135deg, var(--accent), #818CF8);
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            margin: 48px 0;
        }
        .cta-box h3 {
            color: white;
            margin: 0 0 12px;
        }
        .cta-box p {
            color: rgba(255,255,255,0.9);
            margin-bottom: 20px;
        }
        .cta-box a {
            display: inline-block;
            background: white;
            color: var(--accent);
            padding: 12px 28px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
        }
        footer {
            border-top: 1px solid var(--border);
            padding: 40px 24px;
            text-align: center;
            background: var(--bg-secondary);
        }
        footer p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        footer a { color: var(--accent); text-decoration: none; }
        @media (max-width: 768px) {
            header { padding: 12px 16px; }
            .logo { font-size: 1rem; }
            .back-link { font-size: 0.85rem; }
            .hero { padding: 50px 16px; }
            .hero h1 { font-size: 1.6rem; line-height: 1.3; }
            article { padding: 40px 16px; }
            article h2 { font-size: 1.3rem; margin: 32px 0 16px; }
            article h3 { font-size: 1.1rem; }
            .highlight-box, .tool-card, .automation-card { padding: 16px; margin: 24px 0; }
            blockquote { padding: 16px; margin: 24px 0; }
            .cta-box { padding: 28px 20px; margin: 32px 0; }
            footer { padding: 32px 16px; }
            .comparison-table { font-size: 0.85rem; }
            .comparison-table th, .comparison-table td { padding: 10px 8px; }
        }
        /* Share Buttons */
        .share-section {
            margin: 48px 0;
            padding: 32px 0;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            text-align: center;
        }
        .share-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .share-buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
        }
        .share-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
            background: var(--bg-secondary);
            color: var(--text-secondary);
        }
        .share-btn:hover { transform: translateY(-3px); }
        .share-btn.twitter:hover { background: #1DA1F2; color: white; }
        .share-btn.linkedin:hover { background: #0077B5; color: white; }
        .share-btn.copy-link:hover { background: var(--accent); color: white; }
        /* Reading Progress Bar */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), #8B5CF6);
            z-index: 1000;
            transition: width 0.1s ease-out;
        }
        #reading-progress {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), #8B5CF6);
            z-index: 1000;
            transition: width 0.1s ease-out;
        }'''

# Files that need fixing
BROKEN_FILES = [
    "ai-agents-eating-software.html",
    "ai-agents-memory.html", 
    "chatgpt-pro-200-enterprise-ai-shift.html",
    "gemini-2-flash-multimodal-ai-dominance.html",
    "snowflake-openai-enterprise-ai-tipping-point.html",
    "deepseek-r1-vs-openai-o1.html",
    "ai-world-models-next-breakthrough.html"
]

def fix_external_css(content):
    """Remove external CSS links and replace with inline styles."""
    # Remove external CSS links
    content = re.sub(r'<link[^>]*href=["\'][^"\']*\.css["\'][^>]*>', '', content)
    content = re.sub(r'<link\s+rel="stylesheet"\s+href="[^"]*"[^>]*>', '', content)
    return content

def fix_article(filepath):
    """Fix a single article file."""
    print(f"Fixing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove external CSS links first
    content = fix_external_css(content)
    
    # Check if it already has correct theme
    if 'var(--bg-primary)' in content and '#0a0a0a' in content and '#6366F1' in content:
        print(f"  Already has correct theme, skipping CSS replacement")
        return False
    
    # Find the style tag and replace its contents
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    
    if style_match:
        # Replace the entire style content
        content = re.sub(
            r'<style[^>]*>.*?</style>',
            f'<style>\n{CORRECT_CSS}\n    </style>',
            content,
            flags=re.DOTALL
        )
    else:
        # No style tag - need to add one before </head>
        content = content.replace('</head>', f'<style>\n{CORRECT_CSS}\n    </style>\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Fixed!")
    return True

def main():
    fixed_count = 0
    for filename in BROKEN_FILES:
        filepath = ARTICLES_DIR / filename
        if filepath.exists():
            if fix_article(filepath):
                fixed_count += 1
        else:
            print(f"WARNING: File not found: {filename}")
    
    print(f"\nFixed {fixed_count} articles")

if __name__ == "__main__":
    main()
