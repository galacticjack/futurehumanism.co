#!/usr/bin/env python3
"""Fix Twitter card meta tags for all articles"""

import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent.parent / "articles"
IMAGES_DIR = Path(__file__).parent.parent / "images"

# Default fallback image
DEFAULT_OG_IMAGE = "https://futurehumanism.co/images/og-image.jpg"

def fix_twitter_cards(filepath):
    """Ensure all required Twitter card meta tags exist"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    slug = filepath.stem
    
    # Extract existing meta values
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).replace(' | Future Humanism', '').strip() if title_match else slug.replace('-', ' ').title()
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Determine OG image - check if specific one exists, else use default
    specific_og = f"images/og-{slug}.jpg"
    if (IMAGES_DIR / f"og-{slug}.jpg").exists():
        og_image = f"https://futurehumanism.co/{specific_og}"
    else:
        og_image = DEFAULT_OG_IMAGE
    
    # Build required meta tags
    required_meta = {
        'twitter:card': 'summary_large_image',
        'twitter:site': '@FutureHumanism',
        'twitter:title': title,
        'twitter:description': description[:200] if description else title,
        'twitter:image': og_image,
    }
    
    # Check and add missing tags
    changes = []
    for meta_name, meta_content in required_meta.items():
        pattern = f'<meta name="{meta_name}"'
        if pattern not in content and f'<meta property="{meta_name}"' not in content:
            # Add after og:image or before </head>
            new_tag = f'    <meta name="{meta_name}" content="{meta_content}">\n'
            
            if '</head>' in content:
                content = content.replace('</head>', new_tag + '</head>')
                changes.append(meta_name)
    
    # Also ensure og:image exists and points to correct image
    if 'og:image' not in content:
        new_tag = f'    <meta property="og:image" content="{og_image}">\n'
        content = content.replace('</head>', new_tag + '</head>')
        changes.append('og:image')
    else:
        # Update og:image if using missing image
        og_match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
        if og_match:
            current_og = og_match.group(1)
            img_path = current_og.replace('https://futurehumanism.co/', '')
            if not (Path(__file__).parent.parent / img_path).exists():
                content = content.replace(current_og, og_image)
                changes.append('og:image-fixed')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    
    return []

def main():
    print("Fixing Twitter card meta tags...")
    print("")
    
    fixed = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        changes = fix_twitter_cards(filepath)
        if changes:
            print(f"  ✓ {filepath.name}: added {', '.join(changes)}")
            fixed += 1
    
    print(f"\n  Fixed {fixed} articles")

if __name__ == '__main__':
    main()
