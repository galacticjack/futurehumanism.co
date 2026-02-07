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
    'General': 'strategy'
}

# Stock images by category
IMAGES = {
    'ai-agents': 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=80',
    'ai-models': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=80',
    'automation': 'https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600&q=80',
    'strategy': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&q=80',
    'tutorials': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&q=80',
    'crypto': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=600&q=80',
    'lifestyle': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=80',
}

def generate_story_card(article):
    """Generate HTML for a story card."""
    cat_key = CATEGORY_MAP.get(article['category'], 'strategy')
    img = IMAGES.get(cat_key, IMAGES['strategy'])
    
    # Estimate read time (200 words per minute)
    word_count = len(article.get('description', '').split()) * 10  # Rough estimate
    read_time = max(5, min(15, word_count // 200 + 5))
    
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
    
    print(f"Updated stories grid with {len(top_articles)} articles:")
    for a in top_articles:
        print(f"  - {a['date']}: {a['title'][:50]}...")

if __name__ == '__main__':
    main()
