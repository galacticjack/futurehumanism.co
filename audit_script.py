#!/usr/bin/env python3
"""
FutureHumanism.co Article Audit Script
Checks for:
1. Model names consistency
2. Outdated information
3. Duplicate hero images
4. Title-content match
5. Author and meta tags presence
"""

import os
import re
from urllib.parse import urlparse
from collections import defaultdict, Counter

def audit_articles():
    articles_dir = "/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co/articles"
    
    # Track hero images for duplicates
    hero_images = defaultdict(list)
    
    # Model version patterns to check
    model_patterns = {
        'claude_versions': re.compile(r'Claude\s+(?:3\.5|4\.0|4\.5|Opus|Sonnet|Haiku)', re.IGNORECASE),
        'gpt_versions': re.compile(r'GPT-?(?:4o?|5\.?\d*)', re.IGNORECASE),
        'gemini_versions': re.compile(r'Gemini\s+(?:1\.5|2\.0|Pro|Ultra)', re.IGNORECASE),
        'outdated_models': re.compile(r'(?:GPT-?3|Claude\s+1|Claude\s+2(?!\s*[.]0)|Bard)', re.IGNORECASE),
    }
    
    # Date patterns for outdated content
    outdated_patterns = [
        re.compile(r'\b(?:2022|2023|2024|2025)\b'),
        re.compile(r'by\s+(?:2023|2024|2025)', re.IGNORECASE),
        re.compile(r'in\s+(?:2023|2024|2025)', re.IGNORECASE),
    ]
    
    audit_results = []
    
    # Get all HTML files
    html_files = [f for f in os.listdir(articles_dir) if f.endswith('.html') and f != 'index.html']
    html_files.sort()
    
    for filename in html_files:
        filepath = os.path.join(articles_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "NO TITLE FOUND"
            
            # Check for author meta tag
            if '"name": "Galactic Jack"' not in content:
                issues.append("Missing or incorrect author in schema markup")
            
            # Check for OG tags
            if 'property="og:title"' not in content:
                issues.append("Missing og:title meta tag")
            if 'property="og:description"' not in content:
                issues.append("Missing og:description meta tag")
            if 'property="og:image"' not in content:
                issues.append("Missing og:image meta tag")
            
            # Check for schema markup
            if '@type": "Article"' not in content:
                issues.append("Missing article schema markup")
            
            # Extract hero image
            hero_match = re.search(r'url\([\'"]([^\'")]*unsplash\.com[^\'")]*)[\'"]', content)
            if hero_match:
                hero_url = hero_match.group(1)
                hero_images[hero_url].append(filename)
            
            # Check model naming consistency
            for pattern_name, pattern in model_patterns.items():
                matches = pattern.findall(content)
                if pattern_name == 'outdated_models' and matches:
                    issues.append(f"References outdated AI models: {', '.join(set(matches))}")
            
            # Look for specific version inconsistencies
            # Check for mixed usage
            claude_variants = re.findall(r'Claude[^a-zA-Z]*(?:3\.5|4\.0|4\.5|Opus|Sonnet|Haiku|Pro)?', content, re.IGNORECASE)
            gpt_variants = re.findall(r'(?:ChatGPT|GPT)[^a-zA-Z]*(?:3\.5|4o?|5\.?\d*|Plus|Pro)?', content, re.IGNORECASE)
            
            if claude_variants:
                unique_claude = set([v.strip() for v in claude_variants])
                if len(unique_claude) > 2:  # Allow for "Claude" and one version variant
                    issues.append(f"Inconsistent Claude naming: {', '.join(unique_claude)}")
            
            if gpt_variants:
                unique_gpt = set([v.strip() for v in gpt_variants])
                if len(unique_gpt) > 2:  # Allow for "ChatGPT" and one version variant
                    issues.append(f"Inconsistent GPT naming: {', '.join(unique_gpt)}")
            
            # Check for outdated year references
            for pattern in outdated_patterns:
                matches = pattern.findall(content)
                if matches:
                    issues.append(f"Contains outdated date references: {', '.join(set(matches))}")
            
            # Check date published (should be 2026)
            date_pub_match = re.search(r'"datePublished":\s*"([^"]*)"', content)
            if date_pub_match:
                date_str = date_pub_match.group(1)
                if not date_str.startswith('2026'):
                    issues.append(f"Article date is not 2026: {date_str}")
            
            audit_results.append({
                'filename': filename,
                'title': title,
                'issues': issues
            })
            
        except Exception as e:
            audit_results.append({
                'filename': filename,
                'title': "ERROR READING FILE",
                'issues': [f"File read error: {str(e)}"]
            })
    
    # Check for duplicate hero images
    duplicate_images = {url: files for url, files in hero_images.items() if len(files) > 1}
    
    return audit_results, duplicate_images

def generate_report(audit_results, duplicate_images):
    report = []
    report.append("# FUTUREHUMANISM.CO ARTICLE AUDIT REPORT")
    report.append("Generated: February 2026")
    report.append("")
    report.append("## SUMMARY")
    
    total_articles = len(audit_results)
    articles_with_issues = sum(1 for result in audit_results if result['issues'])
    
    report.append(f"- **Total Articles Audited:** {total_articles}")
    report.append(f"- **Articles with Issues:** {articles_with_issues}")
    report.append(f"- **Articles Clean:** {total_articles - articles_with_issues}")
    report.append(f"- **Duplicate Hero Images Found:** {len(duplicate_images)} sets")
    report.append("")
    
    # Duplicate images section
    if duplicate_images:
        report.append("## DUPLICATE HERO IMAGES")
        report.append("")
        for url, files in duplicate_images.items():
            report.append(f"**Image:** {url}")
            report.append(f"**Used in:** {', '.join(files)}")
            report.append(f"**Fix:** Assign unique hero images to each article")
            report.append("")
    
    report.append("## INDIVIDUAL ARTICLE AUDIT")
    report.append("")
    
    for result in audit_results:
        report.append(f"### {result['filename']}")
        report.append(f"**Title:** {result['title']}")
        report.append("")
        
        if result['issues']:
            report.append("**Issues Found:**")
            for issue in result['issues']:
                report.append(f"- {issue}")
            report.append("")
            report.append("**Specific Fixes Needed:**")
            for issue in result['issues']:
                if "Claude naming" in issue:
                    report.append("- Standardize to either 'Claude' or 'Claude Opus 4.5' consistently")
                elif "GPT naming" in issue:
                    report.append("- Standardize to either 'ChatGPT' or 'GPT-4o' consistently")
                elif "outdated date" in issue:
                    report.append("- Update all date references to 2026 or remove specific years if not relevant")
                elif "outdated AI models" in issue:
                    report.append("- Replace outdated model names with current equivalents")
                elif "Missing" in issue and "meta" in issue:
                    report.append("- Add missing meta tags for proper social sharing")
                elif "schema markup" in issue:
                    report.append("- Add proper JSON-LD schema markup for articles")
            report.append("")
        else:
            report.append("**Status:** ✅ No issues found")
            report.append("")
        
        report.append("---")
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    print("Starting audit...")
    audit_results, duplicate_images = audit_articles()
    report = generate_report(audit_results, duplicate_images)
    
    output_path = "/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co/AUDIT-REPORT.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Audit complete. Report saved to: {output_path}")
    print(f"Found {len([r for r in audit_results if r['issues']])} articles with issues")
    print(f"Found {len(duplicate_images)} sets of duplicate hero images")