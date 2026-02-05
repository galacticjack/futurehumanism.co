#!/usr/bin/env python3
"""
Add reading progress bar to all article HTML files
"""
import os
import re
import glob

# CSS for the progress bar
progress_css = """    /* Reading Progress Bar */
    #reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #FF5A5F, #FF7F7F);
        z-index: 1000;
        transition: width 0.1s ease-out;
    }</style>"""

# HTML div for the progress bar
progress_html = """<body>
    <div id="reading-progress"></div>"""

# JavaScript for the progress bar
progress_js = """    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const progressBar = document.getElementById('reading-progress');
        const article = document.querySelector('article, .content, main, .article-content') || document.body;
        
        function updateProgress() {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = Math.min(100, Math.max(0, (scrollTop / docHeight) * 100));
            progressBar.style.width = progress + '%';
        }
        
        window.addEventListener('scroll', updateProgress);
        updateProgress();
    });
    </script>
</body>"""

def add_progress_bar_to_file(filepath):
    """Add progress bar components to a single HTML file"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has progress bar
    if 'reading-progress' in content:
        print(f"  Already has progress bar, skipping")
        return
    
    # 1. Add CSS before closing </style> tag
    content = re.sub(r'(\s*)</style>', r'\1' + progress_css, content)
    
    # 2. Add progress div after opening <body> tag
    content = re.sub(r'(<body[^>]*>)', progress_html, content)
    
    # 3. Add JavaScript before closing </body> tag
    content = re.sub(r'(\s*)</body>', progress_js, content)
    
    # Write back the modified content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Added progress bar")

def main():
    articles_dir = '/Users/galacticjack/projects/futurehumanism/articles'
    html_files = glob.glob(os.path.join(articles_dir, '*.html'))
    
    print(f"Found {len(html_files)} HTML files in {articles_dir}")
    
    for filepath in html_files:
        add_progress_bar_to_file(filepath)
    
    print("\n🚀 Reading progress bar added to all articles!")

if __name__ == "__main__":
    main()