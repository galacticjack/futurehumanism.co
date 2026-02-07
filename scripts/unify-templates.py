#!/usr/bin/env python3
"""
Unify all article templates to match the clean Remote Work template.
This script extracts article content and rebuilds each file with the master template.
"""

import re
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"
TEMPLATE_FILE = ARTICLES_DIR / "remote-work-async-culture-2026.html"

# Article image mapping
ARTICLE_IMAGES = {
    '16-ai-agents-built-c-compiler': 'photo-1629654297299-c8506221ca97',
    '2026-year-ai-agents-production': 'photo-1677442136019-21780ecad995',
    '50-dollar-tech-stack': 'photo-1498050108023-c5249f4df085',
    'agent-infrastructure-orchestration-2026': 'photo-1558494949-ef010cbdcc31',
    'agentic-ai-100-billion-market-2026': 'photo-1551288049-bebda4e38f71',
    'ai-agent-economy-2027': 'photo-1460925895917-afdab827c52f',
    'ai-agent-security-vulnerabilities-2026': 'photo-1563986768609-322da13575f3',
    'ai-agents-2026-guide': 'photo-1531746790731-6c087fecd65a',
    'ai-agents-eating-software': 'photo-1620712943543-bcc4688e7485',
    'ai-agents-memory': 'photo-1485827404703-89b55fcc595e',
    'ai-agents-platform-shift': 'photo-1518770660439-4636190af475',
    'ai-computer-control-revolution': 'photo-1551434678-e076c223a692',
    'ai-marketing-strategies-2026': 'photo-1460925895917-afdab827c52f',
    'ai-model-convergence-2026': 'photo-1620712943543-bcc4688e7485',
    'ai-tools-replacing-saas-subscriptions': 'photo-1581091226825-a6a2a5aee158',
    'ai-world-models-next-breakthrough': 'photo-1518432031352-d6fc5c10da5a',
    'apple-xcode-agentic-coding': 'photo-1621839673705-6617adf9e890',
    'automate-80-percent-agency-work': 'photo-1553729459-efe14ef6055d',
    'automate-freelance-business-ai-guide': 'photo-1460925895917-afdab827c52f',
    'best-ai-coding-assistants-beginners-2026': 'photo-1555949963-ff9fe0c870eb',
    'best-ai-tools-solopreneurs-2026': 'photo-1581091226825-a6a2a5aee158',
    'build-your-first-ai-agent-practical-guide': 'photo-1555949963-aa79dcee981c',
    'building-passive-income-ai-automation': 'photo-1554224155-6726b3ff858f',
    'chatgpt-pro-200-enterprise-ai-shift': 'photo-1553877522-43269d4ea984',
    'claude-vs-chatgpt-for-coding-2026': 'photo-1587620962725-abab7fe55159',
    'claude-vs-gpt-comparison': 'photo-1516110833967-0b5716ca1387',
    'creator-economy-ai-tools-2026': 'photo-1611162617474-5b21e879e113',
    'crypto-market-cycles-ai-trading-signals': 'photo-1518546305927-5a555bb7020d',
    'deepseek-r1-vs-openai-o1': 'photo-1526374965328-7f61d4dc18c5',
    'defi-yield-strategies-2026': 'photo-1639762681485-074b7f938ba0',
    'future-of-search-after-chatgpt': 'photo-1555421689-491a97ff2040',
    'gemini-2-flash-multimodal-ai-dominance': 'photo-1504868584819-f8e8b4b6d7e3',
    'github-copilot-vs-cursor-vs-claude-code-2026': 'photo-1618401471353-b98afee0b2eb',
    'health-tech-wearables-2026': 'photo-1576091160399-112ba8d25d1d',
    'local-llms-running-ai-on-your-hardware': 'photo-1558494949-ef010cbdcc31',
    'nocode-automation-stacks-solopreneurs': 'photo-1551288049-bebda4e38f71',
    'prompt-engineering-that-actually-works': 'photo-1516321318423-f06f85e504b3',
    'remote-work-async-culture-2026': 'photo-1522071820081-009f0129c71c',
    'shadow-ai-enterprise-crisis': 'photo-1563986768609-322da13575f3',
    'side-hustle-ideas-ai-era': 'photo-1554224155-6726b3ff858f',
    'snowflake-openai-200-million-partnership': 'photo-1451187580459-43490279c0fa',
    'snowflake-openai-enterprise-ai-tipping-point': 'photo-1558494949-ef010cbdcc31',
    'why-ai-side-projects-fail': 'photo-1552664730-d307ca884978',
    'why-every-business-needs-ai-strategy-2026': 'photo-1553877522-43269d4ea984',
}

