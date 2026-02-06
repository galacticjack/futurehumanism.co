#!/bin/bash
# Fix navigation across all pages - add Free Guide button

cd /Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co

# CSS for nav-cta-secondary (to be added where missing)
CSS_BLOCK='        .nav-cta-secondary {
            background: transparent;
            border: 1px solid var(--accent);
            color: var(--accent) !important;
        }
        
        .nav-cta-secondary:hover {
            background: var(--accent);
            color: white !important;
        }'

# Find all HTML files except templates
for file in $(find . -name "*.html" -type f | grep -v _TEMPLATE | grep -v node_modules); do
    # Skip if already has Free Guide
    if grep -q "Free Guide" "$file"; then
        echo "SKIP (has Free Guide): $file"
        continue
    fi
    
    # Check if file has the Subscribe nav-cta
    if grep -q 'class="nav-cta">Subscribe' "$file"; then
        echo "FIXING: $file"
        
        # Add Free Guide button before Subscribe
        sed -i '' 's|<a href="/subscribe.html" class="nav-cta">Subscribe</a>|<a href="/free-guide" class="nav-cta nav-cta-secondary">Free Guide</a>\n                <a href="/subscribe.html" class="nav-cta">Subscribe</a>|g' "$file"
        
        # Check if nav-cta-secondary CSS exists, if not add it after .nav-cta:hover
        if ! grep -q "nav-cta-secondary" "$file"; then
            # Add CSS after .nav-cta:hover block
            sed -i '' '/\.nav-cta:hover.*{/,/}/{ /}/a\
        \
        .nav-cta-secondary {\
            background: transparent;\
            border: 1px solid var(--accent);\
            color: var(--accent) !important;\
        }\
        \
        .nav-cta-secondary:hover {\
            background: var(--accent);\
            color: white !important;\
        }
}' "$file"
        fi
    else
        echo "SKIP (no nav-cta Subscribe): $file"
    fi
done

echo "Done!"
