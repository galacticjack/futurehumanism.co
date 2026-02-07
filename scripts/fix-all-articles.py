#!/usr/bin/env python3
"""
FutureHumanism Article Template Fixer
=====================================
Fixes all article issues and applies consistent template across ALL articles.

Issues to fix:
1. Author bio - proper FH gradient logo icon (not "GJ" placeholder)
2. Author bio - add nice X profile link
3. Floating social share buttons - remove or fix positioning
4. Article container - widen for large screens (max-width: 900px)
5. "Keep Reading" - add images, fix grid alignment (always 3 columns)
6. Footer - fix broken layout, add proper footer
7. Remove duplicate "Keep Reading" sections
8. Ensure consistent styling across all articles
"""

import os
import re
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / 'articles'

# The proper FH gradient logo SVG (matches nav)
FH_LOGO_SVG = '''<svg width="48" height="48" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="authorLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#FF6B6B"/>
            <stop offset="50%" style="stop-color:#9B59B6"/>
            <stop offset="100%" style="stop-color:#1E90FF"/>
        </linearGradient>
    </defs>
    <circle cx="50" cy="50" r="45" stroke="url(#authorLogoGrad)" stroke-width="4" fill="none"/>
    <path d="M35 30 Q50 20 65 30 Q75 45 65 60 Q50 75 35 60 Q25 45 35 30" fill="none" stroke="url(#authorLogoGrad)" stroke-width="3"/>
    <circle cx="42" cy="42" r="4" fill="url(#authorLogoGrad)"/>
    <circle cx="58" cy="42" r="4" fill="url(#authorLogoGrad)"/>
    <path d="M40 55 Q50 62 60 55" fill="none" stroke="url(#authorLogoGrad)" stroke-width="2.5" stroke-linecap="round"/>
</svg>'''

# New author bio section with proper logo and X link
AUTHOR_BIO_SECTION = f'''
    <!-- Author Bio -->
    <div class="author-bio-container">
        <div class="author-bio">
            <div class="author-avatar-wrapper">
                {FH_LOGO_SVG}
            </div>
            <div class="author-info">
                <h4>Future Humanism</h4>
                <p>Exploring where AI meets human potential. Daily insights on automation, side projects, and building things that matter.</p>
                <a href="https://x.com/FutureHumanism" target="_blank" rel="noopener" class="author-x-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    Follow on X
                </a>
            </div>
        </div>
    </div>
'''

# Proper footer
FOOTER_HTML = '''
    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-inner">
            <div class="footer-brand">
                <a href="/" class="footer-logo">
                    <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="footerLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#FF6B6B"/>
                                <stop offset="50%" style="stop-color:#9B59B6"/>
                                <stop offset="100%" style="stop-color:#1E90FF"/>
                            </linearGradient>
                        </defs>
                        <circle cx="50" cy="50" r="45" stroke="url(#footerLogoGrad)" stroke-width="4" fill="none"/>
                        <path d="M35 30 Q50 20 65 30 Q75 45 65 60 Q50 75 35 60 Q25 45 35 30" fill="none" stroke="url(#footerLogoGrad)" stroke-width="3"/>
                        <circle cx="42" cy="42" r="4" fill="url(#footerLogoGrad)"/>
                        <circle cx="58" cy="42" r="4" fill="url(#footerLogoGrad)"/>
                        <path d="M40 55 Q50 62 60 55" fill="none" stroke="url(#footerLogoGrad)" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                    <span>Future<span class="light">Humanism</span></span>
                </a>
                <p class="footer-tagline">Where AI meets human potential. Stories, tools, and insights for builders navigating the most interesting time in tech history.</p>
            </div>
            <div class="footer-links">
                <div class="footer-column">
                    <h5>Content</h5>
                    <a href="/articles/">Stories</a>
                    <a href="https://futurehumanism.beehiiv.com" target="_blank">Newsletter</a>
                    <a href="/about.html">About</a>
                </div>
                <div class="footer-column">
                    <h5>Products</h5>
                    <a href="https://gumroad.com/futurehumanism" target="_blank">AI Prompt Playbook</a>
                    <a href="/tools/">Free Tools</a>
                </div>
                <div class="footer-column">
                    <h5>Connect</h5>
                    <a href="https://x.com/FutureHumanism" target="_blank">Twitter</a>
                    <a href="https://futurehumanism.beehiiv.com" target="_blank">Beehiiv</a>
                    <a href="https://gumroad.com/futurehumanism" target="_blank">Gumroad</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Future Humanism. All rights reserved.</p>
        </div>
    </footer>
'''

