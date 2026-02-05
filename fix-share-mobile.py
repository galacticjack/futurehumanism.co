#!/usr/bin/env python3
"""Fix share buttons mobile layout and related article tags."""

import glob
import re

# CSS fix for share buttons and related tags
css_fixes = '''
        /* Share section mobile fix */
        @media (max-width: 768px) {
            .share-buttons {
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }
            .share-btn {
                width: 100%;
                max-width: 250px;
                justify-content: center;
                white-space: nowrap;
            }
        }
        /* Related article tag - purple bg white text */
        .related-tag {
            background: var(--accent) !important;
            color: #ffffff !important;
        }
'''

for filepath in glob.glob('articles/*.html'):
    if filepath == 'articles/index.html':
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix 1: Add mobile CSS for share buttons if not already there
    if 'share-buttons {' in content and 'flex-direction: column' not in content:
        # Find the </style> tag and add our CSS before it
        content = content.replace('</style>', css_fixes + '\n    </style>')
    
    # Fix 2: Make related article tags purple bg + white text
    # Find pattern like: <span style="color: var(--accent)...">DEEP DIVE</span>
    content = re.sub(
        r'<span style="[^"]*color:\s*var\(--accent\)[^"]*">([A-Z\s]+)</span>',
        r'<span style="display: inline-block; background: var(--accent); color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">\1</span>',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f'Fixed: {filepath}')

print('Done!')
