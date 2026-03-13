/* ==========================================================================
   Chat Interface Logic
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('messagesContainer')) {
        initChat();
        loadUserStats();
        loadEmotionSummary();
    }
});

async function sendMessage(text) {
    const messageInput = document.getElementById('messageInput');
    const message = text || messageInput.value.trim();

    if (!message) return;

    // Clear input
    messageInput.value = '';

    // Add user message to chat
    addUserMessage(message);

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        if (data.success) {
            addAIMessage(data.message, data.emotion, data.timestamp);
            updateUserStats();
            updateEmotionBars(data.emotion);
        } else {
            if (window.showNotification) {
                window.showNotification(data.message, 'error');
            } else {
                alert(data.message);
            }
        }
    } catch (error) {
        hideTypingIndicator();
        if (window.showNotification) {
            window.showNotification('An error occurred. Please try again.', 'error');
        } else {
            alert('An error occurred. Please try again.');
        }
    }
}

function initChat() {
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');

    if (messageInput && sendBtn) {
        messageInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-focus input
        messageInput.focus();

        // Scroll to bottom
        scrollToBottom();
    }
}

function addUserMessage(text) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-avatar user">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${window.escapeHtml ? window.escapeHtml(text) : text}</div>
        </div>
    `;

    // Remove welcome message if exists
    const welcomeMsg = container.querySelector('.welcome-message');
    if (welcomeMsg) welcomeMsg.remove();

    container.appendChild(messageDiv);
    scrollToBottom();
}

function addAIMessage(text, emotion, timestamp) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';

    const emotionEmojis = {
        happy: '😊',
        sad: '😢',
        anxious: '😰',
        angry: '😠',
        neutral: '😐'
    };

    const emoji = emotionEmojis[emotion] || '😐';
    const formattedTime = new Date(timestamp).toLocaleString();

    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${window.escapeHtml ? window.escapeHtml(text) : text}</div>
            <div class="message-meta">
                <span class="emotion-badge ${emotion}">${emoji} ${emotion}</span>
                <span class="timestamp">${formattedTime}</span>
            </div>
        </div>
    `;

    container.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'flex';
        scrollToBottom();
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

async function loadUserStats() {
    try {
        const response = await fetch('/api/user_stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;
            const totalEl = document.getElementById('totalMessages');
            const daysEl = document.getElementById('activeDays');

            if (totalEl) totalEl.textContent = stats.total || 0;

            if (daysEl && stats.first_seen) {
                const firstSeen = new Date(stats.first_seen);
                const today = new Date();
                const days = Math.ceil((today - firstSeen) / (1000 * 60 * 60 * 24));
                daysEl.textContent = days || 1;
            }
        }
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

async function updateUserStats() {
    const totalEl = document.getElementById('totalMessages');
    if (totalEl) {
        totalEl.textContent = parseInt(totalEl.textContent) + 1;
    }
}

async function loadEmotionSummary() {
    try {
        const response = await fetch('/api/quick_stats');
        const data = await response.json();

        if (data.success && data.emotion_percentages) {
            const percentages = data.emotion_percentages;

            // Update emotion bars
            const bars = {
                happy: document.querySelector('.emotion-bar-fill.happy'),
                sad: document.querySelector('.emotion-bar-fill.sad'),
                anxious: document.querySelector('.emotion-bar-fill.anxious'),
                angry: document.querySelector('.emotion-bar-fill.angry')
            };

            if (bars.happy) bars.happy.style.width = (percentages.happy || 0) + '%';
            if (bars.sad) bars.sad.style.width = (percentages.sad || 0) + '%';
            if (bars.anxious) bars.anxious.style.width = (percentages.anxious || 0) + '%';
            if (bars.angry) bars.angry.style.width = (percentages.angry || 0) + '%';
        }
    } catch (error) {
        console.error('Error loading emotion summary:', error);
    }
}

function updateEmotionBars(emotion) {
    // Increment emotion bar visually (approximation)
    const bar = document.querySelector(`.emotion-bar-fill.${emotion}`);
    if (bar) {
        const currentWidth = parseFloat(bar.style.width) || 0;
        bar.style.width = Math.min(currentWidth + 5, 100) + '%';
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear your chat history? This cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/api/history/clear', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            if (window.showNotification) window.showNotification('Chat history cleared', 'success');
            location.reload();
        } else {
            if (window.showNotification) window.showNotification(data.message, 'error');
        }
    } catch (error) {
        if (window.showNotification) window.showNotification('An error occurred', 'error');
    }
}

async function loadStats() {
    openModal('statsModal');

    const content = document.getElementById('statsContent');
    content.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch('/api/user_stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;
            content.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-value">${stats.total || 0}</span>
                        <span class="stat-label">Total Messages</span>
                    </div>
                </div>
                <h4>Emotion Distribution</h4>
                <div class="emotion-distribution">
                    ${Object.entries(stats.emotions || {}).map(([emotion, count]) => `
                        <div class="emotion-stat">
                            <span class="emotion-name">${emotion}</span>
                            <span class="emotion-count">${count}</span>
                        </div>
                    `).join('') || '<p>No data yet</p>'}
                </div>
            `;
        }
    } catch (error) {
        content.innerHTML = '<p>Error loading statistics</p>';
    }
}

async function exportHistory() {
    openModal('exportModal');

    const content = document.getElementById('exportContent');
    content.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch('/api/export');
        const data = await response.json();

        if (data.success) {
            const jsonStr = JSON.stringify(data.data, null, 2);
            content.innerHTML = `
                <p>Your chat history contains ${data.data.message_count} messages.</p>
                <button class="btn btn-primary" onclick="downloadExport()">
                    <i class="fas fa-download"></i> Download JSON
                </button>
                <textarea id="exportData" style="display:none">${window.escapeHtml ? window.escapeHtml(jsonStr) : jsonStr}</textarea>
            `;
        } else {
            content.innerHTML = '<p>Error loading export data</p>';
        }
    } catch (error) {
        content.innerHTML = '<p>Error loading export data</p>';
    }
}

function downloadExport() {
    const data = document.getElementById('exportData').value;
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat_history.json';
    a.click();
    URL.revokeObjectURL(url);
}

function openPersonalityModal() {
    openModal('personalityModal');
}

async function changePersonality() {
    const personality = document.querySelector('input[name="new_personality"]:checked').value;

    try {
        const response = await fetch('/api/change_personality', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ personality })
        });

        const data = await response.json();

        if (data.success) {
            if (window.showNotification) window.showNotification(`Personality changed to ${personality}`, 'success');
            closeModal('personalityModal');
            location.reload();
        } else {
            if (window.showNotification) window.showNotification(data.message, 'error');
        }
    } catch (error) {
        if (window.showNotification) window.showNotification('An error occurred', 'error');
    }
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// Close modal on outside click
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}

function refreshChat() {
    location.reload();
}

// Global exports if needed
window.sendMessage = sendMessage;
window.clearHistory = clearHistory;
window.loadStats = loadStats;
window.exportHistory = exportHistory;
window.downloadExport = downloadExport;
window.openPersonalityModal = openPersonalityModal;
window.changePersonality = changePersonality;
window.openModal = openModal;
window.closeModal = closeModal;
window.refreshChat = refreshChat;
