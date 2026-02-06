#!/usr/bin/env python3
"""Remove duplicate share sections outside article tag."""

import glob
import re

for filepath in glob.glob('articles/*.html'):
    if filepath == 'articles/index.html':
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove the duplicate share section that appears AFTER </article>
    # Pattern: </article> followed by <div class="share-section">...</div>
    pattern = r'(</article>\s*)\n\s*<div class="share-section">\s*<p class="share-label">.*?</div>\s*</div>'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, r'\1', content, flags=re.DOTALL)
        print(f'Removed duplicate share section from: {filepath}')
        
        with open(filepath, 'w') as f:
            f.write(content)
    else:
        print(f'No duplicate found in: {filepath}')

print('Done!')
