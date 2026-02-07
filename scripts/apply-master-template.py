#!/usr/bin/env python3
"""
Apply the EXACT template from ai-marketing-strategies-2026.html to ALL articles.
Preserves article content but uses identical CSS, structure, and components.
"""

import re
from pathlib import Path
import html

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"
MASTER_TEMPLATE = ARTICLES_DIR / "ai-marketing-strategies-2026.html"

# Image mapping for each article
ARTICLE_IMAGES = {
    '16-ai-agents-built-c-compiler': 'photo-1629654297299-c8506221ca97',
    '2026-year-ai-agents-production': 'photo-1677442136019-21780ecad995',
    '50-dollar-tech-stack': 'photo-1498050108023-c5249f4df085',
    'agent-infrastructure-orchestration-2026': 'photo-1558494949-ef010cbdcc31',
    'agentic-ai-100-billion-market-2026': 'photo-1551288049-bebda4e38f71',
    'ai-agent-economy-2027': 'photo-1460925895917-afdab827c52f',
    'ai-agent-security-vulnerabilities-2026': 'photo-1563986768609-322da13575f3',
    'ai-agents-2026-guide': 'photo-1677442136019-21780ecad995',
    'ai-agents-eating-software': 'photo-1620712943543-bcc4688e7485',
    'ai-agents-memory': 'photo-1485827404703-89b55fcc595e',
    'ai-agents-platform-shift': 'photo-1518770660439-4636190af475',
    'ai-computer-control-revolution': 'photo-1551434678-e076c223a692',
    'ai-marketing-strategies-2026': 'photo-1533750349088-cd871a92f312',
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

DEFAULT_IMAGE = 'photo-1677442136019-21780ecad995'

def extract_article_data(filepath):
    """Extract key data from an article"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = filepath.stem
    
    # Title
    title_match = re.search(r'<title>([^|<]+)', content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    # Description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Category from hero-tag
    cat_match = re.search(r'hero-tag[^>]*>([^<]+)<', content)
    if not cat_match:
        cat_match = re.search(r'class="category[^"]*">([^<]+)<', content)
    category = cat_match.group(1).strip() if cat_match else "AI Insights"
    
    # Date
    date_match = re.search(r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})', content)
    date_str = date_match.group(1) if date_match else "February 7, 2026"
    
    # Read time
    time_match = re.search(r'(\d+)\s*min', content)
    read_time = time_match.group(1) if time_match else "6"
    
    # Article body content - extract from <article> to </article>
    # But we need to strip out share buttons, inline CTAs, author bios, etc.
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if article_match:
        body = article_match.group(1)
        
        # Remove all the extra stuff we don't want
        body = re.sub(r'<div class="top-share.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="top-share.*?</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="inline-newsletter-cta.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="inline-newsletter.*?</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="inline-cta.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="cta-box.*?</div>\s*</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<div class="cta-box.*?</div>', '', body, flags=re.DOTALL)
        body = re.sub(r'<script>.*?</script>', '', body, flags=re.DOTALL)
        
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

def get_master_template():
    """Extract the template structure from the master file"""
    with open(MASTER_TEMPLATE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get everything from start to just before <article>
    head_match = re.search(r'(<!DOCTYPE html>.*?<article[^>]*>)', content, re.DOTALL)
    head_template = head_match.group(1) if head_match else ""
    
    # Get everything from </article> to end
    tail_match = re.search(r'(</article>.*?</html>)', content, re.DOTALL)
    tail_template = tail_match.group(1) if tail_match else ""
    
    # Remove duplicate newsletter bars from tail
    # Keep only one sticky CTA at the very end
    tail_template = re.sub(r'(<div class="sticky-cta-bar.*?</script>)(?=.*?<div class="sticky-cta-bar)', '', tail_template, flags=re.DOTALL)
    
    return head_template, tail_template

def build_article(data, head_template, tail_template):
    """Build a complete article using the master template"""
    
    slug = data['slug']
    image_id = ARTICLE_IMAGES.get(slug, DEFAULT_IMAGE)
    
    # Check if OG image exists
    og_image_path = PROJECT_ROOT / "images" / f"og-{slug}.jpg"
    if og_image_path.exists():
        og_image = f"https://futurehumanism.co/images/og-{slug}.jpg"
    else:
        og_image = "https://futurehumanism.co/images/og-image.jpg"
    
    # Create the head with article-specific values
    head = head_template
    
    # Replace title
    head = re.sub(r'<title>[^<]+</title>', f'<title>{data["title"]} | Future Humanism</title>', head)
    
    # Replace meta description
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{data["description"]}"', head)
    
    # Replace twitter meta
    head = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{data["title"]}"', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{data["description"][:200]}"', head)
    head = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{og_image}"', head)
    
    # Replace og meta
    head = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{data["title"]}"', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{data["description"]}"', head)
    head = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{og_image}"', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://futurehumanism.co/articles/{slug}.html"', head)
    
    # Replace canonical
    head = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://futurehumanism.co/articles/{slug}.html"', head)
    
    # Replace hero image
    head = re.sub(r"url\('https://images\.unsplash\.com/[^?']+", f"url('https://images.unsplash.com/{image_id}", head)
    
    # Replace hero tag (category)
    head = re.sub(r'<span class="hero-tag">([^<]+)</span>', f'<span class="hero-tag">{data["category"]}</span>', head)
    
    # Replace hero title
    head = re.sub(r'(<div class="hero">.*?<h1>)[^<]+(</h1>)', lambda m: f'{m.group(1)}{data["title"]}{m.group(2)}', head, flags=re.DOTALL)
    
    # Replace hero meta (date and read time)
    head = re.sub(r'<p class="hero-meta">[^<]+</p>', f'<p class="hero-meta">{data["date"]} • {data["read_time"]} min read</p>', head)
    
    # Remove FAQ schema (it's specific to each article)
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema\.org",\s*"@type": "FAQPage".*?</script>', '', head, flags=re.DOTALL)
    
    # Build tail with article-specific share URLs
    tail = tail_template
    encoded_url = f"https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html"
    tail = re.sub(r'ai-marketing-strategies-2026\.html', f'{slug}.html', tail)
    
    # Build final HTML
    article_html = f"{head}\n        {data['body']}\n    </article>{tail}"
    
    return article_html

def main():
    print("Applying master template to all articles...")
    print("=" * 60)
    
    # Get the master template
    head_template, tail_template = get_master_template()
    
    processed = 0
    errors = []
    
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        slug = filepath.stem
        
        try:
            # Extract data from current article
            data = extract_article_data(filepath)
            
            # Check if we got meaningful content
            if len(data['body']) < 200:
                print(f"  ⚠ {slug}: Very short content ({len(data['body'])} chars)")
            
            # Build new article with master template
            new_html = build_article(data, head_template, tail_template)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"  ✓ {slug}")
            processed += 1
            
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
            errors.append(slug)
    
    print("")
    print(f"Applied template to {processed} articles")
    if errors:
        print(f"Errors: {len(errors)}")

if __name__ == '__main__':
    main()