# CSS additions for fixes
ADDITIONAL_CSS = '''
        /* === ARTICLE TEMPLATE FIXES === */
        
        /* 1. Wider article container on large screens */
        article {
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 24px;
        }
        
        @media (min-width: 1200px) {
            article {
                max-width: 900px;
            }
        }
        
        /* 2. Author bio with proper logo and X link */
        .author-bio-container {
            max-width: 900px;
            margin: 48px auto;
            padding: 0 24px;
        }
        
        .author-bio {
            display: flex;
            gap: 20px;
            padding: 24px;
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
        }
        
        .author-avatar-wrapper {
            flex-shrink: 0;
        }
        
        .author-avatar-wrapper svg {
            width: 56px !important;
            height: 56px !important;
        }
        
        .author-info {
            flex: 1;
        }
        
        .author-info h4 {
            color: var(--text-primary);
            margin-bottom: 8px;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .author-info p {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 12px;
            line-height: 1.5;
        }
        
        .author-x-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--accent);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .author-x-link:hover {
            color: var(--accent-hover);
        }
        
        .author-x-link svg {
            width: 14px !important;
            height: 14px !important;
        }
        
        @media (max-width: 768px) {
            .author-bio {
                flex-direction: column;
                text-align: center;
                align-items: center;
            }
            
            .author-info {
                text-align: center;
            }
        }
        
        /* 3. Keep Reading section with images */
        .keep-reading-section {
            max-width: 1200px;
            margin: 60px auto;
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
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
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
        
        .keep-reading-card-image {
            width: 100%;
            height: 160px;
            object-fit: cover;
            background: var(--bg-dark);
        }
        
        .keep-reading-card-content {
            padding: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .keep-reading-card-category {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .keep-reading-card h4 {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .keep-reading-card p {
            font-size: 0.875rem;
            color: var(--text-secondary);
            line-height: 1.5;
            margin: 0;
            flex: 1;
        }
        
        @media (max-width: 1024px) {
            .keep-reading-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 640px) {
            .keep-reading-grid {
                grid-template-columns: 1fr;
            }
            
            .keep-reading-card-image {
                height: 140px;
            }
        }
        
        /* 4. Proper footer styling */
        .site-footer {
            background: var(--bg-dark);
            border-top: 1px solid var(--border);
            padding: 60px 24px 30px;
            margin-top: 60px;
        }
        
        .footer-inner {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.5fr 2fr;
            gap: 60px;
        }
        
        .footer-brand {
            max-width: 300px;
        }
        
        .footer-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text-primary);
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 16px;
        }
        
        .footer-logo svg {
            width: 32px !important;
            height: 32px !important;
        }
        
        .footer-logo .light {
            font-weight: 400;
            opacity: 0.6;
        }
        
        .footer-tagline {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.6;
        }
        
        .footer-links {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
        }
        
        .footer-column h5 {
            color: var(--text-primary);
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }
        
        .footer-column a {
            display: block;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            margin-bottom: 10px;
            transition: color 0.2s;
        }
        
        .footer-column a:hover {
            color: var(--accent);
        }
        
        .footer-bottom {
            max-width: 1200px;
            margin: 40px auto 0;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            text-align: center;
        }
        
        .footer-bottom p {
            color: var(--text-muted);
            font-size: 0.85rem;
        }
        
        @media (max-width: 768px) {
            .footer-inner {
                grid-template-columns: 1fr;
                gap: 40px;
            }
            
            .footer-brand {
                max-width: none;
                text-align: center;
            }
            
            .footer-links {
                grid-template-columns: repeat(3, 1fr);
                text-align: center;
            }
        }
        
        @media (max-width: 480px) {
            .footer-links {
                grid-template-columns: 1fr;
                gap: 30px;
            }
        }
        
        /* 5. Remove floating social share buttons from sidebar */
        .floating-share-buttons,
        .social-sidebar,
        .share-sidebar {
            display: none !important;
        }
'''

