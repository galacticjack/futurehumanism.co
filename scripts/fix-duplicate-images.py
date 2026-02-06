#!/usr/bin/env python3
"""Fix duplicate images in Keep Reading sections across all articles."""
import os
import re
import glob

ARTICLES_DIR = "/Users/galacticjack/.openclaw/workspace/projects/futurehumanism.co/articles"

# Unique images for each article slug
ARTICLE_IMAGES = {
    "ai-agents-2026-guide": "photo-1620712943543-bcc4688e7485",
    "ai-agents-eating-software": "photo-1531746790731-6c087fecd65a",
    "ai-agents-memory": "photo-1485827404703-89b55fcc595e",
    "ai-agents-platform-shift": "photo-1551288049-bebda4e38f71",
    "ai-model-convergence-2026": "photo-1526374965328-7f61d4dc18c5",
    "ai-tools-replacing-saas-subscriptions": "photo-1558494949-ef010cbdcc31",
    "ai-world-models-next-breakthrough": "photo-1504868584819-f8e8b4b6d7e3",
    "automate-80-percent-agency-work": "photo-1460925895917-afdab827c52f",
    "build-your-first-ai-agent-practical-guide": "photo-1498050108023-c5249f4df085",
    "building-passive-income-ai-automation": "photo-1553877522-43269d4ea984",
    "chatgpt-pro-200-enterprise-ai-shift": "photo-1573164713988-8665fc963095",
    "claude-vs-gpt-comparison": "photo-1516110833967-0b5716ca1387",
    "creator-economy-ai-tools-2026": "photo-1611162617474-5b21e879e113",
    "crypto-market-cycles-ai-trading-signals": "photo-1518546305927-5a555bb7020d",
    "deepseek-r1-vs-openai-o1": "photo-1535378917042-10a22c95931a",
    "defi-yield-strategies-2026": "photo-1639762681485-074b7f938ba0",
    "future-of-search-after-chatgpt": "photo-1519389950473-47ba0277781c",
    "gemini-2-flash-multimodal-ai-dominance": "photo-1518770660439-4636190af475",
    "health-tech-wearables-2026": "photo-1576091160399-112ba8d25d1d",
    "local-llms-running-ai-on-your-hardware": "photo-1518432031352-d6fc5c10da5a",
    "nocode-automation-stacks-solopreneurs": "photo-1460925895917-afdab827c52f",
    "prompt-engineering-that-actually-works": "photo-1555949963-ff9fe0c870eb",
    "remote-work-async-culture-2026": "photo-1522071820081-009f0129c71c",
    "side-hustle-ideas-ai-era": "photo-1553729459-efe14ef6055d",
    "snowflake-openai-enterprise-ai-tipping-point": "photo-1563986768609-322da13575f3",
    "why-ai-side-projects-fail": "photo-1555949963-aa79dcee981c",
    "why-every-business-needs-ai-strategy-2026": "photo-1552664730-d307ca884978",
    "50-dollar-tech-stack": "photo-1451187580459-43490279c0fa",
    "ai-agent-economy-2027": "photo-1516321318423-f06f85e504b3",
    "agent-infrastructure-orchestration-2026": "photo-1551434678-e076c223a692",
    "ai-computer-control-revolution": "photo-1533750349088-cd871a92f312",
    "ai-marketing-strategies-2026": "photo-1554224155-6726b3ff858f",
}

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Find all Keep Reading image references and fix them
    # Pattern: <img ... src="...unsplash.com/photo-XXXXX..." alt="ARTICLE_TITLE">
    
    for slug, correct_image in ARTICLE_IMAGES.items():
        # Match patterns where the alt text matches this article
        # Common alt texts to look for
        alt_patterns = [
            slug.replace("-", " ").title(),
            slug.replace("-", " "),
        ]
        
        for alt in alt_patterns:
            # Find img tags with this alt and fix their src
            pattern = rf'(<img[^>]*src="https://images\.unsplash\.com/)photo-[^?]+(\?[^"]*"[^>]*alt="[^"]*{re.escape(alt)}[^"]*")'
            replacement = rf'\g<1>{correct_image}\2'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    fixed = 0
    for filepath in glob.glob(os.path.join(ARTICLES_DIR, "*.html")):
        if "_TEMPLATE" in filepath or "index" in filepath:
            continue
        if fix_file(filepath):
            print(f"Fixed: {os.path.basename(filepath)}")
            fixed += 1
    print(f"\nTotal fixed: {fixed}")

if __name__ == "__main__":
    main()
