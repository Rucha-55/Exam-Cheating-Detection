/* ===========================
   General Utilities
   =========================== */

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===========================
// API Helpers
// ===========================

async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

async function postJSON(url, data) {
    return fetchJSON(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
}

// ===========================
// Notification System
// ===========================

class Notification {
    static show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    static success(message, duration = 3000) {
        this.show(message, 'success', duration);
    }

    static error(message, duration = 5000) {
        this.show(message, 'error', duration);
    }

    static warning(message, duration = 3000) {
        this.show(message, 'warning', duration);
    }
}

// Add notification styles
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    .notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 10000;
        max-width: 300px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        background: #10b981;
    }
    
    .notification-error {
        background: #ef4444;
    }
    
    .notification-warning {
        background: #f59e0b;
    }
    
    .notification-info {
        background: #3b82f6;
    }
`;
document.head.appendChild(notificationStyle);

// ===========================
// Camera Page Functionality
// ===========================

class CheatingDetectionSystem {
    constructor() {
        this.isRunning = false;
        this.sessionStartTime = null;
        this.frameCount = 0;
        this.lastAlerts = [];
        this.statsUpdateInterval = null;
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.sessionStartTime = Date.now();
        this.frameCount = 0;
        this.lastAlerts = [];
        
        this.updateUI();
        this.startStatsUpdate();
        this.startTimer();
        
        Notification.success('Detection started');
    }

    stop() {
        this.isRunning = false;
        if (this.statsUpdateInterval) {
            clearInterval(this.statsUpdateInterval);
        }
        this.updateUI();
        Notification.warning('Detection stopped');
    }

    updateUI() {
        const startBtn = document.getElementById('start-btn');
        const stopBtn = document.getElementById('stop-btn');
        const statusIndicator = document.getElementById('status-indicator');
        
        if (this.isRunning) {
            startBtn.disabled = true;
            stopBtn.disabled = false;
            statusIndicator.style.background = '#d4edda';
            statusIndicator.querySelector('.status-text').textContent = 'Recording';
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
            statusIndicator.style.background = '#f8d7da';
            statusIndicator.querySelector('.status-text').textContent = 'Stopped';
        }
    }

    startTimer() {
        setInterval(() => {
            if (this.isRunning) {
                const elapsed = Math.floor((Date.now() - this.sessionStartTime) / 1000);
                const hours = Math.floor(elapsed / 3600);
                const minutes = Math.floor((elapsed % 3600) / 60);
                const seconds = elapsed % 60;
                
                document.getElementById('timer').textContent = 
                    `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }
        }, 1000);
    }

    startStatsUpdate() {
        const updateStats = async () => {
            if (!this.isRunning) return;
            
            const data = await fetchJSON('/get_results');
            if (!data) return;
            
            // Update scores
            document.getElementById('cheating-score').textContent = data.cheating_score.toFixed(2);
            
            const statusText = data.warning_level === 'critical' ? '🔴 CRITICAL' :
                             data.warning_level === 'warning' ? '🟠 WARNING' : '🟢 SAFE';
            document.getElementById('status-value').textContent = statusText;
            
            // Update indicators
            this.updateAlerts(data.indicators, data.warning_level);
            
            this.frameCount++;
            document.getElementById('frame-count').textContent = this.frameCount;
        };

        this.statsUpdateInterval = setInterval(updateStats, 500);
    }

    updateAlerts(indicators, warningLevel) {
        const alertsContainer = document.getElementById('alerts-container');
        
        if (indicators.length === 0) {
            alertsContainer.innerHTML = '<div class="no-alerts"><p>No suspicious indicators detected</p></div>';
            return;
        }
        
        // Show only new alerts
        const newAlerts = indicators.filter(ind => !this.lastAlerts.includes(ind));
        
        if (newAlerts.length > 0) {
            alertsContainer.innerHTML = indicators.slice(0, 5).map((indicator, idx) => {
                const isNew = newAlerts.includes(indicator);
                return `
                    <div class="alert-item alert-${warningLevel}" ${isNew ? 'style="animation: slideIn 0.3s ease;"' : ''}>
                        <span class="alert-icon">⚠️</span>
                        <span class="alert-text">${indicator}</span>
                        <span class="alert-time">${new Date().toLocaleTimeString()}</span>
                    </div>
                `;
            }).join('');
        }
        
        this.lastAlerts = indicators;
    }

    async saveResults() {
        const data = {
            timestamp: new Date().toISOString(),
            duration: document.getElementById('timer').textContent,
            final_score: document.getElementById('cheating-score').textContent,
            status: document.getElementById('status-value').textContent,
            total_frames: this.frameCount
        };

        const result = await postJSON('/api/results', data);
        if (result) {
            Notification.success('Report saved successfully!');
        } else {
            Notification.error('Failed to save report');
        }
    }
}

// Initialize detection system
let detectionSystem = null;

function initializeCamera() {
    detectionSystem = new CheatingDetectionSystem();
    
    const videoStream = document.getElementById('video-stream');
    const overlay = document.getElementById('video-overlay');
    
    if (videoStream && overlay) {
        videoStream.onload = function() {
            overlay.style.display = 'none';
        };
        
        videoStream.onerror = function() {
            overlay.innerHTML = '<p style="color: red;">Error loading video stream</p>';
            Notification.error('Failed to load video stream');
        };
    }
}

function startDetection() {
    if (detectionSystem) detectionSystem.start();
}

function stopDetection() {
    if (detectionSystem) detectionSystem.stop();
}

function saveResults() {
    if (detectionSystem) detectionSystem.saveResults();
}

// ===========================
// Page Load
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize camera if on camera page
    const videoStream = document.getElementById('video-stream');
    if (videoStream) {
        initializeCamera();
    }
});

// ===========================
// Export Functions
// ===========================

window.startDetection = startDetection;
window.stopDetection = stopDetection;
window.saveResults = saveResults;
window.Notification = Notification;
