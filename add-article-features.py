#!/usr/bin/env python3
"""Add author bio, related articles, and enhanced CSS to all articles."""

import os
import re
from pathlib import Path

ARTICLES_DIR = Path.home() / "projects/futurehumanism/articles"

# Related articles for each article (manually curated for relevance)
RELATED_ARTICLES = {
    "ai-agents-memory.html": [
        ("ai-agents-2025-guide.html", "Deep Dive", "The Complete Guide to AI Agents"),
        ("ai-agents-platform-shift.html", "Analysis", "AI Agents: The Next Platform Shift"),
        ("deepseek-r1-vs-openai-o1.html", "Comparison", "DeepSeek R1 vs OpenAI o1"),
    ],
    "deepseek-r1-vs-openai-o1.html": [
        ("claude-vs-gpt-comparison.html", "Comparison", "Claude vs GPT-4"),
        ("ai-agents-memory.html", "Latest", "AI Agents Getting Memory"),
        ("ai-world-models-next-breakthrough.html", "Deep Dive", "World Models: The Next AI Breakthrough"),
    ],
    "ai-agents-platform-shift.html": [
        ("ai-agents-memory.html", "Latest", "AI Agents Getting Memory"),
        ("ai-agent-economy-2027.html", "Future", "The Agent Economy by 2027"),
        ("ai-agents-eating-software.html", "Analysis", "AI Agents Are Eating Software"),
    ],
    "ai-agents-2025-guide.html": [
        ("ai-agents-memory.html", "Latest", "AI Agents Getting Memory"),
        ("claude-vs-gpt-comparison.html", "Comparison", "Claude vs GPT-4"),
        ("automate-80-percent-agency-work.html", "Case Study", "How We Automated 80% of Agency Work"),
    ],
    "claude-vs-gpt-comparison.html": [
        ("deepseek-r1-vs-openai-o1.html", "Comparison", "DeepSeek R1 vs OpenAI o1"),
        ("ai-agents-2025-guide.html", "Deep Dive", "The Complete Guide to AI Agents"),
        ("50-dollar-tech-stack.html", "Tutorial", "The $50/Month Tech Stack"),
    ],
    "why-ai-side-projects-fail.html": [
        ("50-dollar-tech-stack.html", "Tutorial", "The $50/Month Tech Stack"),
        ("automate-80-percent-agency-work.html", "Case Study", "How We Automated 80% of Agency Work"),
        ("ai-agents-2025-guide.html", "Deep Dive", "The Complete Guide to AI Agents"),
    ],
    "automate-80-percent-agency-work.html": [
        ("ai-agents-2025-guide.html", "Deep Dive", "The Complete Guide to AI Agents"),
        ("50-dollar-tech-stack.html", "Tutorial", "The $50/Month Tech Stack"),
        ("why-ai-side-projects-fail.html", "Strategy", "Why Most AI Side Projects Fail"),
    ],
    "ai-agents-eating-software.html": [
        ("ai-agents-platform-shift.html", "Analysis", "AI Agents: The Next Platform Shift"),
        ("ai-agent-economy-2027.html", "Future", "The Agent Economy by 2027"),
        ("ai-agents-memory.html", "Latest", "AI Agents Getting Memory"),
    ],
    "ai-world-models-next-breakthrough.html": [
        ("ai-agents-memory.html", "Latest", "AI Agents Getting Memory"),
        ("deepseek-r1-vs-openai-o1.html", "Comparison", "DeepSeek R1 vs OpenAI o1"),
        ("ai-agents-platform-shift.html", "Analysis", "AI Agents: The Next Platform Shift"),
    ],
    "chatgpt-pro-200-enterprise-ai-shift.html": [
        ("snowflake-openai-enterprise-ai-tipping-point.html", "Breaking", "The $200M Enterprise AI Deal"),
        ("gemini-2-flash-multimodal-ai-dominance.html", "Industry", "Gemini 2.0 Flash Analysis"),
        ("claude-vs-gpt-comparison.html", "Comparison", "Claude vs GPT-4"),
    ],
    "gemini-2-flash-multimodal-ai-dominance.html": [
        ("claude-vs-gpt-comparison.html", "Comparison", "Claude vs GPT-4"),
        ("deepseek-r1-vs-openai-o1.html", "Comparison", "DeepSeek R1 vs OpenAI o1"),
        ("chatgpt-pro-200-enterprise-ai-shift.html", "Enterprise", "ChatGPT Pro at $200/Month"),
    ],
    "snowflake-openai-enterprise-ai-tipping-point.html": [
        ("chatgpt-pro-200-enterprise-ai-shift.html", "Enterprise", "ChatGPT Pro at $200/Month"),
        ("ai-agent-economy-2027.html", "Future", "The Agent Economy by 2027"),
        ("ai-agents-platform-shift.html", "Analysis", "AI Agents: The Next Platform Shift"),
    ],
    "ai-agent-economy-2027.html": [
        ("ai-agents-platform-shift.html", "Analysis", "AI Agents: The Next Platform Shift"),
        ("ai-agents-eating-software.html", "Analysis", "AI Agents Are Eating Software"),
        ("snowflake-openai-enterprise-ai-tipping-point.html", "Breaking", "The $200M Enterprise AI Deal"),
    ],
}

