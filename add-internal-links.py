#!/usr/bin/env python3
"""
Internal Linking Automation for FutureHumanism.co
SEO Growth Engine - Adds "Related Articles" section to all articles

This script:
1. Analyzes all articles for keywords/topics
2. Calculates topic similarity between articles
3. Adds a "Related Articles" section with 3 relevant internal links
4. Improves SEO through better site structure and crawlability
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

# Configuration
ARTICLES_DIR = Path("/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co/articles")
ARTICLES_JSON = Path("/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co/articles.json")
NUM_RELATED = 3  # Number of related articles to show

# Topic keywords for matching - weighted terms
TOPIC_KEYWORDS = {
    "ai-agents": ["agent", "agents", "autonomous", "automation", "workflow", "orchestrat", "multi-agent"],
    "enterprise": ["enterprise", "business", "company", "corporate", "strategy", "ROI", "pricing"],
    "llm": ["llm", "language model", "chatgpt", "claude", "gemini", "gpt", "model"],
    "productivity": ["productivity", "workflow", "efficiency", "automate", "save time"],
    "side-projects": ["side project", "side hustle", "passive income", "indie", "solopreneur"],
    "tools": ["tool", "software", "saas", "app", "platform"],
    "future-work": ["future of work", "remote", "async", "career", "job", "employment"],
    "marketing": ["marketing", "content", "seo", "growth", "audience"],
    "technical": ["code", "api", "developer", "infrastructure", "deploy", "build"],
    "money": ["revenue", "income", "monetiz", "pricing", "$", "profit", "cost"],
}

def load_articles_metadata():
    """Load article metadata from articles.json"""
    with open(ARTICLES_JSON, 'r') as f:
        return json.load(f)

def extract_article_text(html_path):
    """Extract text content from an article HTML file for analysis"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title and description from meta tags
    title_match = re.search(r'<title>([^<]+)</title>', content)
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    
    title = title_match.group(1) if title_match else ""
    description = desc_match.group(1) if desc_match else ""
    
    # Extract h1, h2 headings
    headings = re.findall(r'<h[12][^>]*>([^<]+)</h[12]>', content)
    
    # Combine for analysis
    text = f"{title} {description} {' '.join(headings)}".lower()
    return text

def calculate_topic_scores(text):
    """Calculate topic relevance scores for article text"""
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            count = text.count(keyword.lower())
            score += count
        scores[topic] = score
    return scores

def calculate_similarity(scores1, scores2):
    """Calculate similarity between two articles based on topic scores"""
    common_topics = 0
    for topic in scores1:
        if scores1[topic] > 0 and scores2[topic] > 0:
            # Weight by minimum occurrence (shared relevance)
            common_topics += min(scores1[topic], scores2[topic])
    return common_topics

def get_related_articles(current_slug, all_articles, topic_scores):
    """Find the most related articles for a given article"""
    current_scores = topic_scores.get(current_slug, {})
    
    similarities = []
    for article in all_articles:
        if article['slug'] == current_slug:
            continue
        other_scores = topic_scores.get(article['slug'], {})
        sim = calculate_similarity(current_scores, other_scores)
        similarities.append((article, sim))
    
    # Sort by similarity (descending), then by date (newest first)
    similarities.sort(key=lambda x: (x[1], x[0].get('date', '')), reverse=True)
    
    # Return top N related articles
    return [s[0] for s in similarities[:NUM_RELATED]]

