// Lazy loading fallback for browsers that don't support native lazy loading
(function() {
    // Check if native lazy loading is supported
    if ('loading' in HTMLImageElement.prototype) {
        return; // Native lazy loading is supported, no fallback needed
    }

    // Fallback for older browsers using Intersection Observer
    function lazyLoad() {
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.src; // Trigger loading
                        img.removeAttribute('loading');
                        observer.unobserve(img);
                    }
                });
            });

            lazyImages.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for very old browsers - load all images immediately
            lazyImages.forEach(img => {
                img.removeAttribute('loading');
            });
        }
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', lazyLoad);
    } else {
        lazyLoad();
    }
})();