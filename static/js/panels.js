// Panels JavaScript functionality

// Panel management
let currentPanel = null;

// Initialize panels
document.addEventListener('DOMContentLoaded', function() {
    initializePanels();
    initializeSearch();
    initializeNotifications();
});

function initializePanels() {
    // Add panel overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-panel-overlay';
    overlay.id = 'panel-overlay';
    document.body.appendChild(overlay);
    
    // Close panels when clicking overlay
    overlay.addEventListener('click', function() {
        closeAllPanels();
    });
    
    // Close panels with ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllPanels();
        }
    });
}

// Panel control functions
function openPanel(panelId) {
    closeAllPanels();
    
    const panel = document.getElementById(panelId);
    const overlay = document.getElementById('panel-overlay');
    
    if (panel && overlay) {
        panel.classList.add('active');
        overlay.classList.add('active');
        currentPanel = panelId;
        document.body.style.overflow = 'hidden';
    }
}

function closeAllPanels() {
    const panels = ['search-panel', 'map-panel', 'notification-panel'];
    const overlay = document.getElementById('panel-overlay');
    
    panels.forEach(panelId => {
        const panel = document.getElementById(panelId);
        if (panel) {
            panel.classList.remove('active');
        }
    });
    
    if (overlay) {
        overlay.classList.remove('active');
    }
    
    currentPanel = null;
    document.body.style.overflow = '';
}

// Specific panel functions
function closeSearchPanel() {
    const panel = document.getElementById('search-panel');
    const overlay = document.getElementById('panel-overlay');
    
    if (panel) panel.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    
    currentPanel = null;
    document.body.style.overflow = '';
}

function closeMapPanel() {
    const panel = document.getElementById('map-panel');
    const overlay = document.getElementById('panel-overlay');
    
    if (panel) panel.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    
    currentPanel = null;
    document.body.style.overflow = '';
}

function closeNotificationPanel() {
    const panel = document.getElementById('notification-panel');
    const overlay = document.getElementById('panel-overlay');
    
    if (panel) panel.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    
    currentPanel = null;
    document.body.style.overflow = '';
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input-field');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    // Load recent searches from localStorage
    loadRecentSearches();
}

function performSearch() {
    const searchInput = document.getElementById('search-input-field');
    const searchTerm = searchInput ? searchInput.value.trim() : '';
    
    if (searchTerm) {
        console.log('Searching for:', searchTerm);
        
        // Add to recent searches
        addToRecentSearches(searchTerm);
        
        // Here you would implement actual search functionality
        // For now, just show a placeholder result
        showSearchResults(searchTerm);
    }
}

function searchFor(term) {
    const searchInput = document.getElementById('search-input-field');
    if (searchInput) {
        searchInput.value = term;
        performSearch();
    }
}

function showSearchResults(term) {
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="search-results-content">
                <h4>Search Results for "${term}"</h4>
                <div class="result-item">
                    <h5>Location: ${term}</h5>
                    <p>Weather data and flood risk information for ${term}</p>
                    <button class="view-details-btn" onclick="viewLocationDetails('${term}')">
                        View Details
                    </button>
                </div>
            </div>
        `;
    }
}

function addToRecentSearches(term) {
    let recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    
    // Remove if already exists
    recentSearches = recentSearches.filter(item => item !== term);
    
    // Add to beginning
    recentSearches.unshift(term);
    
    // Keep only last 5
    recentSearches = recentSearches.slice(0, 5);
    
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
    loadRecentSearches();
}

function loadRecentSearches() {
    const recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    const recentList = document.getElementById('recent-searches-list');
    
    if (recentList) {
        if (recentSearches.length > 0) {
            recentList.innerHTML = recentSearches.map(term => 
                `<div class="recent-item" onclick="searchFor('${term}')">${term}</div>`
            ).join('');
        } else {
            recentList.innerHTML = '<div class="no-recent">No recent searches</div>';
        }
    }
}

function viewLocationDetails(location) {
    console.log('Viewing details for:', location);
    // Implement location details view
}

// Map functionality
function centerMap() {
    console.log('Centering map...');
    // Implement map centering
}

function toggleLayers() {
    console.log('Toggling map layers...');
    // Implement layer toggling
}

// Notification functionality
function initializeNotifications() {
    updateNotificationCount();
}

function filterNotifications(type) {
    const notifications = document.querySelectorAll('.notification-item');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    // Update active filter button
    filterBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter notifications
    notifications.forEach(notification => {
        if (type === 'all' || notification.classList.contains(type)) {
            notification.style.display = 'flex';
        } else {
            notification.style.display = 'none';
        }
    });
}

function markAsRead(button) {
    const notification = button.closest('.notification-item');
    if (notification) {
        notification.style.opacity = '0.5';
        button.style.display = 'none';
        updateNotificationCount();
    }
}

function markAllAsRead() {
    const notifications = document.querySelectorAll('.notification-item');
    const actionBtns = document.querySelectorAll('.action-btn');
    
    notifications.forEach(notification => {
        notification.style.opacity = '0.5';
    });
    
    actionBtns.forEach(btn => {
        btn.style.display = 'none';
    });
    
    updateNotificationCount();
}

function clearAllNotifications() {
    const notificationsList = document.getElementById('notifications-list');
    if (notificationsList) {
        notificationsList.innerHTML = '<div class="no-notifications">No notifications</div>';
        updateNotificationCount();
    }
}

function updateNotificationCount() {
    const unreadNotifications = document.querySelectorAll('.notification-item:not([style*="opacity: 0.5"])');
    const countElement = document.getElementById('notification-count');
    
    if (countElement) {
        countElement.textContent = unreadNotifications.length;
    }
}

// Global functions for navbar integration
function openSearchPanel() {
    openPanel('search-panel');
}

function openMapPanel() {
    openPanel('map-panel');
}

function openNotificationPanel() {
    openPanel('notification-panel');
}

