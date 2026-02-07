#!/usr/bin/env python3
"""
Fix ALL article endings - find content end and replace everything after with clean template
Works regardless of existing structure
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / 'articles'

RELATED_ARTICLES = [
    {'url': '/articles/ai-agents-2026-guide.html', 'title': 'The Complete Guide to AI Agents in 2026', 'desc': 'Everything you need to know about AI agents.', 'cat': 'Guide', 'img': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80'},
    {'url': '/articles/claude-vs-chatgpt-for-coding-2026.html', 'title': 'Claude vs ChatGPT for Coding 2026', 'desc': 'Comparing the top AI coding assistants.', 'cat': 'Comparison', 'img': 'https://images.unsplash.com/photo-1676299081847-824916de030a?w=400&q=80'},
    {'url': '/articles/ai-marketing-strategies-2026.html', 'title': "AI Marketing: What's Working in 2026", 'desc': 'AI strategies delivering real ROI.', 'cat': 'Marketing', 'img': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=400&q=80'},
    {'url': '/articles/best-ai-tools-solopreneurs-2026.html', 'title': 'Best AI Tools for Solopreneurs', 'desc': 'Essential AI tools that save time.', 'cat': 'Tools', 'img': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80'},
]

def get_cards(slug):
    available = [a for a in RELATED_ARTICLES if slug not in a['url']][:4]
    if len(available) < 4:
        available = RELATED_ARTICLES[:4]
    return '\n'.join([f'''                <a href="{a['url']}" class="kr-card">
                    <img src="{a['img']}" alt="{a['title']}" class="kr-img" loading="lazy">
                    <div class="kr-content">
                        <span class="kr-cat">{a['cat']}</span>
                        <h4>{a['title']}</h4>
                        <p>{a['desc']}</p>
                    </div>
                </a>''' for a in available])

ENDING_CSS = '''
        /* Clean article ending styles */
        .share-box { max-width: 900px; margin: 48px auto; padding: 32px 24px 0; border-top: 1px solid var(--border); }
        .share-box h4 { color: var(--text-primary); margin-bottom: 16px; font-size: 1rem; }
        .share-btns { display: flex; gap: 12px; flex-wrap: wrap; }
        .share-btns a, .share-btns button { display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 8px; text-decoration: none; background: var(--bg-secondary); color: var(--text-secondary); font-size: 0.9rem; border: none; cursor: pointer; transition: all 0.2s; }
        .share-btns a:hover, .share-btns button:hover { transform: translateY(-2px); }
        .share-btns .tw:hover { background: #1DA1F2; color: white; }
        .share-btns .li:hover { background: #0077B5; color: white; }
        .share-btns .cp:hover { background: var(--accent); color: white; }
        
        .bio-box { max-width: 900px; margin: 48px auto; padding: 0 24px; }
        .bio-inner { display: flex; gap: 20px; padding: 24px; background: var(--bg-secondary); border-radius: 12px; border: 1px solid var(--border); }
        .bio-avatar svg { width: 56px; height: 56px; }
        .bio-text h4 { color: var(--text-primary); margin-bottom: 8px; font-size: 1.1rem; }
        .bio-text p { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px; }
        .bio-link { display: inline-flex; align-items: center; gap: 6px; color: var(--accent); text-decoration: none; font-size: 0.85rem; font-weight: 500; }
        @media (max-width: 768px) { .bio-inner { flex-direction: column; text-align: center; align-items: center; } }
        
        .kr-section { max-width: 1200px; margin: 48px auto; padding: 0 24px; }
        .kr-section h3 { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 24px; }
        .kr-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
        .kr-card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; text-decoration: none; transition: all 0.2s; }
        .kr-card:hover { border-color: var(--accent); transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .kr-img { width: 100%; height: 140px; object-fit: cover; }
        .kr-content { padding: 16px; }
        .kr-cat { font-size: 0.7rem; font-weight: 600; color: var(--accent); text-transform: uppercase; }
        .kr-card h4 { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); margin: 8px 0; line-height: 1.4; }
        .kr-card p { font-size: 0.8rem; color: var(--text-secondary); margin: 0; }
        @media (max-width: 1024px) { .kr-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { .kr-grid { grid-template-columns: 1fr; } }
        
        .ftr { background: var(--bg-dark); border-top: 1px solid var(--border); padding: 48px 24px 24px; margin-top: 48px; }
        .ftr-inner { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; gap: 40px; flex-wrap: wrap; }
        .ftr-brand { max-width: 280px; }
        .ftr-logo { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); text-decoration: none; display: block; margin-bottom: 12px; }
        .ftr-logo span { font-weight: 400; opacity: 0.6; }
        .ftr-brand p { font-size: 0.85rem; color: var(--text-secondary); }
        .ftr-links { display: flex; gap: 48px; }
        .ftr-col h5 { font-size: 0.75rem; font-weight: 600; color: var(--text-primary); text-transform: uppercase; margin-bottom: 12px; }
        .ftr-col a { display: block; font-size: 0.85rem; color: var(--text-secondary); text-decoration: none; margin-bottom: 8px; }
        .ftr-col a:hover { color: var(--accent); }
        .ftr-btm { max-width: 1200px; margin: 32px auto 0; padding-top: 16px; border-top: 1px solid var(--border); text-align: center; }
        .ftr-btm p { font-size: 0.8rem; color: var(--text-muted); }
        @media (max-width: 768px) { .ftr-inner { flex-direction: column; } .ftr-links { gap: 32px; } }
        
        .sticky-bar { position: fixed; bottom: 0; left: 0; right: 0; background: linear-gradient(90deg, #0a0a0a, #1a1a2e, #0a0a0a); border-top: 1px solid rgba(30,144,255,0.3); padding: 12px 20px; transform: translateY(100%); transition: transform 0.4s; z-index: 9999; }
        .sticky-bar.visible { transform: translateY(0); }
        .sticky-bar.dismissed { display: none; }
        .sticky-inner { max-width: 1000px; margin: 0 auto; display: flex; align-items: center; justify-content: center; gap: 16px; flex-wrap: wrap; }
        .sticky-inner p { color: #fff; font-size: 0.9rem; margin: 0; }
        .sticky-inner strong { color: var(--accent); }
        .sticky-form { display: flex; gap: 8px; }
        .sticky-form input { padding: 8px 14px; border-radius: 6px; border: 1px solid var(--border); background: #0a0a0a; color: #fff; font-size: 0.85rem; }
        .sticky-form button { padding: 8px 16px; border-radius: 6px; border: none; background: var(--accent); color: white; font-weight: 600; cursor: pointer; }
        .sticky-close { background: none; border: none; color: #707070; font-size: 1.2rem; cursor: pointer; }
        @media (max-width: 768px) { .sticky-inner { flex-direction: column; } .sticky-form { width: 100%; } .sticky-form input { flex: 1; } }
'''

def generate_ending(slug):
    cards = get_cards(slug)
    return f'''
    <!-- Share -->
    <div class="share-box">
        <h4>Share This Article</h4>
        <div class="share-btns">
            <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html&via=FutureHumanism" target="_blank" class="tw">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                Share on X
            </a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Ffuturehumanism.co%2Farticles%2F{slug}.html" target="_blank" class="li">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                LinkedIn
            </a>
            <button class="cp" onclick="navigator.clipboard.writeText(window.location.href);this.textContent='Copied!'">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                Copy Link
            </button>
        </div>
    </div>

    <!-- Author -->
    <div class="bio-box">
        <div class="bio-inner">
            <div class="bio-avatar">
                <svg width="56" height="56" viewBox="0 0 100 100" fill="none">
                    <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#FF6B6B"/><stop offset="50%" style="stop-color:#9B59B6"/><stop offset="100%" style="stop-color:#1E90FF"/></linearGradient></defs>
                    <circle cx="50" cy="50" r="45" stroke="url(#g)" stroke-width="4" fill="none"/>
                    <path d="M35 30 Q50 20 65 30 Q75 45 65 60 Q50 75 35 60 Q25 45 35 30" fill="none" stroke="url(#g)" stroke-width="3"/>
                </svg>
            </div>
            <div class="bio-text">
                <h4>Future Humanism</h4>
                <p>Exploring where AI meets human potential. Daily insights on automation, side projects, and building things that matter.</p>
                <a href="https://x.com/FutureHumanism" target="_blank" class="bio-link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    Follow on X
                </a>
            </div>
        </div>
    </div>

    <!-- Keep Reading -->
    <section class="kr-section">
        <h3>Keep Reading</h3>
        <div class="kr-grid">
{cards}
        </div>
    </section>

    <!-- Footer -->
    <footer class="ftr">
        <div class="ftr-inner">
            <div class="ftr-brand">
                <a href="/" class="ftr-logo">Future<span>Humanism</span></a>
                <p>Where AI meets human potential.</p>
            </div>
            <div class="ftr-links">
                <div class="ftr-col"><h5>Content</h5><a href="/articles/">Stories</a><a href="/about.html">About</a></div>
                <div class="ftr-col"><h5>Tools</h5><a href="/tools/">Free Tools</a></div>
                <div class="ftr-col"><h5>Connect</h5><a href="https://x.com/FutureHumanism" target="_blank">Twitter</a></div>
            </div>
        </div>
        <div class="ftr-btm"><p>&copy; 2026 Future Humanism</p></div>
    </footer>

    <!-- Sticky CTA -->
    <div class="sticky-bar" id="stickyBar">
        <div class="sticky-inner">
            <p>⚡ Join <strong>2,000+ builders</strong> getting AI insights</p>
            <form class="sticky-form" action="https://app.beehiiv.com/forms/c7d45ea8-9b86-4677-8bd0-9e3b37e0b1c7/subscribe" method="POST" target="_blank">
                <input type="email" name="email" placeholder="your@email.com" required>
                <button type="submit">Subscribe</button>
            </form>
            <button class="sticky-close" onclick="dismissBar()">×</button>
        </div>
    </div>

    <script>
        window.addEventListener('scroll',()=>{{const p=document.getElementById('progress');if(p)p.style.width=(scrollY/(document.documentElement.scrollHeight-innerHeight)*100)+'%';}});
        (function(){{const b=document.getElementById('stickyBar');if(!b||sessionStorage.getItem('sd'))return;let s=false;window.addEventListener('scroll',()=>{{if(s)return;if(scrollY/(document.body.scrollHeight-innerHeight)>0.3){{b.classList.add('visible');s=true;}}}},{{passive:true}});}})();
        function dismissBar(){{const b=document.getElementById('stickyBar');if(b){{b.classList.remove('visible');b.classList.add('dismissed');sessionStorage.setItem('sd','1');}}}}
    </script>
</body>
</html>'''


def find_content_end(content):
    """Find where article content ends - look for last closing p, ul, ol, or div before any footer/share section"""
    # Try to find </article> first
    match = re.search(r'</article>', content)
    if match:
        return match.end()
    
    # Look for patterns that indicate end of content
    patterns = [
        r'<div class="share',
        r'<!-- Share',
        r'<footer',
        r'<!-- Footer',
        r'<div class="author-bio',
        r'<!-- Author',
        r'<section class="keep-reading',
        r'<!-- Keep Reading',
        r'<div class="sticky',
        r'<!-- Sticky',
    ]
    
    earliest_pos = len(content)
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()
    
    if earliest_pos < len(content):
        return earliest_pos
    
    # Last resort: find last paragraph or list
    last_content = max(
        content.rfind('</p>'),
        content.rfind('</ul>'),
        content.rfind('</ol>'),
        content.rfind('</div>')
    )
    if last_content > 0:
        return last_content + 6  # +6 for </p> or similar
    
    return None


def fix_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = filepath.stem
    
    # Find where content ends
    end_pos = find_content_end(content)
    if not end_pos:
        return False
    
    # Get everything up to content end
    head_content = content[:end_pos]
    
    # Make sure article tag is closed if it was opened
    if '<article>' in head_content or '<article ' in head_content:
        if '</article>' not in head_content:
            head_content += '\n    </article>'
    
    # Add CSS if not present
    if 'Clean article ending styles' not in head_content:
        head_content = head_content.replace('</style>', ENDING_CSS + '\n    </style>', 1)
    
    # Generate ending
    ending = generate_ending(slug)
    
    # Combine
    new_content = head_content + ending
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    print("Fixing ALL article endings...")
    print("=" * 50)
    
    articles = list(ARTICLES_DIR.glob('*.html'))
    articles = [a for a in articles if a.stem not in ('_TEMPLATE', 'index')]
    
    print(f"Found {len(articles)} articles")
    
    fixed = 0
    for article in sorted(articles):
        try:
            if fix_article(article):
                print(f"✓ Fixed: {article.name}")
                fixed += 1
            else:
                print(f"✗ Failed: {article.name}")
        except Exception as e:
            print(f"✗ Error: {article.name} - {e}")
    
    print(f"\nDone! Fixed {fixed}/{len(articles)} articles")


if __name__ == '__main__':
    main()
