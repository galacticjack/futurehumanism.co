#!/usr/bin/env python3
"""
FutureHumanism.co Build Script
Regenerates sitemap.xml, RSS feed, and articles index from actual content.
Run this after adding/removing articles or pages.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"
TOOLS_DIR = PROJECT_ROOT / "tools"

# Site config
SITE_URL = "https://futurehumanism.co"
SITE_NAME = "Future Humanism"

def get_article_metadata(filepath):
    """Extract title, description, date from an article HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>([^|]+)\s*\|', content)
    title = title_match.group(1).strip() if title_match else filepath.stem.replace('-', ' ').title()
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Extract date from schema (handle both YYYY-MM-DD and full ISO timestamps)
    date_match = re.search(r'"datePublished":\s*"([^"]+)"', content)
    if date_match:
        date_str = date_match.group(1)
        # Normalize to YYYY-MM-DD
        date = date_str[:10]  # Just take first 10 chars (YYYY-MM-DD)
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # Extract category/tag
    tag_match = re.search(r'class="hero-tag"[^>]*>([^<]+)<', content)
    category = tag_match.group(1).strip() if tag_match else "General"
    
    return {
        'title': title,
        'description': description,
        'date': date,
        'category': category,
        'url': f"{SITE_URL}/articles/{filepath.name}",
        'slug': filepath.stem
    }

def generate_sitemap():
    """Generate sitemap.xml with all pages"""
    print("Generating sitemap.xml...")
    
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Static pages
    static_pages = [
        ('/', '1.0', 'daily'),
        ('/articles/', '0.9', 'daily'),
        ('/tools/', '0.8', 'weekly'),
        ('/subscribe.html', '0.7', 'monthly'),
        ('/about.html', '0.6', 'monthly'),
        ('/resources.html', '0.7', 'weekly'),
        ('/quiz.html', '0.7', 'monthly'),
        ('/search.html', '0.6', 'monthly'),
        ('/privacy.html', '0.3', 'yearly'),
        ('/terms.html', '0.3', 'yearly'),
    ]
    
    for path, priority, freq in static_pages:
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = f"{SITE_URL}{path}"
        SubElement(url, 'changefreq').text = freq
        SubElement(url, 'priority').text = priority
    
    # Articles
    for filepath in sorted(ARTICLES_DIR.glob("*.html")):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        meta = get_article_metadata(filepath)
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = meta['url']
        SubElement(url, 'lastmod').text = meta['date']
        SubElement(url, 'changefreq').text = 'monthly'
        SubElement(url, 'priority').text = '0.8'
    
    # Tools
    for filepath in sorted(TOOLS_DIR.glob("*.html")):
        if filepath.name == 'index.html':
            continue
        
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = f"{SITE_URL}/tools/{filepath.name}"
        SubElement(url, 'changefreq').text = 'monthly'
        SubElement(url, 'priority').text = '0.7'
    
    # Write sitemap
    xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
    # Remove the XML declaration line that minidom adds (we'll add our own)
    lines = xml_str.split('\n')[1:]  # Skip first line
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + '\n'.join(lines)
    
    sitemap_path = PROJECT_ROOT / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"  Written: {sitemap_path}")
    return len(list(ARTICLES_DIR.glob("*.html"))) - 2  # Exclude _TEMPLATE and index

def generate_rss_feed():
    """Generate RSS feed (feed.xml)"""
    print("Generating feed.xml...")
    
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = SITE_NAME
    SubElement(channel, 'link').text = SITE_URL
    SubElement(channel, 'description').text = "Where AI meets human potential. Daily insights on AI, automation, and building things that matter."
    SubElement(channel, 'language').text = 'en-us'
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    atom_link = SubElement(channel, 'atom:link')
    atom_link.set('href', f'{SITE_URL}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Add articles (newest first)
    articles = []
    for filepath in ARTICLES_DIR.glob("*.html"):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        articles.append(get_article_metadata(filepath))
    
    # Sort by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    for article in articles[:30]:  # Limit to 30 most recent
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = article['title']
        SubElement(item, 'link').text = article['url']
        SubElement(item, 'description').text = article['description']
        SubElement(item, 'pubDate').text = datetime.strptime(article['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 00:00:00 +0000')
        SubElement(item, 'guid').text = article['url']
        SubElement(item, 'category').text = article['category']
    
    # Write feed
    xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
    lines = xml_str.split('\n')[1:]
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + '\n'.join(lines)
    
    feed_path = PROJECT_ROOT / 'feed.xml'
    with open(feed_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"  Written: {feed_path}")
    return len(articles)

def generate_articles_json():
    """Generate a JSON index of all articles for dynamic loading"""
    print("Generating articles.json...")
    
    articles = []
    for filepath in ARTICLES_DIR.glob("*.html"):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        meta = get_article_metadata(filepath)
        articles.append({
            'slug': meta['slug'],
            'title': meta['title'],
            'description': meta['description'],
            'date': meta['date'],
            'category': meta['category'],
            'url': f"/articles/{filepath.name}"
        })
    
    # Sort by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    json_path = PROJECT_ROOT / 'articles.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2)
    
    print(f"  Written: {json_path}")
    return len(articles)

def main():
    print(f"\n{'='*50}")
    print("FutureHumanism.co Build Script")
    print(f"{'='*50}\n")
    
    article_count = generate_sitemap()
    print(f"  → {article_count} articles in sitemap\n")
    
    rss_count = generate_rss_feed()
    print(f"  → {rss_count} articles in RSS feed\n")
    
    json_count = generate_articles_json()
    print(f"  → {json_count} articles in JSON index\n")
    
    print(f"{'='*50}")
    print("Build complete!")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
