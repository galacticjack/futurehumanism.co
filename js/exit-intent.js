/**
 * Exit-Intent Popup System
 * Growth tactic: Capture 10-15% of abandoning visitors
 * 
 * Features:
 * - Desktop: Detects mouse leaving viewport
 * - Mobile: Detects rapid scroll-up + time on page
 * - Smart throttling: Only shows once per session
 * - Lead magnet focus: Free AI Playbook download
 */

(function() {
    'use strict';
    
    const CONFIG = {
        cookieName: 'fh_exit_popup_shown',
        cookieDays: 7,                    // Don't show again for 7 days
        minTimeOnPage: 15000,             // Wait 15s before enabling
        mobileScrollThreshold: -100,      // Pixels scrolled up to trigger
        mobileTimeThreshold: 3000,        // Time window for scroll detection
        leadMagnetUrl: '/free-guide/ai-playbook.pdf',
        beehiivUrl: 'https://futurehumanism.beehiiv.com/subscribe'
    };
    
    // Check if popup already shown
    function hasSeenPopup() {
        return document.cookie.includes(CONFIG.cookieName + '=true') ||
               sessionStorage.getItem(CONFIG.cookieName) === 'true';
    }
    
    // Set popup shown flag
    function markPopupShown() {
        sessionStorage.setItem(CONFIG.cookieName, 'true');
        const date = new Date();
        date.setTime(date.getTime() + (CONFIG.cookieDays * 24 * 60 * 60 * 1000));
        document.cookie = `${CONFIG.cookieName}=true; expires=${date.toUTCString()}; path=/; SameSite=Lax`;
    }
    
    // Check if on a tool page (has its own capture flow)
    function isToolPage() {
        return window.location.pathname.includes('/tools/') ||
               window.location.pathname.includes('/quiz');
    }
    
    // Create popup HTML
    function createPopup() {
        const overlay = document.createElement('div');
        overlay.id = 'exit-intent-popup';
        overlay.className = 'exit-popup-overlay';
        overlay.innerHTML = `
            <div class="exit-popup-modal">
                <button class="exit-popup-close" aria-label="Close">&times;</button>
                
                <div class="exit-popup-content">
                    <div class="exit-popup-icon">📥</div>
                    <h2 class="exit-popup-title">Wait! Grab Your Free AI Playbook</h2>
                    <p class="exit-popup-subtitle">50+ prompts, tool recommendations, and workflows used by 10,000+ professionals.</p>
                    
                    <ul class="exit-popup-benefits">
                        <li>
                            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
                            Productivity prompts that actually work
                        </li>
                        <li>
                            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
                            Tool comparison cheat sheet
                        </li>
                        <li>
                            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
                            Weekly AI insights newsletter
                        </li>
                    </ul>
                    
                    <form class="exit-popup-form" id="exit-popup-form">
                        <input 
                            type="email" 
                            class="exit-popup-input" 
                            placeholder="Enter your email" 
                            required 
                            id="exit-popup-email"
                        >
                        <button type="submit" class="exit-popup-submit">
                            Get Free Playbook
                            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                        </button>
                    </form>
                    
                    <p class="exit-popup-privacy">No spam. Unsubscribe anytime.</p>
                </div>
                
                <button class="exit-popup-skip">No thanks, I'll figure it out myself</button>
            </div>
        `;
        
        // Add styles
        const styles = document.createElement('style');
        styles.textContent = `
            .exit-popup-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.85);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 99999;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease, visibility 0.3s ease;
                padding: 1rem;
                backdrop-filter: blur(4px);
            }
            .exit-popup-overlay.active {
                opacity: 1;
                visibility: visible;
            }
            .exit-popup-modal {
                background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                max-width: 440px;
                width: 100%;
                padding: 2rem;
                transform: scale(0.9) translateY(20px);
                transition: transform 0.3s ease;
                position: relative;
                box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5);
            }
            .exit-popup-overlay.active .exit-popup-modal {
                transform: scale(1) translateY(0);
            }
            .exit-popup-close {
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(255, 255, 255, 0.1);
                border: none;
                color: #888;
                cursor: pointer;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                font-size: 1.25rem;
                line-height: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
            }
            .exit-popup-close:hover {
                background: rgba(255, 255, 255, 0.15);
                color: #fff;
            }
            .exit-popup-content {
                text-align: center;
            }
            .exit-popup-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
                animation: bounce 2s ease infinite;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-8px); }
            }
            .exit-popup-title {
                font-size: 1.6rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 0.5rem;
                line-height: 1.25;
            }
            .exit-popup-subtitle {
                color: #b0b0b0;
                font-size: 0.95rem;
                margin-bottom: 1.25rem;
                line-height: 1.5;
            }
            .exit-popup-benefits {
                list-style: none;
                padding: 0;
                margin: 0 0 1.5rem 0;
                text-align: left;
            }
            .exit-popup-benefits li {
                display: flex;
                align-items: center;
                gap: 0.6rem;
                color: #e0e0e0;
                font-size: 0.9rem;
                margin-bottom: 0.6rem;
            }
            .exit-popup-benefits svg {
                flex-shrink: 0;
                color: #22c55e;
            }
            .exit-popup-form {
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
            }
            .exit-popup-input {
                width: 100%;
                padding: 0.9rem 1rem;
                font-size: 1rem;
                border: 2px solid #2a2a2a;
                border-radius: 10px;
                background: #141414;
                color: #fff;
                outline: none;
                transition: border-color 0.2s;
            }
            .exit-popup-input:focus {
                border-color: #1E90FF;
            }
            .exit-popup-input::placeholder {
                color: #666;
            }
            .exit-popup-submit {
                width: 100%;
                padding: 0.9rem 1.25rem;
                font-size: 1rem;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                background: linear-gradient(135deg, #1E90FF 0%, #00BFFF 100%);
                color: #fff;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .exit-popup-submit:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(30, 144, 255, 0.35);
            }
            .exit-popup-submit:active {
                transform: translateY(0);
            }
            .exit-popup-privacy {
                font-size: 0.75rem;
                color: #666;
                margin-top: 0.75rem;
            }
            .exit-popup-skip {
                background: none;
                border: none;
                color: #555;
                font-size: 0.8rem;
                cursor: pointer;
                margin-top: 1rem;
                width: 100%;
                text-align: center;
                transition: color 0.2s;
            }
            .exit-popup-skip:hover {
                color: #888;
            }
            
            /* Success state */
            .exit-popup-success {
                text-align: center;
                padding: 1rem 0;
            }
            .exit-popup-success-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            .exit-popup-success h3 {
                color: #fff;
                font-size: 1.4rem;
                margin-bottom: 0.5rem;
            }
            .exit-popup-success p {
                color: #b0b0b0;
                font-size: 0.95rem;
            }
            
            /* Mobile styles */
            @media (max-width: 480px) {
                .exit-popup-modal {
                    padding: 1.5rem;
                    margin: 0.5rem;
                }
                .exit-popup-title {
                    font-size: 1.35rem;
                }
                .exit-popup-icon {
                    font-size: 2.5rem;
                }
            }
            
            /* Reduced motion */
            @media (prefers-reduced-motion: reduce) {
                .exit-popup-overlay,
                .exit-popup-modal {
                    transition: opacity 0.2s ease;
                }
                .exit-popup-modal {
                    transform: none;
                }
                .exit-popup-icon {
                    animation: none;
                }
            }
        `;
        
        document.head.appendChild(styles);
        document.body.appendChild(overlay);
        
        return overlay;
    }
    
    // Show popup
    function showPopup() {
        if (hasSeenPopup() || isToolPage()) return;
        
        const popup = createPopup();
        
        // Animate in
        requestAnimationFrame(() => {
            popup.classList.add('active');
        });
        
        // Mark as shown
        markPopupShown();
        
        // Track with GA
        if (typeof gtag === 'function') {
            gtag('event', 'exit_intent_shown', {
                event_category: 'conversion',
                event_label: 'ai_playbook'
            });
        }
        
        // Set up handlers
        setupPopupHandlers(popup);
    }
    
    // Setup event handlers
    function setupPopupHandlers(popup) {
        const closeBtn = popup.querySelector('.exit-popup-close');
        const skipBtn = popup.querySelector('.exit-popup-skip');
        const form = popup.querySelector('#exit-popup-form');
        const emailInput = popup.querySelector('#exit-popup-email');
        const modal = popup.querySelector('.exit-popup-modal');
        
        function closePopup() {
            popup.classList.remove('active');
            setTimeout(() => popup.remove(), 300);
        }
        
        // Close handlers
        closeBtn.addEventListener('click', closePopup);
        skipBtn.addEventListener('click', () => {
            if (typeof gtag === 'function') {
                gtag('event', 'exit_intent_skip', { event_category: 'conversion' });
            }
            closePopup();
        });
        
        // Close on overlay click
        popup.addEventListener('click', (e) => {
            if (e.target === popup) closePopup();
        });
        
        // Escape key
        document.addEventListener('keydown', function escHandler(e) {
            if (e.key === 'Escape') {
                closePopup();
                document.removeEventListener('keydown', escHandler);
            }
        });
        
        // Form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = emailInput.value.trim();
            
            if (!email || !email.includes('@')) return;
            
            // Track conversion
            if (typeof gtag === 'function') {
                gtag('event', 'exit_intent_convert', {
                    event_category: 'conversion',
                    event_label: 'ai_playbook',
                    value: 1
                });
            }
            
            // Store email
            localStorage.setItem('fh_subscriber_email', email);
            
            // Show success
            popup.querySelector('.exit-popup-content').innerHTML = `
                <div class="exit-popup-success">
                    <div class="exit-popup-success-icon">🎉</div>
                    <h3>You're in!</h3>
                    <p>Check your inbox for the AI Playbook. Welcome to Future Humanism!</p>
                </div>
            `;
            popup.querySelector('.exit-popup-skip').style.display = 'none';
            
            // Redirect to Beehiiv after delay
            setTimeout(() => {
                const beehiivUrl = `${CONFIG.beehiivUrl}?email=${encodeURIComponent(email)}&utm_source=exit_intent&utm_medium=popup`;
                window.location.href = beehiivUrl;
            }, 2000);
        });
        
        // Focus input
        setTimeout(() => emailInput.focus(), 300);
    }
    
    // Desktop: Mouse leave detection
    function setupDesktopDetection() {
        let triggered = false;
        
        document.addEventListener('mouseout', (e) => {
            if (triggered || hasSeenPopup()) return;
            
            // Check if mouse is leaving the viewport from the top
            if (e.clientY < 10 && !e.relatedTarget && !e.toElement) {
                triggered = true;
                showPopup();
            }
        });
    }
    
    // Mobile: Scroll-up detection
    function setupMobileDetection() {
        let lastScrollY = window.scrollY;
        let scrollStartTime = 0;
        let triggered = false;
        
        window.addEventListener('scroll', () => {
            if (triggered || hasSeenPopup()) return;
            
            const currentScrollY = window.scrollY;
            const scrollDelta = currentScrollY - lastScrollY;
            
            // User is scrolling up
            if (scrollDelta < 0) {
                if (scrollStartTime === 0) {
                    scrollStartTime = Date.now();
                }
                
                // Check if scrolled up enough and fast enough
                const timeElapsed = Date.now() - scrollStartTime;
                if (scrollDelta < CONFIG.mobileScrollThreshold && timeElapsed < CONFIG.mobileTimeThreshold) {
                    // Only trigger if user has scrolled down at least 50% of page first
                    const pageHeight = document.documentElement.scrollHeight - window.innerHeight;
                    if (lastScrollY > pageHeight * 0.5) {
                        triggered = true;
                        showPopup();
                    }
                }
            } else {
                scrollStartTime = 0;
            }
            
            lastScrollY = currentScrollY;
        }, { passive: true });
    }
    
    // Initialize
    function init() {
        // Don't run if already shown or on tool pages
        if (hasSeenPopup() || isToolPage()) return;
        
        // Wait for minimum time on page
        setTimeout(() => {
            const isMobile = window.innerWidth < 768 || 'ontouchstart' in window;
            
            if (isMobile) {
                setupMobileDetection();
            } else {
                setupDesktopDetection();
            }
        }, CONFIG.minTimeOnPage);
    }
    
    // Start when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
