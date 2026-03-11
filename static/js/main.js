// Emotional Support AI - Main JavaScript

// Global state
const AppState = {
    isTyping: false,
    lastActivity: Date.now(),
    notifications: []
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function () {
    // Initialize mobile navigation toggle
    initMobileNav();

    // Add smooth scroll for anchor links
    initSmoothScroll();

    // Add entrance animations
    initAnimations();

    // Initialize tooltips
    initTooltips();

    // Track user activity
    initActivityTracking();
});

// Mobile Navigation
function initMobileNav() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');

            // Animate hamburger
            const spans = navToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
}

// Smooth Scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Animations
function initAnimations() {
    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .stat-item, .step').forEach(el => {
        observer.observe(el);
    });
}

// Tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', function () {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';

            this._tooltip = tooltip;
        });

        el.addEventListener('mouseleave', function () {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Activity Tracking
function initActivityTracking() {
    document.addEventListener('click', () => {
        AppState.lastActivity = Date.now();
    });

    document.addEventListener('keypress', () => {
        AppState.lastActivity = Date.now();
    });
}

// Notification System
function showNotification(message, type = 'info', duration = 3000) {
    // Remove existing notifications of same type
    AppState.notifications.forEach(n => {
        if (n.message === message) n.element.remove();
    });

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;

    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };

    notification.innerHTML = `
        <i class="fas fa-${icons[type] || 'info-circle'}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    // Trigger animation
    requestAnimationFrame(() => {
        notification.classList.add('show');
    });

    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);

    AppState.notifications.push({ message, element: notification });
}

// Date Formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;

    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;

    return formatDate(dateString);
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncate(text, maxLength = 100) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// API Helper
const API = {
    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, message: 'Network error' };
        }
    },

    async get(url) {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, message: 'Network error' };
        }
    }
};

// Local Storage Helpers
const Storage = {
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch {
            return defaultValue;
        }
    },

    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch {
            return false;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch {
            return false;
        }
    },

    clear() {
        try {
            localStorage.clear();
            return true;
        } catch {
            return false;
        }
    }
};

// Scroll Helpers
function scrollToElement(element, offset = 0) {
    const rect = element.getBoundingClientRect();
    window.scrollTo({
        top: rect.top + window.pageYOffset - offset,
        behavior: 'smooth'
    });
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Copy to Clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
        return true;
    } catch {
        showNotification('Failed to copy', 'error');
        return false;
    }
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Lazy load images
function initLazyLoad() {
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
}

// Export functions for global use
window.AppState = AppState;
window.showNotification = showNotification;
window.formatDate = formatDate;
window.formatRelativeTime = formatRelativeTime;
window.debounce = debounce;
window.throttle = throttle;
window.escapeHtml = escapeHtml;
window.truncate = truncate;
window.API = API;
window.Storage = Storage;
window.scrollToElement = scrollToElement;
window.scrollToTop = scrollToTop;
window.copyToClipboard = copyToClipboard;
window.isInViewport = isInViewport;
