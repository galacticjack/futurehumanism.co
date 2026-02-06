/**
 * Social Proof Engine - FutureHumanism.co
 * Creates trust signals through simulated activity
 * Uses localStorage for persistence + realistic patterns
 */

(function() {
    'use strict';
    
    const STORAGE_KEY = 'fh_social_proof';
    const TOOL_COUNTS_KEY = 'fh_tool_counts';
    
    // Realistic first names for notifications
    const firstNames = [
        'Alex', 'Sam', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery',
        'Jamie', 'Quinn', 'Drew', 'Parker', 'Skyler', 'Dakota', 'Reese', 'Cameron',
        'Blake', 'Charlie', 'Emery', 'Finley', 'Hayden', 'Jesse', 'Kai', 'Logan',
        'Max', 'Nico', 'Peyton', 'River', 'Sage', 'Sydney', 'Tyler', 'Val',
        'Michael', 'Sarah', 'David', 'Emma', 'James', 'Olivia', 'Robert', 'Sophia',
        'William', 'Isabella', 'Daniel', 'Mia', 'Christopher', 'Charlotte', 'Matthew', 'Amelia'
    ];
    
    // Cities for location context
    const locations = [
        'New York', 'London', 'San Francisco', 'Toronto', 'Sydney', 'Berlin',
        'Singapore', 'Austin', 'Seattle', 'Dublin', 'Amsterdam', 'Vancouver',
        'Chicago', 'Los Angeles', 'Miami', 'Boston', 'Denver', 'Portland',
        'Tokyo', 'Paris', 'Stockholm', 'Melbourne', 'Barcelona', 'Mumbai'
    ];
    
    // Tool names for activity feed
    const tools = [
        { name: 'AI Readiness Quiz', url: '/tools/ai-readiness-quiz.html' },
        { name: 'AI ROI Calculator', url: '/tools/ai-roi-calculator.html' },
        { name: 'Prompt Generator', url: '/tools/prompt-generator.html' },
        { name: 'Automation Savings Calculator', url: '/tools/automation-savings-calculator.html' },
        { name: 'AI Job Analyzer', url: '/tools/ai-job-analyzer.html' },
        { name: 'Headline Analyzer', url: '/tools/headline-analyzer.html' },
        { name: 'AI Skills Gap Analyzer', url: '/tools/ai-skills-gap.html' },
        { name: 'AI Workflow Quiz', url: '/tools/ai-workflow-quiz.html' },
        { name: 'AI Productivity Score', url: '/tools/ai-productivity-score.html' },
        { name: 'AI Use Case Generator', url: '/tools/ai-use-case-generator.html' }
    ];
    
    // Actions for variety
    const actions = [
        'just used the',
        'completed the', 
        'got their results from',
        'tried the',
        'calculated savings with'
    ];
    
    // Initialize or get stored data
    function getStoredData() {
        try {
            const data = localStorage.getItem(STORAGE_KEY);
            if (data) {
                const parsed = JSON.parse(data);
                // Reset if data is more than 24 hours old
                if (Date.now() - parsed.timestamp > 86400000) {
                    return initializeData();
                }
                return parsed;
            }
        } catch (e) {}
        return initializeData();
    }
    
    function initializeData() {
        const data = {
            timestamp: Date.now(),
            totalUsers: Math.floor(Math.random() * 2000) + 8500, // 8500-10500 base
            todayUsers: Math.floor(Math.random() * 50) + 120, // 120-170 today
            toolCounts: {}
        };
        
        // Initialize tool counts
        tools.forEach(tool => {
            data.toolCounts[tool.name] = Math.floor(Math.random() * 3000) + 1500;
        });
        
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        return data;
    }
    
    function saveData(data) {
        data.timestamp = Date.now();
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
    
    function incrementCount(toolName) {
        const data = getStoredData();
        if (data.toolCounts[toolName]) {
            data.toolCounts[toolName]++;
        }
        data.totalUsers++;
        data.todayUsers++;
        saveData(data);
        return data;
    }
    
    function formatNumber(num) {
        if (num >= 1000) {
            return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
        }
        return num.toLocaleString();
    }
    
    function getRandomItem(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }
    
    function getTimeAgo() {
        const options = ['just now', '1 min ago', '2 mins ago', '3 mins ago', '5 mins ago'];
        return options[Math.floor(Math.random() * options.length)];
    }
    
    // ===== ACTIVITY TOAST NOTIFICATIONS =====
    function createActivityToast() {
        // Don't show on mobile (too intrusive)
        if (window.innerWidth < 768) return;
        
        const container = document.getElementById('activity-toast-container');
        if (!container) return;
        
        const name = getRandomItem(firstNames);
        const location = getRandomItem(locations);
        const tool = getRandomItem(tools);
        const action = getRandomItem(actions);
        const timeAgo = getTimeAgo();
        
        const toast = document.createElement('div');
        toast.className = 'activity-toast';
        toast.innerHTML = `
            <div class="activity-toast-icon">🚀</div>
            <div class="activity-toast-content">
                <div class="activity-toast-text">
                    <strong>${name}</strong> from ${location} ${action} <a href="${tool.url}">${tool.name}</a>
                </div>
                <div class="activity-toast-time">${timeAgo}</div>
            </div>
            <button class="activity-toast-close" onclick="this.parentElement.remove()" aria-label="Close">&times;</button>
        `;
        
        container.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remove after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
        
        // Track in GA
        if (typeof gtag === 'function') {
            gtag('event', 'social_proof_toast', { event_category: 'engagement' });
        }
    }
    
    // ===== TOOL COUNTER BADGE =====
    function addToolCounter(toolName) {
        const data = getStoredData();
        const count = data.toolCounts[toolName] || 0;
        
        const counterEl = document.getElementById('tool-usage-counter');
        if (counterEl) {
            counterEl.innerHTML = `<span class="counter-icon">👥</span> ${formatNumber(count)} people have used this tool`;
        }
        
        // Increment on page load (simulates usage)
        setTimeout(() => {
            incrementCount(toolName);
        }, 3000);
    }
    
    // ===== HOMEPAGE STATS COUNTER =====
    function updateHomepageStats() {
        const data = getStoredData();
        
        const totalEl = document.getElementById('total-users-count');
        const todayEl = document.getElementById('today-users-count');
        
        if (totalEl) {
            animateCounter(totalEl, data.totalUsers);
        }
        if (todayEl) {
            animateCounter(todayEl, data.todayUsers);
        }
    }
    
    function animateCounter(element, target) {
        const duration = 1500;
        const start = 0;
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * easeOut);
            element.textContent = formatNumber(current);
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }
    
    // ===== TRENDING NOW TICKER =====
    function createTrendingTicker() {
        const ticker = document.getElementById('trending-ticker');
        if (!ticker) return;
        
        const data = getStoredData();
        
        // Get top 3 tools by count
        const sortedTools = Object.entries(data.toolCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3);
        
        let html = '<span class="ticker-label">🔥 Trending Now:</span>';
        sortedTools.forEach(([name, count], i) => {
            const tool = tools.find(t => t.name === name);
            if (tool) {
                html += `<a href="${tool.url}" class="ticker-item">${name} <span class="ticker-count">(${formatNumber(count)})</span></a>`;
                if (i < sortedTools.length - 1) html += '<span class="ticker-sep">•</span>';
            }
        });
        
        ticker.innerHTML = html;
    }
    
    // ===== INITIALIZATION =====
    function init() {
        const data = getStoredData();
        
        // Add toast container if not exists
        if (!document.getElementById('activity-toast-container')) {
            const container = document.createElement('div');
            container.id = 'activity-toast-container';
            document.body.appendChild(container);
        }
        
        // Homepage: start activity toasts after delay
        if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
            updateHomepageStats();
            createTrendingTicker();
            
            // Show first toast after 8 seconds, then every 25-40 seconds
            setTimeout(createActivityToast, 8000);
            setInterval(() => {
                if (Math.random() > 0.3) { // 70% chance to show
                    createActivityToast();
                }
            }, Math.random() * 15000 + 25000);
        }
        
        // Tool pages: add counter
        const currentTool = tools.find(t => window.location.pathname.includes(t.url.replace('/tools/', '')));
        if (currentTool) {
            addToolCounter(currentTool.name);
        }
    }
    
    // CSS for all social proof elements
    const styles = `
        /* Activity Toast Container */
        #activity-toast-container {
            position: fixed;
            bottom: 24px;
            left: 24px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 12px;
            pointer-events: none;
        }
        
        .activity-toast {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(30, 144, 255, 0.3);
            border-radius: 12px;
            padding: 14px 16px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            max-width: 340px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            opacity: 0;
            transform: translateX(-20px);
            transition: all 0.3s ease;
            pointer-events: auto;
        }
        
        .activity-toast.show {
            opacity: 1;
            transform: translateX(0);
        }
        
        .activity-toast-icon {
            font-size: 1.2rem;
            flex-shrink: 0;
        }
        
        .activity-toast-content {
            flex: 1;
            min-width: 0;
        }
        
        .activity-toast-text {
            color: #e0e0e0;
            font-size: 0.85rem;
            line-height: 1.4;
        }
        
        .activity-toast-text strong {
            color: #ffffff;
        }
        
        .activity-toast-text a {
            color: #1E90FF;
            text-decoration: none;
        }
        
        .activity-toast-text a:hover {
            text-decoration: underline;
        }
        
        .activity-toast-time {
            color: #707070;
            font-size: 0.75rem;
            margin-top: 4px;
        }
        
        .activity-toast-close {
            background: none;
            border: none;
            color: #666;
            font-size: 1.2rem;
            cursor: pointer;
            padding: 0;
            line-height: 1;
            transition: color 0.2s;
        }
        
        .activity-toast-close:hover {
            color: #fff;
        }
        
        /* Tool Usage Counter */
        #tool-usage-counter {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(30, 144, 255, 0.1);
            border: 1px solid rgba(30, 144, 255, 0.2);
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 0.9rem;
            color: #b0b0b0;
            margin: 16px 0;
        }
        
        .counter-icon {
            font-size: 1.1rem;
        }
        
        /* Trending Ticker */
        #trending-ticker {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            padding: 12px 0;
        }
        
        .ticker-label {
            font-weight: 600;
            color: #ffffff;
            font-size: 0.9rem;
        }
        
        .ticker-item {
            color: #1E90FF;
            text-decoration: none;
            font-size: 0.85rem;
            transition: color 0.2s;
        }
        
        .ticker-item:hover {
            color: #3BA0FF;
        }
        
        .ticker-count {
            color: #707070;
            font-size: 0.8rem;
        }
        
        .ticker-sep {
            color: #404040;
        }
        
        /* Social Stats Bar */
        .social-stats-bar {
            display: flex;
            justify-content: center;
            gap: 40px;
            padding: 20px;
            background: rgba(30, 144, 255, 0.05);
            border-top: 1px solid #1a1a1a;
            border-bottom: 1px solid #1a1a1a;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1E90FF;
            display: block;
        }
        
        .stat-label {
            font-size: 0.85rem;
            color: #707070;
            margin-top: 4px;
        }
        
        @media (max-width: 768px) {
            #activity-toast-container {
                display: none;
            }
            
            .social-stats-bar {
                gap: 24px;
                padding: 16px;
            }
            
            .stat-number {
                font-size: 1.4rem;
            }
            
            #trending-ticker {
                justify-content: center;
                text-align: center;
            }
        }
    `;
    
    // Inject styles
    const styleEl = document.createElement('style');
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);
    
    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose for manual use
    window.FHSocialProof = {
        incrementCount,
        getStoredData,
        createActivityToast
    };
})();
