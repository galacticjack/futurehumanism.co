// Stories Pagination - Standalone
(function() {
    'use strict';
    
    var currentPage = 1;
    var perPage = 12;
    var totalPages = 1;
    var cards = [];
    
    function init() {
        var grid = document.getElementById('stories-grid');
        var prevBtn = document.getElementById('storiesPrev');
        var nextBtn = document.getElementById('storiesNext');
        var pageSpan = document.getElementById('storiesPage');
        var totalSpan = document.getElementById('storiesTotalPages');
        
        if (!grid || !prevBtn || !nextBtn || !pageSpan || !totalSpan) {
            console.log('Pagination: Missing elements');
            return;
        }
        
        cards = Array.from(grid.querySelectorAll('.grid-story-card'));
        totalPages = Math.ceil(cards.length / perPage);
        totalSpan.textContent = totalPages;
        
        console.log('Pagination ready:', cards.length, 'cards,', totalPages, 'pages');
        
        // Attach click handlers
        prevBtn.onclick = function() {
            if (currentPage > 1) {
                showPage(currentPage - 1);
            }
        };
        
        nextBtn.onclick = function() {
            if (currentPage < totalPages) {
                showPage(currentPage + 1);
            }
        };
        
        showPage(1);
    }
    
    function showPage(page) {
        currentPage = page;
        
        var pageSpan = document.getElementById('storiesPage');
        var prevBtn = document.getElementById('storiesPrev');
        var nextBtn = document.getElementById('storiesNext');
        
        if (pageSpan) pageSpan.textContent = page;
        
        var start = (page - 1) * perPage;
        var end = start + perPage;
        
        cards.forEach(function(card, i) {
            card.style.display = (i >= start && i < end) ? 'block' : 'none';
        });
        
        if (prevBtn) prevBtn.disabled = page <= 1;
        if (nextBtn) nextBtn.disabled = page >= totalPages;
        
        // Scroll to stories section on page change (except page 1)
        if (page > 1) {
            var storiesSection = document.getElementById('stories');
            if (storiesSection) {
                storiesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