# Image mapping for related cards
ARTICLE_IMAGES = {
    "ai-agents-memory.html": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=400&q=80",
    "deepseek-r1-vs-openai-o1.html": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80",
    "ai-agents-platform-shift.html": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80",
    "ai-agents-2025-guide.html": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80",
    "claude-vs-gpt-comparison.html": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=400&q=80",
    "50-dollar-tech-stack.html": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&q=80",
    "why-ai-side-projects-fail.html": "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=400&q=80",
    "automate-80-percent-agency-work.html": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400&q=80",
    "ai-agents-eating-software.html": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80",
    "ai-world-models-next-breakthrough.html": "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?w=400&q=80",
    "chatgpt-pro-200-enterprise-ai-shift.html": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&q=80",
    "gemini-2-flash-multimodal-ai-dominance.html": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80",
    "snowflake-openai-enterprise-ai-tipping-point.html": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",
    "ai-agent-economy-2027.html": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&q=80",
}

ENHANCED_CSS = '''
    /* Author Bio */
    .author-bio {
        display: flex;
        gap: 20px;
        padding: 32px;
        background: var(--bg-secondary);
        border-radius: 12px;
        margin: 48px 0;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    .author-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid var(--accent);
    }
    .author-info {
        flex: 1;
    }
    .author-info h4 {
        color: var(--text-primary);
        font-size: 1.1rem;
        margin-bottom: 8px;
    }
    .author-info p {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .author-follow {
        color: var(--accent);
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .author-follow:hover {
        text-decoration: underline;
    }
    /* Related Articles */
    .related-articles {
        max-width: 900px;
        margin: 60px auto;
        padding: 0 24px;
    }
    .related-articles h3 {
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 32px;
        color: var(--text-primary);
    }
    .related-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }
    .related-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
        text-decoration: none;
        transition: transform 0.2s, border-color 0.2s;
    }
    .related-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent);
    }
    .related-card img {
        width: 100%;
        aspect-ratio: 16/10;
        object-fit: cover;
    }
    .related-content {
        padding: 16px;
    }
    .related-tag {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--accent);
        margin-bottom: 8px;
    }
    .related-content h4 {
        font-size: 0.95rem;
        color: var(--text-primary);
        line-height: 1.4;
    }
    @media (max-width: 768px) {
        .author-bio {
            flex-direction: column;
            text-align: center;
            padding: 24px;
        }
        .author-avatar {
            margin: 0 auto;
        }
        .related-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }
        .related-articles {
            padding: 0 16px;
        }
    }'''

def generate_author_bio():
    return '''
    <!-- Author Bio -->
    <div class="author-bio">
        <img src="../images/profile.jpg" alt="Author" class="author-avatar">
        <div class="author-info">
            <h4>Written by Future Humanism</h4>
            <p>Exploring where AI meets human potential. Weekly insights on automation, side projects, and building things that matter.</p>
            <a href="https://twitter.com/FutureHumanism" target="_blank" class="author-follow">Follow on X →</a>
        </div>
    </div>'''

def generate_related_articles(filename):
    related = RELATED_ARTICLES.get(filename, [])
    if not related:
        # Default related articles
        related = [
            ("ai-agents-memory.html", "Latest", "AI Agents Getting Memory"),
            ("claude-vs-gpt-comparison.html", "Comparison", "Claude vs GPT-4"),
            ("50-dollar-tech-stack.html", "Tutorial", "The $50/Month Tech Stack"),
        ]
    
    cards = ""
    for href, tag, title in related:
        img = ARTICLE_IMAGES.get(href, "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&q=80")
        cards += f'''
            <a href="{href}" class="related-card">
                <img loading="lazy" src="{img}" alt="{title}">
                <div class="related-content">
                    <span class="related-tag">{tag}</span>
                    <h4>{title}</h4>
                </div>
            </a>'''
    
    return f'''
    <!-- Related Articles -->
    <div class="related-articles">
        <h3>Keep Reading</h3>
        <div class="related-grid">{cards}
        </div>
    </div>'''

def add_features_to_article(filepath):
    filename = filepath.name
    if filename == "index.html":
        return False
    
    print(f"Processing: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has author bio
    if 'author-bio' in content:
        print(f"  Already has features, skipping")
        return False
    
    # Add CSS before </style>
    if '</style>' in content:
        # First check if our CSS is already there
        if 'Author Bio' not in content:
            content = content.replace('</style>', ENHANCED_CSS + '\n    </style>')
    
    # Add author bio and related articles before </article>
    if '</article>' in content:
        author_bio = generate_author_bio()
        related = generate_related_articles(filename)
        content = content.replace('</article>', f'{author_bio}\n{related}\n\n    </article>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Added features!")
    return True

def main():
    count = 0
    for filepath in ARTICLES_DIR.glob("*.html"):
        if filepath.name == "index.html":
            continue
        if add_features_to_article(filepath):
            count += 1
    print(f"\nAdded features to {count} articles")

if __name__ == "__main__":
    main()
