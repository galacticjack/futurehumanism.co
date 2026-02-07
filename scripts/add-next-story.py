#!/usr/bin/env python3
"""Add 'Next Story' navigation to all articles"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"

# CSS for next story navigation
NEXT_STORY_CSS = """
    /* Next Story Navigation */
    .next-story {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 24px;
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin: 24px auto;
        text-decoration: none;
        transition: all 0.2s ease;
        max-width: 800px;
    }
    .next-story:hover {
        border-color: var(--accent);
        background: rgba(30, 144, 255, 0.05);
    }
    .next-story-content {
        flex: 1;
    }
    .next-story-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--accent);
        margin-bottom: 4px;
    }
    .next-story-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.4;
    }
    .next-story-arrow {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--accent);
        flex-shrink: 0;
        margin-left: 16px;
    }
    .next-story-arrow svg {
        width: 24px;
        height: 24px;
        transition: transform 0.2s ease;
    }
    .next-story:hover .next-story-arrow svg {
        transform: translateX(4px);
    }
    @media (max-width: 768px) {
        .next-story {
            padding: 16px 20px;
            margin: 20px 16px;
        }
        .next-story-title {
            font-size: 0.95rem;
        }
    }
"""

def get_article_metadata(filepath):
    """Extract title and date from article"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<title>([^|]+)\s*\|', content)
    title = title_match.group(1).strip() if title_match else filepath.stem.replace('-', ' ').title()
    
    date_match = re.search(r'"datePublished":\s*"([^"]+)"', content)
    date = date_match.group(1)[:10] if date_match else '2026-01-01'
    
    return {'title': title, 'date': date, 'slug': filepath.stem, 'filename': filepath.name}

def get_all_articles():
    """Get all articles sorted by date"""
    articles = []
    for filepath in ARTICLES_DIR.glob('*.html'):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        articles.append(get_article_metadata(filepath))
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

def add_next_story_to_article(filepath, next_article):
    """Add next story navigation to an article"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has next-story
    if 'class="next-story"' in content:
        return False
    
    # Add CSS before </style> 
    style_end = content.find('</style>')
    if style_end == -1:
        return False
    
    content = content[:style_end] + NEXT_STORY_CSS + '\n    ' + content[style_end:]
    
    # Next story HTML
    next_story_html = f'''
    <!-- Next Story Navigation -->
    <a href="{next_article['filename']}" class="next-story">
        <div class="next-story-content">
            <div class="next-story-label">Next Story</div>
            <div class="next-story-title">{next_article['title']}</div>
        </div>
        <div class="next-story-arrow">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
        </div>
    </a>

'''
    
    # Try multiple insertion patterns
    insertion_patterns = [
        # Pattern 1: After author-bio, before related-articles div
        (r'(</a>\s*</div>\s*</div>\s*\n)(\s*<!-- Related Articles -->)', r'\1' + next_story_html + r'\2'),
        (r'(</a>\s*</div>\s*</div>\s*\n)(\s*<div class="related-articles")', r'\1' + next_story_html + r'\2'),
        # Pattern 2: Before related-section (some articles use this)
        (r'(\s*\n)(\s*<div class="related-section">)', r'\1' + next_story_html + r'\2'),
        # Pattern 3: Before Keep Reading h3 inside a div
        (r'(\s*\n)(\s*<div class="related-articles">\s*\n\s*<h3>Keep Reading)', r'\1' + next_story_html + r'\2'),
        # Pattern 4: Just before any related/keep reading section
        (r'(\n\s*)(<div class="related-(?:articles|section)">)', r'\1' + next_story_html.strip() + r'\n\1\2'),
        # Pattern 5: Before footer if no related section
        (r'(\n\s*)(</article>\s*\n\s*<footer>)', r'\1' + next_story_html.strip() + r'\n\1\2'),
    ]
    
    original_content = content
    for pattern, replacement in insertion_patterns:
        new_content = re.sub(pattern, replacement, content, count=1)
        if new_content != content:
            content = new_content
            break
    
    if content == original_content:
        # Last resort: insert before </article>
        article_end = content.rfind('</article>')
        if article_end != -1:
            content = content[:article_end] + next_story_html + content[article_end:]
        else:
            return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("Adding 'Next Story' navigation to articles...")
    
    articles = get_all_articles()
    print(f"  Found {len(articles)} articles")
    
    updated_count = 0
    
    for i, article in enumerate(articles):
        filepath = ARTICLES_DIR / article['filename']
        
        # Next article wraps around
        next_idx = (i + 1) % len(articles)
        next_article = articles[next_idx]
        
        if add_next_story_to_article(filepath, next_article):
            print(f"    ✓ {article['filename']}")
            updated_count += 1
    
    print(f"\n  Updated {updated_count} articles with 'Next Story' navigation")

if __name__ == '__main__':
    main()
