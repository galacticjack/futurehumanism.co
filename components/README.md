# FutureHumanism.co Component Library

This folder contains reusable components to ensure consistency across all pages.

## Usage

When creating or updating pages, copy the relevant CSS and HTML from these files.

## Components

### footer.html / footer.css
The standard site footer with 4-column layout (brand, content, tools, connect).
Used on: All pages except quiz.html and 404.html

### article-share.html / article-share.css  
Share buttons (X, LinkedIn, Copy Link) for article pages.
Used on: All articles in /articles/

### article-author.html / article-author.css
Author bio section for article pages.
Used on: All articles in /articles/

## Design Tokens

```css
:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #1a1a1a;
    --bg-dark: #050505;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --text-muted: #666666;
    --accent: #3b82f6;
    --accent-hover: #2563eb;
    --border: #222222;
}
```

## Rules
1. Always use these components when adding new pages
2. When updating a component, update ALL pages that use it
3. Test on both mobile and desktop after changes
