#!/usr/bin/env python3
"""
Clean Article Structure - Complete rebuild of article endings
Removes ALL duplicate sections and creates ONE clean structure:
1. Article content (</article>)
2. Share Section
3. Author Bio
4. Keep Reading (visual 4-card)
5. Footer
6. Sticky CTA
7. Scripts
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / 'articles'

# Related articles for Keep Reading
RELATED_ARTICLES = [
    {
        'url': '/articles/ai-agents-2026-guide.html',
        'title': 'The Complete Guide to AI Agents in 2026',
        'description': 'Everything you need to know about AI agents.',
        'category': 'Guide',
        'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80'
    },
    {
        'url': '/articles/claude-vs-chatgpt-for-coding-2026.html',
        'title': 'Claude vs ChatGPT for Coding 2026',
        'description': 'Comparing the top AI coding assistants.',
        'category': 'Comparison',
        'image': 'https://images.unsplash.com/photo-1676299081847-824916de030a?w=400&q=80'
    },
    {
        'url': '/articles/ai-marketing-strategies-2026.html',
        'title': "AI Marketing: What's Working in 2026",
        'description': 'AI strategies delivering real ROI.',
        'category': 'Marketing',
        'image': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=400&q=80'
    },
    {
        'url': '/articles/best-ai-tools-solopreneurs-2026.html',
        'title': 'Best AI Tools for Solopreneurs',
        'description': 'Essential AI tools that save time.',
        'category': 'Tools',
        'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80'
    },
]


def get_keep_reading_cards(current_slug):
    """Get 4 Keep Reading cards excluding current article"""
    available = [a for a in RELATED_ARTICLES if current_slug not in a['url']]
    if len(available) < 4:
        available = RELATED_ARTICLES[:4]
    
    cards = ''
    for a in available[:4]:
        cards += f'''
                <a href="{a['url']}" class="keep-reading-card">
                    <img src="{a['image']}" alt="{a['title']}" class="keep-reading-img" loading="lazy">
                    <div class="keep-reading-content">
                        <span class="keep-reading-cat">{a['category']}</span>
                        <h4>{a['title']}</h4>
                        <p>{a['description']}</p>
                    </div>
                </a>'''
    return cards


def generate_article_ending(slug):
    """Generate complete clean article ending"""
    cards = get_keep_reading_cards(slug)
    
    return f'''
    <!-- Share Section -->
    <div class="share-section">
        <h4>Share This Article</h4>
        <div class="share-buttons">
            <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html&via=FutureHumanism" target="_blank" class="share-btn twitter">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                Share on X
            </a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html" target="_blank" class="share-btn linkedin">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                LinkedIn
            </a>
            <button class="share-btn copy" onclick="navigator.clipboard.writeText(window.location.href);this.textContent='Copied!'">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                Copy Link
            </button>
        </div>
    </div>

    <!-- Author Bio -->
    <div class="author-bio-section">
        <div class="author-bio">
            <div class="author-avatar">
                <svg width="48" height="48" viewBox="0 0 100 100" fill="none">
                    <defs>
                        <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#FF6B6B"/>
                            <stop offset="50%" style="stop-color:#9B59B6"/>
                            <stop offset="100%" style="stop-color:#1E90FF"/>
                        </linearGradient>
                    </defs>
                    <circle cx="50" cy="50" r="45" stroke="url(#logoGrad)" stroke-width="4" fill="none"/>
                    <path d="M35 30 Q50 20 65 30 Q75 45 65 60 Q50 75 35 60 Q25 45 35 30" fill="none" stroke="url(#logoGrad)" stroke-width="3"/>
                </svg>
            </div>
            <div class="author-info">
                <h4>Future Humanism</h4>
                <p>Exploring where AI meets human potential. Daily insights on automation, side projects, and building things that matter.</p>
                <a href="https://x.com/FutureHumanism" target="_blank" class="author-link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    Follow on X
                </a>
            </div>
        </div>
    </div>

    <!-- Keep Reading -->
    <section class="keep-reading-section">
        <h3>Keep Reading</h3>
        <div class="keep-reading-grid">{cards}
        </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-inner">
            <div class="footer-brand">
                <a href="/" class="footer-logo">Future<span>Humanism</span></a>
                <p>Where AI meets human potential.</p>
            </div>
            <div class="footer-links">
                <div class="footer-col">
                    <h5>Content</h5>
                    <a href="/articles/">Stories</a>
                    <a href="/about.html">About</a>
                </div>
                <div class="footer-col">
                    <h5>Tools</h5>
                    <a href="/tools/">Free Tools</a>
                </div>
                <div class="footer-col">
                    <h5>Connect</h5>
                    <a href="https://x.com/FutureHumanism" target="_blank">Twitter</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Future Humanism</p>
        </div>
    </footer>

    <!-- Sticky CTA -->
    <div class="sticky-cta-bar" id="stickyCta">
        <div class="sticky-cta-inner">
            <span class="sticky-icon">⚡</span>
            <p>Join <strong>2,000+ builders</strong> getting AI insights weekly</p>
            <form class="sticky-form" action="https://app.beehiiv.com/forms/c7d45ea8-9b86-4677-8bd0-9e3b37e0b1c7/subscribe" method="POST" target="_blank">
                <input type="email" name="email" placeholder="your@email.com" required>
                <button type="submit">Subscribe</button>
            </form>
            <button class="sticky-close" onclick="dismissStickyBar()">×</button>
        </div>
    </div>

    <script>
        window.addEventListener('scroll', () => {{
            const p = document.getElementById('progress');
            if (p) p.style.width = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight) * 100) + '%';
        }});
        (function() {{
            const bar = document.getElementById('stickyCta');
            if (!bar || sessionStorage.getItem('stickyDismissed')) return;
            let shown = false;
            window.addEventListener('scroll', () => {{
                if (shown) return;
                if ((window.scrollY / (document.body.scrollHeight - window.innerHeight)) > 0.3) {{
                    bar.classList.add('visible');
                    shown = true;
                }}
            }}, {{ passive: true }});
        }})();
        function dismissStickyBar() {{
            const bar = document.getElementById('stickyCta');
            if (bar) {{ bar.classList.remove('visible'); bar.classList.add('dismissed'); sessionStorage.setItem('stickyDismissed', 'true'); }}
        }}
    </script>
</body>
</html>'''


# CSS to add
ARTICLE_CSS = '''
        /* Article ending sections */
        .share-section {
            max-width: 900px;
            margin: 48px auto;
            padding: 32px 24px 0;
            border-top: 1px solid var(--border);
        }
        .share-section h4 { color: var(--text-primary); margin-bottom: 16px; font-size: 1rem; }
        .share-buttons { display: flex; gap: 12px; flex-wrap: wrap; }
        .share-btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 8px; text-decoration: none; background: var(--bg-secondary); color: var(--text-secondary); font-size: 0.9rem; border: none; cursor: pointer; transition: all 0.2s; }
        .share-btn:hover { transform: translateY(-2px); }
        .share-btn.twitter:hover { background: #1DA1F2; color: white; }
        .share-btn.linkedin:hover { background: #0077B5; color: white; }
        .share-btn.copy:hover { background: var(--accent); color: white; }
        
        .author-bio-section { max-width: 900px; margin: 48px auto; padding: 0 24px; }
        .author-bio { display: flex; gap: 20px; padding: 24px; background: var(--bg-secondary); border-radius: 12px; border: 1px solid var(--border); }
        .author-avatar svg { width: 56px; height: 56px; }
        .author-info h4 { color: var(--text-primary); margin-bottom: 8px; font-size: 1.1rem; }
        .author-info p { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.5; }
        .author-link { display: inline-flex; align-items: center; gap: 6px; color: var(--accent); text-decoration: none; font-size: 0.85rem; font-weight: 500; }
        .author-link:hover { color: var(--accent-hover); }
        @media (max-width: 768px) { .author-bio { flex-direction: column; text-align: center; align-items: center; } }
        
        .keep-reading-section { max-width: 1200px; margin: 48px auto; padding: 0 24px; }
        .keep-reading-section h3 { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 24px; }
        .keep-reading-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
        .keep-reading-card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; text-decoration: none; transition: all 0.2s; }
        .keep-reading-card:hover { border-color: var(--accent); transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .keep-reading-img { width: 100%; height: 140px; object-fit: cover; }
        .keep-reading-content { padding: 16px; }
        .keep-reading-cat { font-size: 0.7rem; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px; }
        .keep-reading-card h4 { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); margin: 8px 0; line-height: 1.4; }
        .keep-reading-card p { font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin: 0; }
        @media (max-width: 1024px) { .keep-reading-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { .keep-reading-grid { grid-template-columns: 1fr; } }
        
        .site-footer { background: var(--bg-dark); border-top: 1px solid var(--border); padding: 48px 24px 24px; margin-top: 48px; }
        .footer-inner { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; gap: 40px; flex-wrap: wrap; }
        .footer-brand { max-width: 280px; }
        .footer-logo { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); text-decoration: none; display: block; margin-bottom: 12px; }
        .footer-logo span { font-weight: 400; opacity: 0.6; }
        .footer-brand p { font-size: 0.85rem; color: var(--text-secondary); }
        .footer-links { display: flex; gap: 48px; }
        .footer-col h5 { font-size: 0.75rem; font-weight: 600; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
        .footer-col a { display: block; font-size: 0.85rem; color: var(--text-secondary); text-decoration: none; margin-bottom: 8px; }
        .footer-col a:hover { color: var(--accent); }
        .footer-bottom { max-width: 1200px; margin: 32px auto 0; padding-top: 16px; border-top: 1px solid var(--border); text-align: center; }
        .footer-bottom p { font-size: 0.8rem; color: var(--text-muted); }
        @media (max-width: 768px) { .footer-inner { flex-direction: column; } .footer-links { gap: 32px; } }
        
        .sticky-cta-bar { position: fixed; bottom: 0; left: 0; right: 0; background: linear-gradient(90deg, #0a0a0a, #1a1a2e, #0a0a0a); border-top: 1px solid rgba(30,144,255,0.3); padding: 12px 20px; transform: translateY(100%); transition: transform 0.4s; z-index: 9999; }
        .sticky-cta-bar.visible { transform: translateY(0); }
        .sticky-cta-bar.dismissed { display: none; }
        .sticky-cta-inner { max-width: 1000px; margin: 0 auto; display: flex; align-items: center; justify-content: center; gap: 16px; flex-wrap: wrap; }
        .sticky-icon { font-size: 1.3rem; }
        .sticky-cta-inner p { color: #fff; font-size: 0.9rem; margin: 0; }
        .sticky-cta-inner strong { color: var(--accent); }
        .sticky-form { display: flex; gap: 8px; }
        .sticky-form input { padding: 8px 14px; border-radius: 6px; border: 1px solid var(--border); background: #0a0a0a; color: #fff; font-size: 0.85rem; }
        .sticky-form button { padding: 8px 16px; border-radius: 6px; border: none; background: var(--accent); color: white; font-weight: 600; font-size: 0.85rem; cursor: pointer; }
        .sticky-close { background: none; border: none; color: #707070; font-size: 1.2rem; cursor: pointer; margin-left: 8px; }
        @media (max-width: 768px) { .sticky-cta-inner { flex-direction: column; gap: 10px; } .sticky-form { width: 100%; } .sticky-form input { flex: 1; } }
'''


def clean_article(filepath):
    """Completely rebuild article ending"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = filepath.stem
    
    # Find </article> tag
    article_match = re.search(r'</article>', content)
    if not article_match:
        print(f"  No </article> tag found in {filepath.name}")
        return False
    
    # Keep everything up to and including </article>
    head_and_article = content[:article_match.end()]
    
    # Add CSS if not present
    if 'Article ending sections' not in head_and_article:
        head_and_article = head_and_article.replace('</style>', ARTICLE_CSS + '\n    </style>', 1)
    
    # Generate clean ending
    ending = generate_article_ending(slug)
    
    # Combine
    new_content = head_and_article + ending
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    print("Cleaning article structure...")
    print("=" * 50)
    
    articles = list(ARTICLES_DIR.glob('*.html'))
    articles = [a for a in articles if a.stem not in ('_TEMPLATE', 'index')]
    
    print(f"Found {len(articles)} articles")
    
    fixed = 0
    for article in sorted(articles):
        try:
            if clean_article(article):
                print(f"✓ Cleaned: {article.name}")
                fixed += 1
        except Exception as e:
            print(f"✗ Error: {article.name} - {e}")
    
    print(f"\nDone! Cleaned {fixed}/{len(articles)} articles")


if __name__ == '__main__':
    main()
