#!/usr/bin/env python3
"""
Fix Keep Reading sections - remove ALL old ones and add ONE proper visual section with 4 cards with images
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / 'articles'

# Related articles with images (4 cards for even grid)
RELATED_ARTICLES = [
    {
        'url': '/articles/ai-agents-2026-guide.html',
        'title': 'The Complete Guide to AI Agents in 2026',
        'description': 'Everything you need to know about AI agents and how they work.',
        'category': 'Guide',
        'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80'
    },
    {
        'url': '/articles/claude-vs-chatgpt-for-coding-2026.html',
        'title': 'Claude vs ChatGPT for Coding 2026',
        'description': 'A detailed comparison of the two leading AI coding assistants.',
        'category': 'Comparison',
        'image': 'https://images.unsplash.com/photo-1676299081847-824916de030a?w=400&q=80'
    },
    {
        'url': '/articles/ai-marketing-strategies-2026.html',
        'title': "AI Marketing: What's Working in 2026",
        'description': 'The AI marketing strategies delivering real ROI.',
        'category': 'Marketing',
        'image': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=400&q=80'
    },
    {
        'url': '/articles/best-ai-tools-solopreneurs-2026.html',
        'title': 'Best AI Tools for Solopreneurs',
        'description': 'The essential AI tools that save time and make money.',
        'category': 'Tools',
        'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80'
    },
]


def generate_keep_reading_html(current_slug):
    """Generate visual Keep Reading section with 4 cards"""
    # Filter out current article
    available = [a for a in RELATED_ARTICLES if current_slug not in a['url']]
    # If we filtered out current article, grab one more
    if len(available) < 4:
        extras = [
            {
                'url': '/articles/ai-agent-economy-2027.html',
                'title': 'The AI Agent Economy: 2027 Predictions',
                'description': 'How AI agents will reshape work and opportunities.',
                'category': 'Prediction',
                'image': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80'
            },
            {
                'url': '/articles/future-of-search-after-chatgpt.html',
                'title': 'The Future of Search After ChatGPT',
                'description': 'How AI is changing search behavior forever.',
                'category': 'Search',
                'image': 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=400&q=80'
            }
        ]
        for e in extras:
            if current_slug not in e['url'] and len(available) < 4:
                available.append(e)
    
    selected = available[:4]
    
    cards_html = ''
    for article in selected:
        cards_html += f'''
                <a href="{article['url']}" class="keep-reading-card">
                    <img src="{article['image']}" alt="{article['title']}" class="keep-reading-img" loading="lazy">
                    <div class="keep-reading-content">
                        <span class="keep-reading-cat">{article['category']}</span>
                        <h4>{article['title']}</h4>
                        <p>{article['description']}</p>
                    </div>
                </a>'''
    
    return f'''
    <!-- Keep Reading Section (Visual 4-card grid) -->
    <section class="keep-reading-section">
        <h3>Keep Reading</h3>
        <div class="keep-reading-grid">{cards_html}
        </div>
    </section>
'''


KEEP_READING_CSS = '''
        /* Keep Reading - Visual 4-card grid */
        .keep-reading-section {
            max-width: 1200px;
            margin: 48px auto;
            padding: 0 24px;
        }
        
        .keep-reading-section h3 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 24px;
        }
        
        .keep-reading-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }
        
        .keep-reading-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            text-decoration: none;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
        }
        
        .keep-reading-card:hover {
            border-color: var(--accent);
            transform: translateY(-4px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .keep-reading-img {
            width: 100%;
            height: 140px;
            object-fit: cover;
        }
        
        .keep-reading-content {
            padding: 16px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .keep-reading-cat {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .keep-reading-card h4 {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .keep-reading-card p {
            font-size: 0.8rem;
            color: var(--text-secondary);
            line-height: 1.5;
            margin: 0;
        }
        
        @media (max-width: 1024px) {
            .keep-reading-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 600px) {
            .keep-reading-grid {
                grid-template-columns: 1fr;
            }
            
            .keep-reading-img {
                height: 120px;
            }
        }
'''


def fix_article(filepath):
    """Remove ALL Keep Reading sections and add ONE proper one before footer"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = filepath.stem
    original = content
    
    # Remove ALL variations of Keep Reading / related articles sections
    patterns_to_remove = [
        # Old related-articles style sections
        r'<style>\s*\.related-articles\s*\{[^}]+\}[\s\S]*?</style>',
        r'<!-- Related Articles.*?<!-- End Related Articles -->',
        r'<div class="related-articles">[\s\S]*?</div>\s*</div>\s*</div>',
        # Keep Reading sections (various forms)
        r'<section class="keep-reading-section">[\s\S]*?</section>',
        r'<div class="keep-reading-section">[\s\S]*?</div>\s*</div>\s*</div>',
        # Inline Keep Reading in article body
        r'<div class="related-articles"[^>]*>[\s\S]*?<h3>Keep Reading</h3>[\s\S]*?</div>\s*</div>',
        # Any remaining Keep Reading headers with content
        r'<h3>Keep Reading</h3>\s*<div class="related-grid">[\s\S]*?</div>\s*</div>',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Also clean up any orphaned Keep Reading CSS
    content = re.sub(r'\.keep-reading-section\s*\{[^}]+\}', '', content)
    content = re.sub(r'\.keep-reading-grid\s*\{[^}]+\}', '', content)
    content = re.sub(r'\.keep-reading-card\s*\{[^}]+\}', '', content)
    
    # Add the Keep Reading CSS if not present
    if 'Keep Reading - Visual 4-card grid' not in content:
        content = content.replace('</style>', KEEP_READING_CSS + '\n    </style>', 1)
    
    # Generate new Keep Reading section
    keep_reading_html = generate_keep_reading_html(slug)
    
    # Find where to insert - before the footer
    footer_match = re.search(r'(<footer class="site-footer">|<!-- Footer -->)', content)
    if footer_match:
        insert_pos = footer_match.start()
        content = content[:insert_pos] + keep_reading_html + '\n' + content[insert_pos:]
    else:
        # No footer found, insert before </body>
        content = content.replace('</body>', keep_reading_html + '\n</body>')
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("Fixing Keep Reading sections across all articles...")
    print("=" * 50)
    
    articles = list(ARTICLES_DIR.glob('*.html'))
    articles = [a for a in articles if a.stem != '_TEMPLATE']
    
    print(f"Found {len(articles)} articles")
    
    fixed = 0
    for article in sorted(articles):
        try:
            if fix_article(article):
                print(f"✓ Fixed: {article.name}")
                fixed += 1
            else:
                print(f"- Skipped: {article.name}")
        except Exception as e:
            print(f"✗ Error: {article.name} - {e}")
    
    print(f"\nDone! Fixed {fixed}/{len(articles)} articles")


if __name__ == '__main__':
    main()
