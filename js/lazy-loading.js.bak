/**
 * Lazy Loading Script with Intersection Observer Fallback
 * Provides enhanced image lazy loading for optimal performance
 */

(function() {
    'use strict';
    
    // Check if native lazy loading is supported
    const supportsNativeLazyLoading = 'loading' in HTMLImageElement.prototype;
    
    if (supportsNativeLazyLoading) {
        // Native lazy loading is supported, just ensure all images have the attribute
        const images = document.querySelectorAll('img:not([loading])');
        images.forEach(img => {
            img.setAttribute('loading', 'lazy');
        });
        return;
    }
    
    // Fallback for browsers without native lazy loading support
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                
                // Load the image
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                
                if (img.dataset.srcset) {
                    img.srcset = img.dataset.srcset;
                    img.removeAttribute('data-srcset');
                }
                
                // Remove placeholder class if it exists
                img.classList.remove('lazy-placeholder');
                img.classList.add('lazy-loaded');
                
                // Stop observing this image
                observer.unobserve(img);
            }
        });
    }, {
        // Start loading when image is 50px away from viewport
        rootMargin: '50px 0px',
        threshold: 0.01
    });
    
    // Function to setup lazy loading for images
    function setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src], img[loading="lazy"]:not([data-processed]):not([data-no-lazy])');
        
        images.forEach(img => {
            // Mark as processed to avoid double processing
            img.setAttribute('data-processed', 'true');
            
            // If image has data-src, it's ready for intersection observer
            if (img.dataset.src) {
                imageObserver.observe(img);
                return;
            }
            
            // For images with loading="lazy", move src to data-src for fallback
            if (img.src && !img.dataset.src) {
                img.dataset.src = img.src;
                img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMSIgaGVpZ2h0PSIxIiB2aWV3Qm94PSIwIDAgMSAxIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNmNWY1ZjUiLz48L3N2Zz4=';
            }
            
            if (img.srcset && !img.dataset.srcset) {
                img.dataset.srcset = img.srcset;
                img.removeAttribute('srcset');
            }
            
            // Add placeholder styling
            img.classList.add('lazy-placeholder');
            
            // Observe the image
            imageObserver.observe(img);
        });
    }
    
    // Setup when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupLazyLoading);
    } else {
        setupLazyLoading();
    }
    
    // CSS styles for lazy loading placeholders
    const style = document.createElement('style');
    style.textContent = `
        .lazy-placeholder {
            background-color: #f5f5f5;
            background-image: linear-gradient(90deg, #f5f5f5 25%, #e5e5e5 50%, #f5f5f5 75%);
            background-size: 200% 100%;
            animation: lazy-loading 1.5s infinite;
        }
        
        .lazy-loaded {
            animation: lazy-fade-in 0.3s ease-in-out;
        }
        
        @keyframes lazy-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        @keyframes lazy-fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
})();