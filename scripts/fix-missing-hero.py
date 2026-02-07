#!/usr/bin/env python3
"""Fix articles missing hero section"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"
MASTER_FILE = ARTICLES_DIR / "ai-marketing-strategies-2026.html"

MISSING_HERO = [
    'ai-agent-economy-2027',
    'ai-agents-platform-shift', 
    'ai-computer-control-revolution',
]

IMAGES = {
    'ai-agent-economy-2027': 'photo-1460925895917-afdab827c52f',
    'ai-agents-platform-shift': 'photo-1518770660439-4636190af475',
    'ai-computer-control-revolution': 'photo-1551434678-e076c223a692',
}

def extract_data(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    slug = filepath.stem
    
    title_match = re.search(r'<title>([^|<]+)', content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Try to find category
    cat_patterns = [
        r'hero-tag[^>]*>([^<]+)<',
        r'class="category[^"]*">([^<]+)<',
        r'class="tag[^"]*">([^<]+)<',
        r'<span class="[^"]*category[^"]*">([^<]+)</span>',
    ]
    category = "AI Insights"
    for pattern in cat_patterns:
        cat_match = re.search(pattern, content)
        if cat_match:
            category = cat_match.group(1).strip()
            break
    
    date_match = re.search(r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})', content)
    date_str = date_match.group(1) if date_match else "February 7, 2026"
    
    time_match = re.search(r'(\d+)\s*min', content)
    read_time = time_match.group(1) if time_match else "6"
    
    # Extract article body
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if article_match:
        body = article_match.group(1)
        # Clean up
        body = re.sub(r'<div class="top-share.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="byline.*?</div>', '', body, flags=re.DOTALL)
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

def main():
    with open(MASTER_FILE, 'r') as f:
        master = f.read()
    
    print("Fixing articles missing hero section...")
    
    for slug in MISSING_HERO:
        filepath = ARTICLES_DIR / f"{slug}.html"
        
        try:
            data = extract_data(filepath)
            image_id = IMAGES.get(slug, 'photo-1677442136019-21780ecad995')
            
            og_path = PROJECT_ROOT / "images" / f"og-{slug}.jpg"
            og_image = f"https://futurehumanism.co/images/og-{slug}.jpg" if og_path.exists() else "https://futurehumanism.co/images/og-image.jpg"
            
            # Build new HTML from master
            new_html = master
            
            # Replace metadata
            new_html = re.sub(r'<title>[^<]+</title>', f'<title>{data["title"]} | Future Humanism</title>', new_html)
            new_html = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{data["description"]}"', new_html)
            new_html = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{data["title"]}"', new_html)
            new_html = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{data["description"][:200]}"', new_html)
            new_html = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{og_image}"', new_html)
            new_html = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{data["title"]}"', new_html)
            new_html = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{data["description"]}"', new_html)
            new_html = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{og_image}"', new_html)
            new_html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://futurehumanism.co/articles/{slug}.html"', new_html)
            new_html = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://futurehumanism.co/articles/{slug}.html"', new_html)
            
            # Replace hero
            new_html = re.sub(r"url\('https://images\.unsplash\.com/[^?']+", f"url('https://images.unsplash.com/{image_id}", new_html)
            new_html = re.sub(r'<span class="hero-tag">[^<]+</span>', f'<span class="hero-tag">{data["category"]}</span>', new_html)
            new_html = re.sub(r'(<div class="hero">.*?<h1>)[^<]+(</h1>)', lambda m: f'{m.group(1)}{data["title"]}{m.group(2)}', new_html, flags=re.DOTALL)
            new_html = re.sub(r'<p class="hero-meta">[^<]+</p>', f'<p class="hero-meta">{data["date"]} • {data["read_time"]} min read</p>', new_html)
            
            # Replace article body
            new_html = re.sub(r'(<article>).*?(</article>)', f'\\1\n        {data["body"]}\n    \\2', new_html, flags=re.DOTALL)
            
            # Update share URLs
            new_html = re.sub(r'ai-marketing-strategies-2026\.html', f'{slug}.html', new_html)
            
            with open(filepath, 'w') as f:
                f.write(new_html)
            
            print(f"  ✓ {slug}")
            
        except Exception as e:
            print(f"  ✗ {slug}: {e}")

if __name__ == '__main__':
    main()
