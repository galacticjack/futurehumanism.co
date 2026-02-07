#!/usr/bin/env python3
"""
Clean rebuild of all articles with ONLY the essential content.
Strips all share buttons, author bios, CTAs, etc.
"""

import re
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"
ARTICLES_JSON = PROJECT_ROOT / "articles.json"

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

def extract_clean_content(html_content):
    """Extract ONLY the real article content - no share buttons, author bios, CTAs"""
    
    # Find article tag content
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL)
    if not article_match:
        return ""
    
    content = article_match.group(1)
    
    # Aggressively remove ALL non-content elements
    patterns_to_remove = [
        r'<div class="top-share.*?</div>\s*</div>\s*</div>',  # top share buttons
        r'<div class="top-share.*?</div>',
        r'<div class="share-section.*?</div>\s*</div>\s*</div>',
        r'<div class="share-section.*?</div>',
        r'<div class="author-bio.*?</div>\s*</div>',
        r'<div class="author-card.*?</div>\s*</div>',
        r'<section class="newsletter.*?</section>',
        r'<div class="inline-cta.*?</div>\s*</div>',
        r'<div class="next-story.*?</div>\s*</div>\s*</div>',
        r'<section class="related-articles.*?</section>',
        r'<div class="keep-reading.*?</div>',
        r'<div class="article-footer.*?</div>',
        r'<div class="cta-box.*?</div>',
        r'<div class="subscribe-box.*?</div>',
        r'<script>.*?</script>',
        r'<style>.*?</style>',
        r'<!--.*?-->',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Keep only: p, h2, h3, ul, ol, li, strong, em, a, div.highlight-box, blockquote
    # Remove any remaining divs that wrap things we don't want
    content = re.sub(r'<div[^>]*class="[^"]*(?:share|author|cta|newsletter|subscribe|follow)[^"]*"[^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content

def extract_metadata(html_content, slug):
    """Extract article metadata"""
    
    title_match = re.search(r'<title>([^|<]+)', html_content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    description = desc_match.group(1) if desc_match else ""
    
    # Category from hero-tag
    cat_match = re.search(r'hero-tag[^>]*>([^<]+)<', html_content)
    if not cat_match:
        cat_match = re.search(r'class="category[^"]*">([^<]+)<', html_content)
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

def build_clean_article(metadata, content):
    """Build article with clean template - NO extras"""
    
    slug = metadata['slug']
    image_id = ARTICLE_IMAGES.get(slug, DEFAULT_IMAGE)
    
    og_image_path = PROJECT_ROOT / "images" / f"og-{slug}.jpg"
    og_image = f"https://futurehumanism.co/images/og-{slug}.jpg" if og_image_path.exists() else "https://futurehumanism.co/images/og-image.jpg"
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-W0SQN4JHN2"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-W0SQN4JHN2');</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <link rel="canonical" href="https://futurehumanism.co/articles/{slug}.html">
    <link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #0a0a0a; --bg2: #141414; --text: #ffffff; --text2: #b0b0b0; --accent: #1E90FF; --border: #2a2a2a; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text2); line-height: 1.7; }}
        .progress {{ position: fixed; top: 0; left: 0; height: 3px; background: var(--accent); z-index: 1000; }}
        header {{ padding: 16px 24px; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: rgba(10,10,10,0.95); backdrop-filter: blur(10px); z-index: 100; }}
        .header-inner {{ max-width: 800px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--text); }}
        .logo-icon {{ width: 32px; height: 32px; border-radius: 50%; overflow: hidden; }}
        .logo-icon img {{ width: 100%; height: 100%; object-fit: cover; }}
        .logo-text {{ font-weight: 700; font-size: 1.2rem; }}
        .logo-text span {{ font-weight: 400; opacity: 0.6; }}
        .back-link {{ color: var(--accent); text-decoration: none; font-weight: 500; }}
        .hero {{ padding: 60px 24px; text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(10,10,10,1)), url('https://images.unsplash.com/{image_id}?w=800&q=80') center/cover; }}
        .hero-tag {{ display: inline-block; background: var(--accent); color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; }}
        .hero h1 {{ font-size: clamp(1.75rem, 5vw, 2.5rem); line-height: 1.2; font-weight: 700; color: var(--text); margin-bottom: 16px; max-width: 800px; margin-left: auto; margin-right: auto; }}
        .hero-meta {{ color: var(--text2); font-size: 0.9rem; }}
        article {{ max-width: 680px; margin: 0 auto; padding: 48px 24px; }}
        article h2 {{ font-size: 1.4rem; color: var(--text); margin: 40px 0 16px; font-weight: 700; }}
        article h3 {{ font-size: 1.2rem; color: var(--text); margin: 32px 0 12px; font-weight: 600; }}
        article p {{ margin-bottom: 20px; }}
        article ul, article ol {{ margin: 0 0 20px 24px; }}
        article li {{ margin-bottom: 8px; }}
        article strong {{ color: var(--text); }}
        article a {{ color: #60a5fa; }}
        article a:hover {{ color: var(--accent); }}
        .highlight-box {{ background: var(--bg2); border-left: 4px solid var(--accent); padding: 20px; margin: 24px 0; border-radius: 0 8px 8px 0; }}
        .highlight-box p {{ margin: 0; color: var(--text); }}
        blockquote {{ border-left: 3px solid var(--accent); padding-left: 20px; margin: 24px 0; font-style: italic; color: var(--text2); }}
        footer {{ padding: 40px 24px; background: var(--bg2); text-align: center; border-top: 1px solid var(--border); }}
        footer a {{ color: var(--accent); text-decoration: none; }}
        footer p {{ color: #707070; font-size: 0.85rem; }}
        @media (max-width: 640px) {{ .hero h1 {{ font-size: 1.5rem; }} article {{ padding: 32px 16px; }} }}
    </style>
</head>
<body>
    <div class="progress" id="progress"></div>
    <header>
        <div class="header-inner">
            <a href="/" class="logo">
                <div class="logo-icon"><img src="../images/profile.jpg" alt=""></div>
                <div class="logo-text">Future<span>Humanism</span></div>
            </a>
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </header>
    
    <div class="hero">
        <span class="hero-tag">{metadata['category']}</span>
        <h1>{metadata['title']}</h1>
        <p class="hero-meta">{metadata['date']} • {metadata['read_time']} min read</p>
    </div>

    <article>
{content}
    </article>
    
    <footer>
        <p>© 2026 <a href="/">Future Humanism</a> · <a href="https://twitter.com/FutureHumanism" target="_blank">Twitter</a> · <a href="/subscribe.html">Newsletter</a></p>
    </footer>

    <script>
        window.addEventListener('scroll', () => {{
            const h = document.documentElement.scrollHeight - window.innerHeight;
            document.getElementById('progress').style.width = (window.scrollY / h * 100) + '%';
        }});
    </script>
</body>
</html>'''

def main():
    print("Clean rebuild of all articles...")
    print("=" * 50)
    
    processed = 0
    
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        slug = filepath.stem
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            metadata = extract_metadata(html, slug)
            content = extract_clean_content(html)
            
            # Ensure content has actual paragraphs
            if content.count('<p') < 3:
                print(f"  ⚠ {slug}: Low content ({content.count('<p')} paragraphs)")
                continue
            
            new_html = build_clean_article(metadata, content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"  ✓ {slug}")
            processed += 1
            
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
    
    print(f"\nRebuilt {processed} articles")

if __name__ == '__main__':
    main()
