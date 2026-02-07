#!/usr/bin/env python3
"""
Update the stories grid on the homepage with the latest articles from articles.json.
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_FILE = PROJECT_ROOT / 'index.html'
ARTICLES_JSON = PROJECT_ROOT / 'articles.json'

# Category mapping for data attributes
CATEGORY_MAP = {
    'AI Agents': 'ai-agents',
    'AI Models': 'ai-models',
    'Automation': 'automation',
    'Strategy': 'strategy',
    'Tutorials': 'tutorials',
    'Crypto & DeFi': 'crypto',
    'Crypto': 'crypto',
    'Lifestyle': 'lifestyle',
    'Breaking News': 'ai-agents',
    'General': 'strategy',
    'Enterprise AI': 'enterprise',
    'Enterprise AI Strategy': 'enterprise',
    'AI Tools': 'ai-tools',
    'AI Development': 'ai-models',
    'AI Analysis': 'ai-models',
    'Security Alert': 'security',
    'Future of Work': 'lifestyle',
    'Health & Wellness': 'lifestyle',
    'Deep Dive': 'ai-models',
    'Industry Analysis': 'enterprise',
}

# Unique images per article slug
ARTICLE_IMAGES = {
    '16-ai-agents-built-c-compiler': 'photo-1629654297299-c8506221ca97',
    '2026-year-ai-agents-production': 'photo-1677442136019-21780ecad995',
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
    '50-dollar-tech-stack': 'photo-1498050108023-c5249f4df085',
}

# Fallback by category
CATEGORY_IMAGES = {
    'ai-agents': 'photo-1555949963-ff9fe0c870eb',
    'ai-models': 'photo-1677442136019-21780ecad995',
    'ai-tools': 'photo-1581091226825-a6a2a5aee158',
    'automation': 'photo-1518432031352-d6fc5c10da5a',
    'strategy': 'photo-1552664730-d307ca884978',
    'tutorials': 'photo-1516321318423-f06f85e504b3',
    'crypto': 'photo-1639762681485-074b7f938ba0',
    'lifestyle': 'photo-1522071820081-009f0129c71c',
    'enterprise': 'photo-1553877522-43269d4ea984',
    'security': 'photo-1563986768609-322da13575f3',
}

def get_image_for_article(slug, category):
    """Get unique image for article, fall back to category image."""
    if slug in ARTICLE_IMAGES:
        return f"https://images.unsplash.com/{ARTICLE_IMAGES[slug]}?w=600&q=80"
    
    cat_key = CATEGORY_MAP.get(category, 'strategy')
    photo_id = CATEGORY_IMAGES.get(cat_key, 'photo-1485827404703-89b55fcc595e')
    return f"https://images.unsplash.com/{photo_id}?w=600&q=80"

def generate_story_card(article):
    """Generate HTML for a story card."""
    cat_key = CATEGORY_MAP.get(article['category'], 'strategy')
    img = get_image_for_article(article['slug'], article['category'])
    
    # Read time estimate
    read_time = 6  # Default
    
    return f'''            <a href="articles/{article['slug']}.html" class="grid-story-card" data-category="{cat_key}">
                <img loading="lazy" src="{img}" alt="{article['title'][:50]}">
                <div class="grid-card-content">
                    <span class="grid-card-category">{article['category']}</span>
                    <h3 class="grid-card-title">{article['title'][:60]}{"..." if len(article['title']) > 60 else ""}</h3>
                    <div class="grid-card-meta"><span>{read_time} min read</span></div>
                </div>
            </a>'''

def main():
    # Load articles
    with open(ARTICLES_JSON, 'r') as f:
        articles = json.load(f)
    
    # Sort by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Take top 12 for the grid
    top_articles = articles[:12]
    
    # Generate HTML
    cards_html = '\n'.join(generate_story_card(a) for a in top_articles)
    
    # Read index.html
    with open(INDEX_FILE, 'r') as f:
        content = f.read()
    
    # Find and replace the stories grid content
    pattern = r'(<div class="stories-grid" id="stories-grid">).*?(</div>\s*</section>\s*<!-- Testimonials)'
    replacement = r'\1\n' + cards_html + r'\n        \2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print("Could not find stories grid to update")
        return
    
    # Write back
    with open(INDEX_FILE, 'w') as f:
        f.write(new_content)
    
    print(f"Updated stories grid with {len(top_articles)} articles (unique images)")

if __name__ == '__main__':
    main()
