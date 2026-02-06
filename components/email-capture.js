/**
 * Email Capture Component for FutureHumanism Tools
 * Captures emails at peak engagement (after quiz/calculator results)
 * 
 * Usage:
 * 1. Include this script
 * 2. Call showEmailCapture({ score: 85, toolName: 'AI Productivity Score', type: 'quiz' })
 * 3. On submit, redirects to Beehiiv with email
 */

(function() {
    // Inject styles
    const styles = `
        .fh-email-capture-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s;
            padding: 1rem;
        }
        .fh-email-capture-overlay.active {
            opacity: 1;
            visibility: visible;
        }
        .fh-email-capture-modal {
            background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            max-width: 480px;
            width: 100%;
            padding: 2.5rem;
            transform: translateY(20px);
            transition: transform 0.3s;
            position: relative;
        }
        .fh-email-capture-overlay.active .fh-email-capture-modal {
            transform: translateY(0);
        }
        .fh-email-capture-close {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            color: #707070;
            cursor: pointer;
            padding: 0.5rem;
            font-size: 1.5rem;
            line-height: 1;
        }
        .fh-email-capture-close:hover {
            color: #fff;
        }
        .fh-email-capture-badge {
            display: inline-block;
            background: linear-gradient(135deg, #1E90FF 0%, #00BFFF 100%);
            color: #fff;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .fh-email-capture-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.75rem;
            line-height: 1.2;
        }
        .fh-email-capture-subtitle {
            color: #b0b0b0;
            font-size: 1rem;
            margin-bottom: 1.5rem;
            line-height: 1.5;
        }
        .fh-email-capture-benefits {
            list-style: none;
            padding: 0;
            margin: 0 0 1.5rem 0;
        }
        .fh-email-capture-benefits li {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            color: #e0e0e0;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
        .fh-email-capture-benefits svg {
            flex-shrink: 0;
            color: #22c55e;
            margin-top: 2px;
        }
        .fh-email-capture-form {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        .fh-email-capture-input {
            width: 100%;
            padding: 1rem 1.25rem;
            font-size: 1rem;
            border: 1px solid #2a2a2a;
            border-radius: 8px;
            background: #141414;
            color: #fff;
            outline: none;
            transition: border-color 0.2s;
        }
        .fh-email-capture-input:focus {
            border-color: #1E90FF;
        }
        .fh-email-capture-input::placeholder {
            color: #707070;
        }
        .fh-email-capture-submit {
            width: 100%;
            padding: 1rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            background: linear-gradient(135deg, #1E90FF 0%, #00BFFF 100%);
            color: #fff;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .fh-email-capture-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(30, 144, 255, 0.4);
        }
        .fh-email-capture-submit:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .fh-email-capture-privacy {
            font-size: 0.8rem;
            color: #707070;
            text-align: center;
            margin-top: 1rem;
        }
        .fh-email-capture-privacy a {
            color: #1E90FF;
            text-decoration: none;
        }
        .fh-email-capture-skip {
            background: none;
            border: none;
            color: #707070;
            font-size: 0.85rem;
            cursor: pointer;
            margin-top: 0.75rem;
            text-align: center;
            display: block;
            width: 100%;
        }
        .fh-email-capture-skip:hover {
            color: #b0b0b0;
        }
        @media (max-width: 480px) {
            .fh-email-capture-modal {
                padding: 1.5rem;
            }
            .fh-email-capture-title {
                font-size: 1.5rem;
            }
        }
    `;
    
    const styleEl = document.createElement('style');
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);
    
    // Create modal HTML
    function createModal(options) {
        const { score, toolName, type } = options;
        
        // Determine messaging based on score
        let headline, subtitle;
        if (score >= 80) {
            headline = "You're an AI Power User!";
            subtitle = "Get advanced strategies to stay ahead of the curve.";
        } else if (score >= 60) {
            headline = "You're Making Progress!";
            subtitle = "Get personalized tips to level up faster.";
        } else {
            headline = "Time to Level Up!";
            subtitle = "Get your personalized AI improvement plan.";
        }
        
        const modal = document.createElement('div');
        modal.className = 'fh-email-capture-overlay';
        modal.id = 'fh-email-capture';
        modal.innerHTML = `
            <div class="fh-email-capture-modal">
                <button class="fh-email-capture-close" aria-label="Close">&times;</button>
                <span class="fh-email-capture-badge">Free Report</span>
                <h2 class="fh-email-capture-title">${headline}</h2>
                <p class="fh-email-capture-subtitle">${subtitle} Get your detailed ${toolName} report delivered to your inbox.</p>
                <ul class="fh-email-capture-benefits">
                    <li>
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
                        Personalized improvement recommendations
                    </li>
                    <li>
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
                        Weekly AI tips and tool updates
                    </li>
                    <li>
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
                        Early access to new tools and guides
                    </li>
                </ul>
                <form class="fh-email-capture-form" id="fh-email-form">
                    <input type="email" class="fh-email-capture-input" placeholder="Enter your email" required id="fh-email-input">
                    <button type="submit" class="fh-email-capture-submit">Send My Report</button>
                </form>
                <p class="fh-email-capture-privacy">We respect your privacy. <a href="/privacy.html">Unsubscribe anytime.</a></p>
                <button class="fh-email-capture-skip" id="fh-skip-btn">No thanks, I'll skip the report</button>
            </div>
        `;
        
        return modal;
    }
    
    // Show email capture modal
    window.showEmailCapture = function(options) {
        // Don't show if already captured in this session
        if (sessionStorage.getItem('fh_email_captured')) {
            return;
        }
        
        // Remove existing modal if any
        const existing = document.getElementById('fh-email-capture');
        if (existing) existing.remove();
        
        const modal = createModal(options);
        document.body.appendChild(modal);
        
        // Trigger animation
        requestAnimationFrame(() => {
            modal.classList.add('active');
        });
        
        // Close handlers
        const closeBtn = modal.querySelector('.fh-email-capture-close');
        const skipBtn = modal.querySelector('#fh-skip-btn');
        
        function closeModal() {
            modal.classList.remove('active');
            setTimeout(() => modal.remove(), 300);
        }
        
        closeBtn.addEventListener('click', closeModal);
        skipBtn.addEventListener('click', () => {
            sessionStorage.setItem('fh_email_skipped', 'true');
            closeModal();
            // Track skip
            if (typeof gtag !== 'undefined') {
                gtag('event', 'email_capture_skip', {
                    'event_category': 'conversion',
                    'event_label': options.toolName
                });
            }
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
        
        // Form submission
        const form = modal.querySelector('#fh-email-form');
        const input = modal.querySelector('#fh-email-input');
        
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = input.value.trim();
            
            if (!email || !email.includes('@')) return;
            
            // Mark as captured
            sessionStorage.setItem('fh_email_captured', 'true');
            localStorage.setItem('fh_subscriber_email', email);
            
            // Track conversion
            if (typeof gtag !== 'undefined') {
                gtag('event', 'email_capture', {
                    'event_category': 'conversion',
                    'event_label': options.toolName,
                    'value': 1
                });
            }
            
            // Redirect to Beehiiv subscription
            const beehiivUrl = `https://futurehumanism.beehiiv.com/subscribe?email=${encodeURIComponent(email)}&utm_source=tool&utm_medium=${encodeURIComponent(options.toolName)}`;
            window.location.href = beehiivUrl;
        });
        
        // Auto-focus input
        setTimeout(() => input.focus(), 300);
        
        // Track impression
        if (typeof gtag !== 'undefined') {
            gtag('event', 'email_capture_shown', {
                'event_category': 'conversion',
                'event_label': options.toolName
            });
        }
    };
    
    // Auto-trigger after delay when results shown (optional)
    window.triggerEmailCaptureOnResults = function(options, delayMs = 3000) {
        setTimeout(() => {
            showEmailCapture(options);
        }, delayMs);
    };
})();
