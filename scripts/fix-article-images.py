#!/usr/bin/env python3
"""Assign unique images to articles that are using duplicates"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = PROJECT_ROOT / "articles"

# Unique Unsplash images for different article topics
UNIQUE_IMAGES = {
    # AI Agents
    'ai-agents': 'photo-1677442136019-21780ecad995',  # AI brain
    'ai-agent-economy': 'photo-1551288049-bebda4e38f71',  # Charts/economy
    'ai-agent-security': 'photo-1563986768609-322da13575f3',  # Security lock
    
    # Coding/Dev
    'coding': 'photo-1555949963-ff9fe0c870eb',  # Code on screen
    'github': 'photo-1618401471353-b98afee0b2eb',  # GitHub style
    'cursor': 'photo-1629654297299-c8506221ca97',  # IDE
    'claude-code': 'photo-1587620962725-abab7fe55159',  # Programming
    
    # Enterprise/Business  
    'enterprise': 'photo-1553877522-43269d4ea984',  # Business meeting
    'snowflake': 'photo-1451187580459-43490279c0fa',  # Data/cloud
    'chatgpt-pro': 'photo-1516321318423-f06f85e504b3',  # AI assistant
    
    # Tools/Automation
    'automation': 'photo-1518432031352-d6fc5c10da5a',  # Automation
    'tools': 'photo-1581091226825-a6a2a5aee158',  # Tech tools
    'nocode': 'photo-1460925895917-afdab827c52f',  # Dashboard
    
    # Research/Analysis
    'deepseek': 'photo-1526374965328-7f61d4dc18c5',  # Matrix/AI
    'convergence': 'photo-1620712943543-bcc4688e7485',  # AI comparison
    'world-models': 'photo-1518770660439-4636190af475',  # 3D/Models
    
    # Lifestyle/Work
    'remote-work': 'photo-1522071820081-009f0129c71c',  # Remote team
    'side-hustle': 'photo-1554224155-6726b3ff858f',  # Money/hustle
    'health': 'photo-1576091160399-112ba8d25d1d',  # Health tech
    'creator': 'photo-1611162617474-5b21e879e113',  # Creator
    
    # Crypto/DeFi
    'crypto': 'photo-1518546305927-5a555bb7020d',  # Crypto
    'defi': 'photo-1639762681485-074b7f938ba0',  # DeFi
    
    # AI Models
    'gemini': 'photo-1504868584819-f8e8b4b6d7e3',  # Google style
    'search': 'photo-1555421689-491a97ff2040',  # Search
    'llm': 'photo-1558494949-ef010cbdcc31',  # AI network
    
    # Strategy
    'strategy': 'photo-1552664730-d307ca884978',  # Strategy
    'business': 'photo-1553877522-43269d4ea984',  # Business
    
    # Default fallback
    'default': 'photo-1485827404703-89b55fcc595e',  # Robot
}

# Map specific articles to images
ARTICLE_IMAGES = {
    '16-ai-agents-built-c-compiler': 'photo-1629654297299-c8506221ca97',  # Compiler/code
    '2026-year-ai-agents-production': 'photo-1677442136019-21780ecad995',  # AI
    'agent-infrastructure-orchestration-2026': 'photo-1558494949-ef010cbdcc31',  # Network
    'agentic-ai-100-billion-market-2026': 'photo-1551288049-bebda4e38f71',  # Market
    'ai-agent-economy-2027': 'photo-1460925895917-afdab827c52f',  # Economy
    'ai-agent-security-vulnerabilities-2026': 'photo-1563986768609-322da13575f3',  # Security
    'ai-agents-2026-guide': 'photo-1531746790731-6c087fecd65a',  # AI agents
    'ai-agents-eating-software': 'photo-1620712943543-bcc4688e7485',  # Software
    'ai-agents-memory': 'photo-1485827404703-89b55fcc595e',  # Memory/robot
    'ai-agents-platform-shift': 'photo-1518770660439-4636190af475',  # Platform
    'ai-computer-control-revolution': 'photo-1551434678-e076c223a692',  # Computer
    'ai-marketing-strategies-2026': 'photo-1460925895917-afdab827c52f',  # Marketing
    'ai-model-convergence-2026': 'photo-1620712943543-bcc4688e7485',  # Models
    'ai-tools-replacing-saas-subscriptions': 'photo-1581091226825-a6a2a5aee158',  # Tools
    'ai-world-models-next-breakthrough': 'photo-1518432031352-d6fc5c10da5a',  # 3D
    'apple-xcode-agentic-coding': 'photo-1621839673705-6617adf9e890',  # Apple/Xcode
    'automate-80-percent-agency-work': 'photo-1553729459-efe14ef6055d',  # Automation
    'automate-freelance-business-ai-guide': 'photo-1460925895917-afdab827c52f',  # Freelance
    'best-ai-coding-assistants-beginners-2026': 'photo-1555949963-ff9fe0c870eb',  # Coding
    'best-ai-tools-solopreneurs-2026': 'photo-1581091226825-a6a2a5aee158',  # Tools
    'build-your-first-ai-agent-practical-guide': 'photo-1555949963-aa79dcee981c',  # Build
    'building-passive-income-ai-automation': 'photo-1554224155-6726b3ff858f',  # Income
    'chatgpt-pro-200-enterprise-ai-shift': 'photo-1553877522-43269d4ea984',  # Enterprise
    'claude-vs-chatgpt-for-coding-2026': 'photo-1587620962725-abab7fe55159',  # Code compare
    'claude-vs-gpt-comparison': 'photo-1516110833967-0b5716ca1387',  # Comparison
    'creator-economy-ai-tools-2026': 'photo-1611162617474-5b21e879e113',  # Creator
    'crypto-market-cycles-ai-trading-signals': 'photo-1518546305927-5a555bb7020d',  # Crypto
    'deepseek-r1-vs-openai-o1': 'photo-1526374965328-7f61d4dc18c5',  # Reasoning
    'defi-yield-strategies-2026': 'photo-1639762681485-074b7f938ba0',  # DeFi
    'future-of-search-after-chatgpt': 'photo-1555421689-491a97ff2040',  # Search
    'gemini-2-flash-multimodal-ai-dominance': 'photo-1504868584819-f8e8b4b6d7e3',  # Multimodal
    'github-copilot-vs-cursor-vs-claude-code-2026': 'photo-1618401471353-b98afee0b2eb',  # GitHub
    'health-tech-wearables-2026': 'photo-1576091160399-112ba8d25d1d',  # Health
    'local-llms-running-ai-on-your-hardware': 'photo-1558494949-ef010cbdcc31',  # Local
    'nocode-automation-stacks-solopreneurs': 'photo-1551288049-bebda4e38f71',  # No-code
    'prompt-engineering-that-actually-works': 'photo-1516321318423-f06f85e504b3',  # Prompts
    'remote-work-async-culture-2026': 'photo-1522071820081-009f0129c71c',  # Remote
    'shadow-ai-enterprise-crisis': 'photo-1563986768609-322da13575f3',  # Shadow IT
    'side-hustle-ideas-ai-era': 'photo-1554224155-6726b3ff858f',  # Side hustle
    'snowflake-openai-200-million-partnership': 'photo-1451187580459-43490279c0fa',  # Data
    'snowflake-openai-enterprise-ai-tipping-point': 'photo-1558494949-ef010cbdcc31',  # Enterprise
    'why-ai-side-projects-fail': 'photo-1552664730-d307ca884978',  # Strategy
    'why-every-business-needs-ai-strategy-2026': 'photo-1553877522-43269d4ea984',  # Business
}

def get_image_for_article(slug):
    """Get the appropriate image for an article"""
    if slug in ARTICLE_IMAGES:
        return ARTICLE_IMAGES[slug]
    return UNIQUE_IMAGES['default']

def fix_article_images():
    """Update hero images in articles"""
    
    fixed = 0
    for filepath in sorted(ARTICLES_DIR.glob('*.html')):
        if filepath.name in ['_TEMPLATE.html', 'index.html']:
            continue
        
        slug = filepath.stem
        new_image = get_image_for_article(slug)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update hero background image
        old_content = content
        
        # Replace Unsplash image in hero background
        content = re.sub(
            r"(\.hero\s*\{[^}]*background:[^;]*url\('?)https://images\.unsplash\.com/[^?'\"]+",
            rf"\g<1>https://images.unsplash.com/{new_image}",
            content
        )
        
        if content != old_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ {filepath.name}")
            fixed += 1
    
    return fixed

def main():
    print("Assigning unique images to articles...")
    print("")
    
    fixed = fix_article_images()
    print(f"\n  Updated {fixed} articles with unique images")

if __name__ == '__main__':
    main()
