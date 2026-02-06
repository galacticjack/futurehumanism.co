/**
 * Social Proof Notification System
 * Growth tactic: Creates FOMO by showing reader activity
 * Inspired by Morning Brew's viral growth tactics
 */

(function() {
    'use strict';
    
    // Config
    const CONFIG = {
        notificationDelay: 5000,      // First notification after 5s
        notificationInterval: 25000,  // New notification every 25s
        displayDuration: 6000,        // Each notification visible for 6s
        maxNotifications: 5,          // Max notifications per session
        storageKey: 'fh_social_proof_shown'
    };
    
    // Realistic city data with weights (higher = more common)
    const LOCATIONS = [
        { city: 'San Francisco', country: 'USA', weight: 15 },
        { city: 'New York', country: 'USA', weight: 12 },
        { city: 'London', country: 'UK', weight: 14 },
        { city: 'Austin', country: 'USA', weight: 8 },
        { city: 'Toronto', country: 'Canada', weight: 7 },
        { city: 'Berlin', country: 'Germany', weight: 6 },
        { city: 'Sydney', country: 'Australia', weight: 5 },
        { city: 'Singapore', country: 'Singapore', weight: 8 },
        { city: 'Amsterdam', country: 'Netherlands', weight: 4 },
        { city: 'Seattle', country: 'USA', weight: 7 },
        { city: 'Los Angeles', country: 'USA', weight: 9 },
        { city: 'Dublin', country: 'Ireland', weight: 4 },
        { city: 'Mumbai', country: 'India', weight: 6 },
        { city: 'Tokyo', country: 'Japan', weight: 5 },
        { city: 'Paris', country: 'France', weight: 5 },
        { city: 'Denver', country: 'USA', weight: 4 },
        { city: 'Chicago', country: 'USA', weight: 6 },
        { city: 'Melbourne', country: 'Australia', weight: 4 },
        { city: 'Stockholm', country: 'Sweden', weight: 3 },
        { city: 'Boston', country: 'USA', weight: 5 },
        { city: 'Bangkok', country: 'Thailand', weight: 3 },
        { city: 'Tel Aviv', country: 'Israel', weight: 4 },
        { city: 'Bangalore', country: 'India', weight: 5 },
        { city: 'Vancouver', country: 'Canada', weight: 4 },
        { city: 'Miami', country: 'USA', weight: 4 }
    ];
    
    // Action templates
    const ACTIONS = [
        { text: 'just subscribed', icon: '📬', weight: 30 },
        { text: 'just downloaded the AI Playbook', icon: '📥', weight: 20 },
        { text: 'just took the AI Quiz', icon: '🎯', weight: 15 },
        { text: 'just read an article', icon: '📖', weight: 25 },
        { text: 'just joined 2,400+ readers', icon: '🚀', weight: 10 }
    ];
    
    // Time ago generator
    function getTimeAgo() {
        const options = [
            'just now',
            '1 minute ago',
            '2 minutes ago',
            '3 minutes ago',
            '5 minutes ago'
        ];
        return options[Math.floor(Math.random() * options.length)];
    }
    
    // Weighted random selection
    function weightedRandom(items) {
        const totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (const item of items) {
            random -= item.weight;
            if (random <= 0) return item;
        }
        return items[0];
    }
    
    // Generate notification content
    function generateNotification() {
        const location = weightedRandom(LOCATIONS);
        const action = weightedRandom(ACTIONS);
        const timeAgo = getTimeAgo();
        
        return {
            location: `${location.city}, ${location.country}`,
            action: action.text,
            icon: action.icon,
            time: timeAgo
        };
    }
    
    // Create notification element
    function createNotificationElement() {
        const container = document.createElement('div');
        container.id = 'social-proof-notification';
        container.innerHTML = `
            <div class="sp-inner">
                <div class="sp-icon"></div>
                <div class="sp-content">
                    <div class="sp-text">
                        <strong class="sp-location"></strong>
                        <span class="sp-action"></span>
                    </div>
                    <div class="sp-time"></div>
                </div>
                <button class="sp-close" aria-label="Close">&times;</button>
            </div>
        `;
        
        // Add styles
        const styles = document.createElement('style');
        styles.textContent = `
            #social-proof-notification {
                position: fixed;
                bottom: 24px;
                left: 24px;
                z-index: 9999;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                pointer-events: none;
            }
            #social-proof-notification.sp-visible {
                opacity: 1;
                transform: translateY(0);
                pointer-events: auto;
            }
            .sp-inner {
                display: flex;
                align-items: center;
                gap: 12px;
                background: rgba(26, 26, 26, 0.95);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 14px 18px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
                max-width: 360px;
            }
            .sp-icon {
                font-size: 1.5rem;
                line-height: 1;
            }
            .sp-content {
                flex: 1;
                min-width: 0;
            }
            .sp-text {
                font-size: 0.9rem;
                color: #e0e0e0;
                line-height: 1.4;
            }
            .sp-location {
                color: #fff;
                font-weight: 600;
            }
            .sp-action {
                color: #b0b0b0;
            }
            .sp-time {
                font-size: 0.75rem;
                color: #666;
                margin-top: 4px;
            }
            .sp-close {
                background: none;
                border: none;
                color: #666;
                font-size: 1.2rem;
                cursor: pointer;
                padding: 4px;
                line-height: 1;
                transition: color 0.2s;
            }
            .sp-close:hover {
                color: #fff;
            }
            
            /* Mobile adjustments */
            @media (max-width: 480px) {
                #social-proof-notification {
                    left: 12px;
                    right: 12px;
                    bottom: 12px;
                }
                .sp-inner {
                    max-width: none;
                }
            }
            
            /* Respect prefers-reduced-motion */
            @media (prefers-reduced-motion: reduce) {
                #social-proof-notification {
                    transition: opacity 0.2s;
                    transform: none;
                }
            }
        `;
        
        document.head.appendChild(styles);
        document.body.appendChild(container);
        
        // Close button handler
        container.querySelector('.sp-close').addEventListener('click', () => {
            hideNotification();
            clearInterval(window.spInterval);
            sessionStorage.setItem(CONFIG.storageKey, 'dismissed');
        });
        
        return container;
    }
    
    // Show notification
    function showNotification() {
        const container = document.getElementById('social-proof-notification') || createNotificationElement();
        const data = generateNotification();
        
        container.querySelector('.sp-icon').textContent = data.icon;
        container.querySelector('.sp-location').textContent = data.location;
        container.querySelector('.sp-action').textContent = ' ' + data.action;
        container.querySelector('.sp-time').textContent = data.time;
        
        // Animate in
        requestAnimationFrame(() => {
            container.classList.add('sp-visible');
        });
        
        // Track with GA if available
        if (typeof gtag === 'function') {
            gtag('event', 'social_proof_shown', {
                event_category: 'engagement',
                event_label: data.action
            });
        }
        
        // Auto-hide after duration
        setTimeout(hideNotification, CONFIG.displayDuration);
    }
    
    // Hide notification
    function hideNotification() {
        const container = document.getElementById('social-proof-notification');
        if (container) {
            container.classList.remove('sp-visible');
        }
    }
    
    // Initialize
    function init() {
        // Don't show if already dismissed this session
        if (sessionStorage.getItem(CONFIG.storageKey) === 'dismissed') {
            return;
        }
        
        // Don't show on mobile for better UX (optional - can remove)
        // if (window.innerWidth < 480) return;
        
        let notificationCount = 0;
        
        // First notification after delay
        setTimeout(() => {
            showNotification();
            notificationCount++;
            
            // Subsequent notifications at interval
            window.spInterval = setInterval(() => {
                if (notificationCount >= CONFIG.maxNotifications) {
                    clearInterval(window.spInterval);
                    return;
                }
                showNotification();
                notificationCount++;
            }, CONFIG.notificationInterval);
            
        }, CONFIG.notificationDelay);
    }
    
    // Start when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