# Related articles data (we'll use this for Keep Reading sections)
RELATED_ARTICLES = [
    {
        'url': '/articles/ai-agents-2026-guide.html',
        'title': 'The Complete Guide to AI Agents in 2026',
        'description': 'Everything you need to know about AI agents and how they work.',
        'category': 'Guide',
        'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80'
    },
    {
        'url': '/articles/claude-vs-chatgpt-2026.html',
        'title': 'Claude vs ChatGPT: The 2026 AI Showdown',
        'description': 'A detailed comparison of the two leading AI assistants.',
        'category': 'Comparison',
        'image': 'https://images.unsplash.com/photo-1676299081847-824916de030a?w=400&q=80'
    },
    {
        'url': '/articles/ai-agent-economy-2027.html',
        'title': 'The AI Agent Economy: 2027 Predictions',
        'description': 'How AI agents will reshape work and create new opportunities.',
        'category': 'Prediction',
        'image': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80'
    },
    {
        'url': '/articles/ai-marketing-strategies-2026.html',
        'title': "AI Marketing in 2026: What's Working",
        'description': 'The AI marketing strategies delivering real ROI.',
        'category': 'Marketing',
        'image': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=400&q=80'
    },
    {
        'url': '/articles/best-ai-tools-2026.html',
        'title': 'Best AI Tools in 2026',
        'description': 'The essential AI tools that are actually worth using.',
        'category': 'Tools',
        'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80'
    },
    {
        'url': '/articles/future-of-search-after-chatgpt.html',
        'title': 'The Future of Search After ChatGPT',
        'description': 'How AI is fundamentally changing search behavior.',
        'category': 'Search Evolution',
        'image': 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=400&q=80'
    }
]


def generate_keep_reading_section(current_slug):
    """Generate Keep Reading section with 3 related articles (excluding current)"""
    # Filter out current article and pick 3
    available = [a for a in RELATED_ARTICLES if current_slug not in a['url']]
    selected = available[:3]
    
    if len(selected) < 3:
        # If we don't have enough, just repeat from beginning
        selected = RELATED_ARTICLES[:3]
    
    cards_html = ''
    for article in selected:
        cards_html += f'''
            <a href="{article['url']}" class="keep-reading-card">
                <img src="{article['image']}" alt="{article['title']}" class="keep-reading-card-image" loading="lazy">
                <div class="keep-reading-card-content">
                    <span class="keep-reading-card-category">{article['category']}</span>
                    <h4>{article['title']}</h4>
                    <p>{article['description']}</p>
                </div>
            </a>'''
    
    return f'''
    <!-- Keep Reading Section -->
    <div class="keep-reading-section">
        <h3>Keep Reading</h3>
        <div class="keep-reading-grid">{cards_html}
        </div>
    </div>
'''