def generate_related_section_html(related_articles):
    """Generate the HTML for the related articles section"""
    if not related_articles:
        return ""
    
    cards_html = ""
    for article in related_articles:
        title = article.get('title', 'Untitled')
        # Truncate long titles
        if len(title) > 70:
            title = title[:67] + "..."
        description = article.get('description', '')
        if len(description) > 120:
            description = description[:117] + "..."
        url = article.get('url', f"/articles/{article['slug']}.html")
        category = article.get('category', 'Article')
        
        cards_html += f'''
            <a href="{url}" class="related-card">
                <span class="related-category">{category}</span>
                <h4>{title}</h4>
                <p>{description}</p>
            </a>'''
    
    return f'''
<!-- Related Articles Section - Auto-generated for SEO -->
<style>
.related-articles {{
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border, #2a2a2a);
}}
.related-articles h3 {{
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: var(--text-primary, #ffffff);
}}
.related-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
}}
.related-card {{
    background: var(--bg-secondary, #1a1a1a);
    border: 1px solid var(--border, #2a2a2a);
    border-radius: 12px;
    padding: 1.25rem;
    text-decoration: none;
    transition: all 0.2s ease;
    display: block;
}}
.related-card:hover {{
    border-color: var(--accent, #1E90FF);
    transform: translateY(-2px);
}}
.related-category {{
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent, #1E90FF);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
    display: block;
}}
.related-card h4 {{
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary, #ffffff);
    margin-bottom: 0.5rem;
    line-height: 1.4;
}}
.related-card p {{
    font-size: 0.875rem;
    color: var(--text-secondary, #b0b0b0);
    line-height: 1.5;
    margin: 0;
}}
@media (max-width: 640px) {{
    .related-grid {{
        grid-template-columns: 1fr;
    }}
}}
</style>
<div class="related-articles">
    <h3>Keep Reading</h3>
    <div class="related-grid">{cards_html}
    </div>
</div>
<!-- End Related Articles -->
'''

def add_related_section_to_article(html_path, related_html):
    """Insert the related articles section into an article HTML file"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has related articles section
    if '<!-- Related Articles Section' in content:
        # Remove existing related section
        content = re.sub(
            r'<!-- Related Articles Section.*?<!-- End Related Articles -->\n?',
            '',
            content,
            flags=re.DOTALL
        )
    
    # Find insertion point - before the sticky CTA bar or at end of article
    # Look for the sticky CTA section
    sticky_match = re.search(r'(<style>\s*\.sticky-cta-bar)', content)
    
    if sticky_match:
        # Insert before sticky CTA styles
        insert_pos = sticky_match.start()
        new_content = content[:insert_pos] + related_html + '\n' + content[insert_pos:]
    else:
        # Insert before closing body tag
        new_content = content.replace('</body>', related_html + '\n</body>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("🔗 FutureHumanism Internal Linking Automation")
    print("=" * 50)
    
    # Load article metadata
    articles = load_articles_metadata()
    print(f"📚 Loaded {len(articles)} articles from articles.json")
    
    # Calculate topic scores for all articles
    topic_scores = {}
    for article in articles:
        slug = article['slug']
        html_path = ARTICLES_DIR / f"{slug}.html"
        if html_path.exists():
            text = extract_article_text(html_path)
            topic_scores[slug] = calculate_topic_scores(text)
    
    print(f"📊 Analyzed topic relevance for {len(topic_scores)} articles")
    
    # Process each article
    updated_count = 0
    skipped_count = 0
    
    for article in articles:
        slug = article['slug']
        html_path = ARTICLES_DIR / f"{slug}.html"
        
        if not html_path.exists():
            print(f"⚠️  Skipping {slug} - file not found")
            skipped_count += 1
            continue
        
        # Find related articles
        related = get_related_articles(slug, articles, topic_scores)
        
        if not related:
            print(f"⚠️  Skipping {slug} - no related articles found")
            skipped_count += 1
            continue
        
        # Generate and insert related section
        related_html = generate_related_section_html(related)
        add_related_section_to_article(html_path, related_html)
        
        related_titles = [r['title'][:40] + '...' if len(r['title']) > 40 else r['title'] for r in related]
        print(f"✅ {slug}")
        for t in related_titles:
            print(f"   └─ {t}")
        
        updated_count += 1
    
    print("\n" + "=" * 50)
    print(f"✨ Done! Updated {updated_count} articles with internal links")
    if skipped_count:
        print(f"⚠️  Skipped {skipped_count} articles")
    print("\n💡 SEO Impact:")
    print(f"   - Added {updated_count * NUM_RELATED} internal links total")
    print("   - Improved topic clustering and site structure")
    print("   - Better crawlability for search engines")

if __name__ == "__main__":
    main()
