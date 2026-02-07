#!/usr/bin/env python3
"""
Fix articles that have the wrong template (purple theme instead of blue).
Extracts content and rebuilds with the correct template.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"
MASTER_FILE = ARTICLES_DIR / "ai-marketing-strategies-2026.html"

# Articles that need fixing
BROKEN_ARTICLES = [
    '16-ai-agents-built-c-compiler',
    '2026-year-ai-agents-production', 
    'agentic-ai-100-billion-market-2026',
    'ai-agent-security-vulnerabilities-2026',
    'apple-xcode-agentic-coding',
    'automate-freelance-business-ai-guide',
    'best-ai-coding-assistants-beginners-2026',
    'best-ai-tools-solopreneurs-2026',
    'claude-vs-chatgpt-for-coding-2026',
    'github-copilot-vs-cursor-vs-claude-code-2026',
    'shadow-ai-enterprise-crisis',
    'snowflake-openai-200-million-partnership',
]

# Image mapping
ARTICLE_IMAGES = {
    '16-ai-agents-built-c-compiler': 'photo-1629654297299-c8506221ca97',
    '2026-year-ai-agents-production': 'photo-1677442136019-21780ecad995',
    'agentic-ai-100-billion-market-2026': 'photo-1551288049-bebda4e38f71',
    'ai-agent-security-vulnerabilities-2026': 'photo-1563986768609-322da13575f3',
    'apple-xcode-agentic-coding': 'photo-1621839673705-6617adf9e890',
    'automate-freelance-business-ai-guide': 'photo-1460925895917-afdab827c52f',
    'best-ai-coding-assistants-beginners-2026': 'photo-1555949963-ff9fe0c870eb',
    'best-ai-tools-solopreneurs-2026': 'photo-1581091226825-a6a2a5aee158',
    'claude-vs-chatgpt-for-coding-2026': 'photo-1587620962725-abab7fe55159',
    'github-copilot-vs-cursor-vs-claude-code-2026': 'photo-1618401471353-b98afee0b2eb',
    'shadow-ai-enterprise-crisis': 'photo-1563986768609-322da13575f3',
    'snowflake-openai-200-million-partnership': 'photo-1451187580459-43490279c0fa',
}

def get_master_template():
    """Get the full master template"""
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def extract_article_data(filepath):
    """Extract metadata and content from an article"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = filepath.stem
    
    # Title
    title_match = re.search(r'<title>([^|<]+)', content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    # Description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Category from hero-tag or similar
    cat_match = re.search(r'hero-tag[^>]*>([^<]+)<', content)
    if not cat_match:
        cat_match = re.search(r'class="category[^"]*">([^<]+)<', content)
    if not cat_match:
        cat_match = re.search(r'class="tag[^"]*">([^<]+)<', content)
    category = cat_match.group(1).strip() if cat_match else "AI Insights"
    
    # Date
    date_match = re.search(r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})', content)
    date_str = date_match.group(1) if date_match else "February 7, 2026"
    
    # Read time
    time_match = re.search(r'(\d+)\s*min', content)
    read_time = time_match.group(1) if time_match else "6"
    
    # Article body - extract between <article> tags
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if article_match:
        body = article_match.group(1)
        
        # Clean up - remove elements we don't want
        body = re.sub(r'<div class="top-share.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="top-share.*?</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="toc.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="table-of-contents.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<nav class="toc.*?</nav>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="inline-newsletter.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="inline-cta.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="share-section.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="author-bio.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="author-card.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
        body = body.strip()
    else:
        body = "<p>Content not available.</p>"
    
    return {
        'slug': slug,
        'title': title,
        'description': description,
        'category': category,
        'date': date_str,
        'read_time': read_time,
        'body': body
    }

def rebuild_article(data, master_template):
    """Rebuild article using master template structure"""
    
    slug = data['slug']
    image_id = ARTICLE_IMAGES.get(slug, 'photo-1677442136019-21780ecad995')
    
    # Check if OG image exists
    og_path = PROJECT_ROOT / "images" / f"og-{slug}.jpg"
    og_image = f"https://futurehumanism.co/images/og-{slug}.jpg" if og_path.exists() else "https://futurehumanism.co/images/og-image.jpg"
    
    # Start with master template
    new_html = master_template
    
    # Replace title
    new_html = re.sub(r'<title>[^<]+</title>', f'<title>{data["title"]} | Future Humanism</title>', new_html)
    
    # Replace meta description
    new_html = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{data["description"]}"', new_html)
    
    # Replace twitter meta
    new_html = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{data["title"]}"', new_html)
    new_html = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{data["description"][:200]}"', new_html)
    new_html = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{og_image}"', new_html)
    
    # Replace og meta
    new_html = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{data["title"]}"', new_html)
    new_html = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{data["description"]}"', new_html)
    new_html = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{og_image}"', new_html)
    new_html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://futurehumanism.co/articles/{slug}.html"', new_html)
    
    # Replace canonical
    new_html = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://futurehumanism.co/articles/{slug}.html"', new_html)
    
    # Replace hero image
    new_html = re.sub(r"url\('https://images\.unsplash\.com/[^?']+", f"url('https://images.unsplash.com/{image_id}", new_html)
    
    # Replace hero tag (category)
    new_html = re.sub(r'<span class="hero-tag">[^<]+</span>', f'<span class="hero-tag">{data["category"]}</span>', new_html)
    
    # Replace hero h1 title
    new_html = re.sub(r'(<div class="hero">.*?<h1>)[^<]+(</h1>)', 
                      lambda m: f'{m.group(1)}{data["title"]}{m.group(2)}', 
                      new_html, flags=re.DOTALL)
    
    # Replace hero meta (date and read time)
    new_html = re.sub(r'<p class="hero-meta">[^<]+</p>', 
                      f'<p class="hero-meta">{data["date"]} • {data["read_time"]} min read</p>', 
                      new_html)
    
    # Replace article body content
    new_html = re.sub(r'(<article>).*?(</article>)', 
                      f'\\1\n        {data["body"]}\n    \\2', 
                      new_html, flags=re.DOTALL)
    
    # Update share URLs
    new_html = re.sub(r'ai-marketing-strategies-2026\.html', f'{slug}.html', new_html)
    
    return new_html

def main():
    print("Fixing articles with wrong template...")
    print("=" * 60)
    
    # Get master template
    master_template = get_master_template()
    
    fixed = 0
    for slug in BROKEN_ARTICLES:
        filepath = ARTICLES_DIR / f"{slug}.html"
        
        if not filepath.exists():
            print(f"  ⚠ {slug}: File not found")
            continue
        
        try:
            # Extract data
            data = extract_article_data(filepath)
            
            # Rebuild with master template
            new_html = rebuild_article(data, master_template)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"  ✓ {slug}")
            fixed += 1
            
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
    
    print(f"\nFixed {fixed} articles")

if __name__ == '__main__':
    main()
