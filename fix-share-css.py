#!/usr/bin/env python3
"""Fix share button CSS to show text properly."""

import glob

old_css = '''        .share-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
            background: var(--bg-secondary);
            color: var(--text-secondary);
        }'''

new_css = '''        .share-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
            background: var(--bg-secondary);
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
        }'''

for filepath in glob.glob('articles/*.html'):
    if filepath == 'articles/index.html':
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
    
    if old_css in content:
        content = content.replace(old_css, new_css)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Fixed CSS in: {filepath}')
    else:
        print(f'CSS already fixed or different in: {filepath}')

print('Done!')
