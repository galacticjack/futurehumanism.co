#!/usr/bin/env python3
"""Fix share buttons to be clean and simple across all articles."""

import glob
import re

# The clean share button CSS
clean_share_css = '''        /* Share Section */
        .share-section {
            margin: 48px 0;
            padding: 32px 0;
            border-top: 1px solid var(--border);
        }
        .share-section h4 {
            font-size: 0.9rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
            text-align: center;
        }
        .share-buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }
        .share-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
        }
        .share-btn.twitter {
            background: #1DA1F2;
            color: white;
        }
        .share-btn.twitter:hover {
            background: #1a8cd8;
        }
        .share-btn.linkedin {
            background: #0077B5;
            color: white;
        }
        .share-btn.linkedin:hover {
            background: #006396;
        }
        .share-btn.copy-link {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        .share-btn.copy-link:hover {
            border-color: var(--accent);
        }
        .share-btn svg {
            width: 18px;
            height: 18px;
        }
        .follow-section {
            text-align: center;
        }
        .follow-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 14px 28px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
        }
        .follow-btn:hover {
            border-color: var(--accent);
            background: var(--accent);
            color: white;
        }
        .follow-btn svg {
            width: 18px;
            height: 18px;
        }'''

for filepath in glob.glob('articles/*.html'):
    if filepath == 'articles/index.html':
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove old share-section CSS and related styles
    # Pattern to match share-section CSS block
    patterns_to_remove = [
        r'/\* Share Section \*/.*?(?=/\*|\Z)',
        r'/\* Share Buttons \*/.*?(?=\.share-btn\.twitter:hover|/\*|\Z)',
        r'\.share-section\s*\{[^}]+\}',
        r'\.share-section h4\s*\{[^}]+\}', 
        r'\.share-buttons\s*\{[^}]+\}',
        r'\.share-btn\s*\{[^}]+\}',
        r'\.share-btn:hover\s*\{[^}]+\}',
        r'\.share-btn\.twitter:hover\s*\{[^}]+\}',
        r'\.share-btn\.linkedin:hover\s*\{[^}]+\}',
        r'\.share-btn\.copy-link:hover\s*\{[^}]+\}',
        r'\.follow-section\s*\{[^}]+\}',
        r'\.follow-btn\s*\{[^}]+\}',
        r'\.follow-btn:hover\s*\{[^}]+\}',
        r'\.follow-btn svg\s*\{[^}]+\}',
    ]
    
    # Find the </style> tag and insert our clean CSS before it
    if '/* Share Section */' in content:
        # Already has share section, replace it
        content = re.sub(r'/\* Share Section \*/.*?(?=/\* Reading Progress|\Z)', '', content, flags=re.DOTALL)
    
    # Insert clean CSS before </style>
    if clean_share_css not in content:
        content = content.replace('</style>', clean_share_css + '\n    </style>')
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f'Updated: {filepath}')

print('Done!')