def fix_article(filepath):
    """Fix a single article with all template improvements"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = filepath.stem
    modified = False
    
    # 1. Add additional CSS before </style> (if not already present)
    if 'ARTICLE TEMPLATE FIXES' not in content:
        content = content.replace('</style>', ADDITIONAL_CSS + '\n    </style>')
        modified = True
    
    # 2. Remove old author-bio sections and floating social share
    # Remove old author-bio divs (various patterns)
    old_author_patterns = [
        r'<div class="author-bio"[^>]*>.*?</div>\s*</div>',  # nested
        r'<div class="author-bio"[^>]*>.*?</div>',  # simple
    ]
    for pattern in old_author_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            modified = True
    
    # 3. Remove duplicate Keep Reading / related-articles sections (keep only one)
    # Count how many Keep Reading sections exist
    keep_reading_count = len(re.findall(r'<div class="(?:keep-reading-section|related-articles)"', content))
    if keep_reading_count > 1:
        # Remove ALL Keep Reading sections - we'll add a fresh one
        content = re.sub(r'<div class="related-articles">.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Related Articles.*?<!-- End Related Articles -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="keep-reading-section">.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        modified = True
    
    # Also remove the old style block for related-articles if duplicated
    content = re.sub(r'<style>\s*\.related-articles\s*\{[^}]+\}[^<]*</style>', '', content, count=10)
    
    # 4. Find where to insert new sections (before </body>)
    # First, let's clean up by removing old footer patterns
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
    
    # 5. Build the new ending sections
    keep_reading = generate_keep_reading_section(slug)
    new_ending = f'''
    <!-- Share Section -->
    <div class="share-section" style="max-width: 900px; margin: 48px auto; padding: 0 24px;">
        <h4 style="color: var(--text-primary); margin-bottom: 16px; font-size: 1rem;">Share This Article</h4>
        <div class="share-buttons" style="display: flex; gap: 12px; flex-wrap: wrap;">
            <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html&via=FutureHumanism" target="_blank" class="share-btn twitter" style="display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 8px; text-decoration: none; background: var(--bg-secondary); color: var(--text-secondary); font-size: 0.9rem; transition: all 0.2s;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                Share on X
            </a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html" target="_blank" class="share-btn linkedin" style="display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 8px; text-decoration: none; background: var(--bg-secondary); color: var(--text-secondary); font-size: 0.9rem; transition: all 0.2s;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                LinkedIn
            </a>
            <button class="share-btn copy" onclick="navigator.clipboard.writeText(window.location.href);this.textContent='Copied!'" style="display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 8px; background: var(--bg-secondary); color: var(--text-secondary); font-size: 0.9rem; border: none; cursor: pointer; transition: all 0.2s;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                Copy Link
            </button>
        </div>
    </div>

{AUTHOR_BIO_SECTION}

{keep_reading}

{FOOTER_HTML}

    <!-- Sticky CTA Bar -->
    <div class="sticky-cta-bar" id="stickyCta">
        <div class="sticky-cta-inner">
            <div class="sticky-cta-text">
                <span class="icon">⚡</span>
                <p>Join <strong>2,000+ builders</strong> getting AI insights weekly</p>
            </div>
            <form class="sticky-cta-form" action="https://app.beehiiv.com/forms/c7d45ea8-9b86-4677-8bd0-9e3b37e0b1c7/subscribe" method="POST" target="_blank">
                <input type="email" name="email" placeholder="your@email.com" required>
                <button type="submit">Subscribe</button>
            </form>
            <button class="sticky-cta-close" onclick="dismissStickyBar()" aria-label="Close">&times;</button>
        </div>
    </div>

    <script>
        // Progress bar
        window.addEventListener('scroll', () => {{
            const scroll = window.scrollY;
            const height = document.documentElement.scrollHeight - window.innerHeight;
            const progress = document.getElementById('progress');
            if (progress) progress.style.width = (scroll / height * 100) + '%';
        }});
        
        // Sticky CTA bar
        (function() {{
            const stickyBar = document.getElementById('stickyCta');
            if (!stickyBar) return;
            if (sessionStorage.getItem('stickyCtaDismissed')) {{
                stickyBar.classList.add('dismissed');
                return;
            }}
            let hasShown = false;
            function checkScroll() {{
                if (hasShown) return;
                const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
                if (scrollPercent > 30) {{
                    stickyBar.classList.add('visible');
                    hasShown = true;
                }}
            }}
            window.addEventListener('scroll', checkScroll, {{ passive: true }});
        }})();
        
        function dismissStickyBar() {{
            const bar = document.getElementById('stickyCta');
            if (bar) {{
                bar.classList.remove('visible');
                bar.classList.add('dismissed');
                sessionStorage.setItem('stickyCtaDismissed', 'true');
            }}
        }}
    </script>
</body>
</html>'''

    # Remove everything from the first share-section to end, then add our new ending
    # Find </article> tag and work from there
    article_end_match = re.search(r'</article>', content)
    if article_end_match:
        # Keep everything up to and including </article>
        content = content[:article_end_match.end()] + new_ending
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Process all articles"""
    print("FutureHumanism Article Template Fixer")
    print("=" * 50)
    
    articles = list(ARTICLES_DIR.glob('*.html'))
    # Exclude template file
    articles = [a for a in articles if a.stem != '_TEMPLATE']
    
    print(f"Found {len(articles)} articles to process")
    
    fixed = 0
    for article in sorted(articles):
        try:
            if fix_article(article):
                print(f"✓ Fixed: {article.name}")
                fixed += 1
            else:
                print(f"- Skipped: {article.name} (no changes needed)")
        except Exception as e:
            print(f"✗ Error: {article.name} - {e}")
    
    print(f"\nDone! Fixed {fixed}/{len(articles)} articles")


if __name__ == '__main__':
    main()