DEFAULT_IMAGE = 'photo-1485827404703-89b55fcc595e'

def extract_metadata(html_content, slug):
    """Extract article metadata from HTML"""
    
    # Title
    title_match = re.search(r'<title>([^|<]+)', html_content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    # Description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    description = desc_match.group(1) if desc_match else ""
    
    # Category - try multiple patterns
    cat_match = re.search(r'class="hero-tag[^"]*">([^<]+)<', html_content)
    if not cat_match:
        cat_match = re.search(r'class="category[^"]*">([^<]+)<', html_content)
    if not cat_match:
        cat_match = re.search(r'class="article-category[^"]*">([^<]+)<', html_content)
    category = cat_match.group(1).strip() if cat_match else "AI Insights"
    
    # Date
    date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', html_content)
    date_str = date_match.group(0) if date_match else "February 7, 2026"
    
    # Read time
    time_match = re.search(r'(\d+)\s*min\s*read', html_content)
    read_time = int(time_match.group(1)) if time_match else 6
    
    return {
        'title': title,
        'description': description,
        'category': category,
        'date': date_str,
        'read_time': read_time,
        'slug': slug
    }

def extract_article_content(html_content):
    """Extract the main article body content"""
    
    # Try to find article content between <article> tags
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL)
    if article_match:
        content = article_match.group(1)
        # Clean up - remove author bio, share section, newsletter CTA, next story, keep reading
        content = re.sub(r'<div class="author-bio.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="share-section.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="share-section.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<section class="newsletter.*?</section>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="inline-cta.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="next-story.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<section class="related-articles.*?</section>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="keep-reading.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = content.strip()
        return content
    
    # Fallback: try to find content div
    content_match = re.search(r'<div class="content[^"]*">(.*?)</div>\s*(?:<div class="share|<footer|</article)', html_content, re.DOTALL)
    if content_match:
        return content_match.group(1).strip()
    
    # Last resort: look for body paragraphs
    paragraphs = re.findall(r'<p[^>]*>.*?</p>', html_content, re.DOTALL)
    if len(paragraphs) > 3:
        return '\n\n'.join(paragraphs[1:])  # Skip first (usually intro in header)
    
    return ""

def get_template():
    """Get the master template from the Remote Work article"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def build_article(metadata, content, template):
    """Build a complete article using the template"""
    
    slug = metadata['slug']
    image_id = ARTICLE_IMAGES.get(slug, DEFAULT_IMAGE)
    og_image = f"https://futurehumanism.co/images/og-{slug}.jpg"
    
    # Check if OG image exists, otherwise use default
    og_image_path = PROJECT_ROOT / "images" / f"og-{slug}.jpg"
    if not og_image_path.exists():
        og_image = "https://futurehumanism.co/images/og-image.jpg"
    
    # Build the HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-W0SQN4JHN2"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-W0SQN4JHN2');
    </script>
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#1E90FF">
    <title>{metadata['title']} | Future Humanism</title>
    <meta name="description" content="{metadata['description']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@FutureHumanism">
    <meta name="twitter:title" content="{metadata['title']}">
    <meta name="twitter:description" content="{metadata['description'][:200]}">
    <meta name="twitter:image" content="{og_image}">
    <meta property="og:title" content="{metadata['title']}">
    <meta property="og:description" content="{metadata['description']}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:url" content="https://futurehumanism.co/articles/{slug}.html">
    <meta property="og:type" content="article">
    <link rel="canonical" href="https://futurehumanism.co/articles/{slug}.html">
    <link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0a0a;
            --bg-secondary: #141414;
            --bg-dark: #000000;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --text-muted: #707070;
            --accent: #1E90FF;
            --accent-hover: #3BA0FF;
            --border: #2a2a2a;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--bg-primary);
            color: var(--text-secondary);
            line-height: 1.7;
        }}
        .progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: var(--accent);
            z-index: 1000;
            transition: width 0.1s;
        }}
        header {{
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            background: rgba(10,10,10,0.95);
            backdrop-filter: blur(10px);
            z-index: 100;
        }}
        .header-inner {{
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text-primary);
        }}
        .logo-icon {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            overflow: hidden;
        }}
        .logo-icon img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .logo-text {{
            font-weight: 700;
            font-size: 1.2rem;
        }}
        .logo-text span {{ font-weight: 400; opacity: 0.6; }}
        .back-link {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 500;
        }}
        .hero {{
            padding: 60px 24px;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.6), rgba(10,10,10,1)), url('https://images.unsplash.com/{image_id}?w=800&q=80') center/cover;
        }}
        .hero-tag {{
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
        }}
        .hero h1 {{
            font-size: clamp(2rem, 5vw, 3rem);
            line-height: 1.15;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 16px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        .hero-meta {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        article {{
            max-width: 700px;
            margin: 0 auto;
            padding: 48px 24px;
        }}
        article h2 {{
            font-size: 1.5rem;
            color: var(--text-primary);
            margin: 40px 0 20px;
            font-weight: 700;
        }}
        article h3 {{
            font-size: 1.25rem;
            color: var(--text-primary);
            margin: 32px 0 16px;
            font-weight: 600;
        }}
        article p {{
            margin-bottom: 20px;
            color: #b0b0b0;
        }}
        article ul, article ol {{
            margin: 0 0 20px 24px;
            color: #b0b0b0;
        }}
        article li {{
            margin-bottom: 10px;
            color: #b0b0b0;
        }}
        article strong {{
            color: var(--text-primary);
        }}
        article a {{
            color: #60a5fa;
            text-decoration: underline;
            text-decoration-thickness: 1px;
            text-underline-offset: 2px;
        }}
        article a:hover {{
            color: var(--accent);
        }}
        .highlight-box {{
            background: var(--bg-secondary);
            border-left: 4px solid var(--accent);
            padding: 24px;
            margin: 32px 0;
            border-radius: 0 8px 8px 0;
        }}
        .highlight-box p {{
            margin: 0;
            color: var(--text-primary);
        }}
        footer {{
            padding: 48px 24px;
            background: var(--bg-secondary);
            text-align: center;
            border-top: 1px solid var(--border);
        }}
        footer a {{
            color: var(--accent);
            text-decoration: none;
        }}
        footer a:hover {{
            text-decoration: underline;
        }}
        footer p {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 1.75rem; }}
            article {{ padding: 32px 20px; }}
        }}
    </style>
</head>
<body>
    <div class="progress-bar" id="progress"></div>
    <header>
        <div class="header-inner">
            <a href="/" class="logo">
                <div class="logo-icon"><img src="../images/profile.jpg" alt="Future Humanism"></div>
                <div class="logo-text">Future<span>Humanism</span></div>
            </a>
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </header>
    
    <div class="hero">
        <span class="hero-tag">{metadata['category']}</span>
        <h1>{metadata['title']}</h1>
        <p class="hero-meta">{metadata['date']} &bull; {metadata['read_time']} min read</p>
    </div>

    <article>
        {content}
    </article>
    
    <footer>
        <p>© 2026 <a href="/">Future Humanism</a> · <a href="https://twitter.com/FutureHumanism" target="_blank">Twitter</a> · <a href="/subscribe.html">Newsletter</a></p>
    </footer>

    <script>
        // Reading progress bar
        window.addEventListener('scroll', () => {{
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrolled = (window.scrollY / docHeight) * 100;
            document.getElementById('progress').style.width = scrolled + '%';
        }});
    </script>
</body>
</html>'''
    
    return html

def main():
    print("Unifying article templates...")
    print("=" * 50)
    
    # Get template
    template = get_template()
    
    processed = 0
    errors = []
    
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        slug = filepath.stem
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Extract metadata and content
            metadata = extract_metadata(html_content, slug)
            content = extract_article_content(html_content)
            
            if not content or len(content) < 200:
                print(f"  ⚠ {slug}: Could not extract content (len={len(content)})")
                errors.append(slug)
                continue
            
            # Build new article
            new_html = build_article(metadata, content, template)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"  ✓ {slug}")
            processed += 1
            
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
            errors.append(slug)
    
    print("")
    print(f"Processed: {processed} articles")
    if errors:
        print(f"Errors: {len(errors)} - {', '.join(errors)}")

if __name__ == '__main__':
    main()
