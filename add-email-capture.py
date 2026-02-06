#!/usr/bin/env python3
"""
Add email capture component to all tools that have results/score sections.
This increases conversion at peak engagement moment.
"""

import os
import re
from pathlib import Path

TOOLS_DIR = Path(__file__).parent / "tools"

# Map of tool filenames to their display names
TOOLS_CONFIG = {
    "ai-productivity-score.html": "AI Productivity Score",
    "ai-readiness-quiz.html": "AI Readiness Assessment",
    "ai-workflow-quiz.html": "AI Workflow Quiz",
    "ai-skills-gap.html": "AI Skills Gap Analyzer",
    "ai-roi-calculator.html": "AI ROI Calculator",
    "automation-savings-calculator.html": "Automation Savings Calculator",
    "ai-job-analyzer.html": "AI Job Impact Analyzer",
    "ai-or-human.html": "AI or Human Quiz",
    "headline-analyzer.html": "Headline Analyzer",
    "ai-use-case-generator.html": "AI Use Case Generator",
}

def add_email_capture_to_file(filepath, tool_name):
    """Add email capture component to a tool file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already has email capture
    if 'email-capture.js' in content:
        print(f"  [SKIP] {filepath.name} - already has email capture")
        return False
    
    # Add script include before closing </body> or before main script
    script_include = '    <!-- Email Capture Component -->\n    <script src="../components/email-capture.js"></script>\n\n'
    
    # Find a good insertion point - before the main <script> tag
    # Look for the pattern: </footer>\n\n    <script> or similar
    patterns_to_try = [
        (r'(</footer>\s*\n\s*\n\s*<script>)', r'\1'),  # After footer, before script
        (r'(<script>\s*const\s+)', script_include + r'    <script>\n        const '),  # Before first const
    ]
    
    # Try to insert the script include
    if '</footer>' in content and '<script>' in content:
        # Insert between footer and script
        content = content.replace(
            '</footer>\n\n    <script>',
            '</footer>\n\n' + script_include + '    <script>'
        )
    elif '</footer>' in content:
        content = content.replace(
            '</footer>',
            '</footer>\n\n' + script_include
        )
    
    # Determine quiz type
    is_quiz = 'quiz' in filepath.name.lower() or 'score' in filepath.name.lower() or 'readiness' in filepath.name.lower()
    tool_type = 'quiz' if is_quiz else 'calculator'
    
    # Add the trigger call after results are shown
    # Look for patterns like gtag('event', 'quiz_complete' or similar tracking events
    trigger_code = f'''
            
            // Show email capture after 3 seconds
            if (typeof triggerEmailCaptureOnResults === 'function') {{
                triggerEmailCaptureOnResults({{
                    score: typeof total !== 'undefined' ? total : 75,
                    toolName: '{tool_name}',
                    type: '{tool_type}'
                }}, 3000);
            }}'''
    
    # Try to find results display function and add trigger
    # Common patterns: showResults(), displayResults(), calculateResults()
    result_patterns = [
        r"(gtag\('event',\s*'quiz_complete'[^}]+}\);)",
        r"(gtag\('event',\s*'calculator_complete'[^}]+}\);)",
        r"(gtag\('event',\s*'assessment_complete'[^}]+}\);)",
        r"(gtag\('event',\s*'result[s]?_shown'[^}]+}\);)",
    ]
    
    trigger_added = False
    for pattern in result_patterns:
        match = re.search(pattern, content)
        if match and 'triggerEmailCaptureOnResults' not in content:
            # Insert after the gtag call
            original = match.group(1)
            replacement = original + trigger_code
            content = content.replace(original, replacement)
            trigger_added = True
            break
    
    # If no gtag found, try to find showResults function ending
    if not trigger_added and 'triggerEmailCaptureOnResults' not in content:
        # Look for the end of a showResults-like function
        show_results_patterns = [
            r"(function showResults\(\)[^}]+(?:\{[^}]*\})*[^}]+)(}[\s\n]*function)",
        ]
        # This is complex, so let's just note it needs manual review
        print(f"  [WARN] {filepath.name} - couldn't auto-add trigger, may need manual review")
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  [OK] {filepath.name} - added email capture")
    return True

def main():
    print("Adding email capture component to FutureHumanism tools...\n")
    
    updated = 0
    for filename, tool_name in TOOLS_CONFIG.items():
        filepath = TOOLS_DIR / filename
        if filepath.exists():
            if add_email_capture_to_file(filepath, tool_name):
                updated += 1
        else:
            print(f"  [MISS] {filename} - file not found")
    
    print(f"\nDone! Updated {updated} files.")

if __name__ == "__main__":
    main()
