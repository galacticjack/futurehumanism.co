#!/usr/bin/env python3
"""
FAQ Schema Generator for FutureHumanism.co

This script automatically adds FAQ schema to articles based on their H2 headings.
FAQ schema helps with:
1. Google "People Also Ask" features
2. AI search citation (ChatGPT, Perplexity)
3. More SERP real estate

Growth tactic: SEO Quick Win from seo-growth-engine skill
"""

import os
import re
import json
from pathlib import Path
from html import unescape

ARTICLES_DIR = Path(__file__).parent / "articles"

def extract_h2_content(html_content):
    """Extract H2 headings and their following paragraph content as FAQ pairs."""
    faqs = []
    
    # Find all h2 tags and their following content
    h2_pattern = r'<h2[^>]*>(.*?)</h2>\s*(?:<[^>]+>)*\s*<p>(.*?)</p>'
    matches = re.findall(h2_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    for question, answer in matches:
        # Clean up the question
        question = re.sub(r'<[^>]+>', '', question).strip()
        question = unescape(question)
        
        # Skip non-question headings
        skip_headings = [
            'Bottom Line', 'Keep Reading', 'Related', 'Before you go', 
            'Stay Ahead', 'Subscribe', 'Newsletter', 'Comments',
            'Share', 'About', 'Author', 'Sources', 'References'
        ]
        if any(skip in question for skip in skip_headings):
            continue
            
        # Clean up the answer
        answer = re.sub(r'<[^>]+>', '', answer).strip()
        answer = unescape(answer)
        
        # Skip if answer is too short or too long
        if len(answer) < 50 or len(answer) > 600:
            continue
            
        # Convert heading to question format if needed
        if not question.endswith('?'):
            question = f"What is {question}?" if len(question.split()) <= 3 else f"{question}?"
        
        faqs.append({
            "question": question,
            "answer": answer
        })
    
    # Limit to 5 FAQs (Google best practice)
    return faqs[:5]

def generate_faq_schema(faqs):
    """Generate FAQ schema JSON-LD."""
    if not faqs:
        return None
        
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }
    
    return json.dumps(schema, indent=4)

def has_faq_schema(html_content):
    """Check if article already has FAQ schema."""
    return 'FAQPage' in html_content

def add_faq_schema_to_article(filepath):
    """Add FAQ schema to a single article."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has FAQ schema
    if has_faq_schema(content):
        return False, "Already has FAQ schema"
    
    # Skip template
    if '_TEMPLATE' in str(filepath):
        return False, "Template file"
    
    # Extract FAQs
    faqs = extract_h2_content(content)
    
    if not faqs:
        return False, "No suitable FAQs found"
    
    # Generate schema
    faq_schema = generate_faq_schema(faqs)
    
    # Find where to insert (after existing schema or before </head>)
    # Look for the closing </script> of the Article schema
    article_schema_end = content.find('</script>', content.find('"@type": "Article"'))
    
    if article_schema_end > 0:
        # Insert after existing Article schema
        insert_point = article_schema_end + len('</script>')
        new_script = f'\n    <script type="application/ld+json">\n    {faq_schema}\n    </script>'
        content = content[:insert_point] + new_script + content[insert_point:]
    else:
        # Insert before </head>
        head_end = content.find('</head>')
        if head_end > 0:
            new_script = f'    <script type="application/ld+json">\n    {faq_schema}\n    </script>\n    '
            content = content[:head_end] + new_script + content[head_end:]
        else:
            return False, "Could not find insertion point"
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"Added {len(faqs)} FAQs"

def main():
    """Process all articles."""
    print("🔍 FAQ Schema Generator for FutureHumanism.co")
    print("=" * 50)
    
    articles = list(ARTICLES_DIR.glob("*.html"))
    updated = 0
    skipped = 0
    
    for article in sorted(articles):
        if article.name.startswith('_'):
            continue
            
        success, message = add_faq_schema_to_article(article)
        
        if success:
            print(f"✅ {article.name}: {message}")
            updated += 1
        else:
            print(f"⏭️  {article.name}: {message}")
            skipped += 1
    
    print("=" * 50)
    print(f"📊 Results: {updated} articles updated, {skipped} skipped")
    print("\n🚀 FAQ schema helps with:")
    print("   - Google 'People Also Ask' features")
    print("   - AI search citations (ChatGPT, Perplexity)")
    print("   - More SERP real estate")

if __name__ == "__main__":
    main()
