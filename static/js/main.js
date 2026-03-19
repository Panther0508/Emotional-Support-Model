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

/* ==========================================================================
   Theme Toggle
   ========================================================================== */
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    if (window.showNotification) {
        window.showNotification(`Switched to ${newTheme} mode`, 'info');
    }
}

function updateThemeIcon(theme) {
    const icons = document.querySelectorAll('.theme-icon');
    icons.forEach(icon => {
        icon.className = theme === 'dark' ? 'fas fa-moon theme-icon' : 'fas fa-sun theme-icon';
    });
}

window.toggleTheme = toggleTheme;

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
});

/* ==========================================================================
   Disclaimer Modal Logic
   ========================================================================== */
window.initDisclaimer = function () {
    const modal = document.getElementById('disclaimerModal');
    const modalTimer = document.getElementById('modalTimer');
    const modalProgress = document.getElementById('modalProgress');
    const modalAcceptBtn = document.getElementById('modalAcceptBtn');

    let remainingTime = 10;
    let countdown = null;
    let isNavigating = false;

    function checkDisclaimer() {
        const currentPath = window.location.pathname;
        if (currentPath !== '/' && currentPath !== '/chat' && currentPath !== '/index') {
            return;
        }

        const accepted = sessionStorage.getItem('disclaimer_accepted');
        const timestamp = sessionStorage.getItem('disclaimer_timestamp');

        if (accepted === 'true' && timestamp) {
            const elapsed = (Date.now() - parseInt(timestamp)) / 1000;
            if (elapsed < 10) {
                remainingTime = Math.ceil(10 - elapsed);
                showModal();
            }
            return;
        }

        remainingTime = 10;
        showModal();
    }

    function showModal() {
        if (modal) {
            modal.style.display = 'flex';
            updateTimerDisplay();
            startCountdown();
        }
    }

    function hideModal() {
        if (modal) {
            modal.style.display = 'none';
            clearInterval(countdown);
        }
    }

    function startCountdown() {
        clearInterval(countdown);
        countdown = setInterval(() => {
            if (isNavigating) {
                clearInterval(countdown);
                return;
            }

            remainingTime--;
            updateTimerDisplay();

            if (remainingTime <= 0) {
                clearInterval(countdown);
                window.acceptDisclaimerModal();
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        if (modalTimer) modalTimer.textContent = remainingTime;
        if (modalProgress) {
            const progress = ((10 - remainingTime) / 10) * 100;
            modalProgress.style.width = progress + '%';
        }
    }

    window.acceptDisclaimerModal = function () {
        if (isNavigating) return;
        isNavigating = true;

        if (modalAcceptBtn) {
            modalAcceptBtn.disabled = true;
            modalAcceptBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Accepting...';
        }

        fetch('/accept-disclaimer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                sessionStorage.setItem('disclaimer_accepted', 'true');
                sessionStorage.setItem('disclaimer_timestamp', Date.now().toString());
                hideModal();
            })
            .catch(error => {
                console.error('Error:', error);
                sessionStorage.setItem('disclaimer_accepted', 'true');
                sessionStorage.setItem('disclaimer_timestamp', Date.now().toString());
                hideModal();
            });
    };

    checkDisclaimer();
};

/* ==========================================================================
   Home Page Statistics Logic
   ========================================================================== */
window.initHomeStats = function (emotionData, totalConversations) {
    function renderEmotionChart() {
        const container = document.getElementById('emotionChart');
        if (!container || !emotionData) return;

        const colors = {
            'happy': '#4CAF50',
            'sad': '#2196F3',
            'anxious': '#FF9800',
            'angry': '#F44336',
            'neutral': '#9E9E9E'
        };

        let html = '';
        for (const [emotion, count] of Object.entries(emotionData)) {
            const percentage = totalConversations > 0 ? Math.round((count / totalConversations) * 100) : 0;
            html += `
                <div class="emotion-bar animate-fade-in" style="margin-bottom: 1.5rem;">
                    <div class="d-flex justify-between mb-2 small text-uppercase tracking-wider">
                        <span class="color-${emotion}">${emotion}</span>
                        <span class="text-muted">${percentage}%</span>
                    </div>
                    <div class="bar-container glass-panel" style="height: 10px; border-radius: 5px; overflow: hidden; background: rgba(255, 255, 255, 0.05);">
                        <div class="bar neon-glow bg-${emotion}" style="width: ${percentage}%; height: 100%; transition: width 1s ease-out;"></div>
                    </div>
                </div>
            `;
        }
        container.innerHTML = html;
    }

    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number[data-count]');

        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count')) || 0;
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            updateCounter();
        });
    }

    animateCounters();
    renderEmotionChart();
};

window.scrollToFeatures = function() {
    const el = document.getElementById('features');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
};
