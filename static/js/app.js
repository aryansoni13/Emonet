// Emotion Avatar Web Application
class EmotionAvatarApp {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        
        // UI Elements
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.captureBtn = document.getElementById('captureBtn');
        this.emotionEmoji = document.getElementById('emotionEmoji');
        this.emotionText = document.getElementById('emotionText');
        this.emotionDescription = document.getElementById('emotionDescription');
        this.confidenceFill = document.getElementById('confidenceFill');
        this.confidenceText = document.getElementById('confidenceText');
        this.faceStatus = document.getElementById('faceStatus');
        this.emotionTimeline = document.getElementById('emotionTimeline');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        // State
        this.stream = null;
        this.isProcessing = false;
        this.processingInterval = null;
        this.emotionHistory = [];
        this.lastEmotion = null;
        
        // Initialize
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.hideLoading();
    }
    
    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startCamera());
        this.stopBtn.addEventListener('click', () => this.stopCamera());
        this.captureBtn.addEventListener('click', () => this.captureImage());
    }
    
    async startCamera() {
        try {
            this.showLoading('Accessing camera...');
            
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });
            
            this.video.srcObject = this.stream;
            this.video.play();
            
            this.video.addEventListener('loadedmetadata', () => {
                this.canvas.width = this.video.videoWidth;
                this.canvas.height = this.video.videoHeight;
                this.startProcessing();
                this.updateUI('camera', 'started');
                this.hideLoading();
            });
            
        } catch (error) {
            this.hideLoading();
            this.showError('Failed to access camera: ' + error.message);
        }
    }
    
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.stopProcessing();
        this.updateUI('camera', 'stopped');
        this.resetEmotionDisplay();
    }
    
    startProcessing() {
        if (this.processingInterval) return;
        
        this.isProcessing = true;
        this.processingInterval = setInterval(() => {
            this.processFrame();
        }, 300); // Process every 300ms for smooth experience
    }
    
    stopProcessing() {
        this.isProcessing = false;
        if (this.processingInterval) {
            clearInterval(this.processingInterval);
            this.processingInterval = null;
        }
    }
    
    async processFrame() {
        if (!this.isProcessing || !this.stream) return;
        
        try {
            // Draw video frame to canvas
            this.ctx.drawImage(this.video, 0, 0);
            
            // Convert canvas to base64
            const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
            
            // Send to server
            const response = await fetch('/api/process_frame', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });
            
            if (!response.ok) {
                throw new Error('Server error: ' + response.status);
            }
            
            const emotionData = await response.json();
            this.updateEmotionDisplay(emotionData);
            
        } catch (error) {
            console.error('Processing error:', error);
            // Don't show error for every frame, just log it
        }
    }
    
    updateEmotionDisplay(data) {
        // Update emotion display
        this.emotionEmoji.textContent = data.emoji;
        this.emotionText.textContent = data.emotion.charAt(0).toUpperCase() + data.emotion.slice(1);
        this.emotionDescription.textContent = data.description;
        
        // Update confidence
        const confidencePercent = Math.round(data.confidence * 100);
        this.confidenceFill.style.width = confidencePercent + '%';
        this.confidenceText.textContent = confidencePercent + '%';
        
        // Update face detection status
        this.updateFaceStatus(data.face_detected);
        
        // Update emotion history
        if (data.face_detected && data.emotion !== this.lastEmotion) {
            this.addToHistory(data);
            this.lastEmotion = data.emotion;
        }
        
        // Update emotion indicator color
        this.updateEmotionColor(data.color);
    }
    
    updateFaceStatus(detected) {
        const statusElement = this.faceStatus;
        
        if (detected) {
            statusElement.innerHTML = '<i class="fas fa-check-circle"></i> Face Detected';
            statusElement.className = 'status-indicator detected';
        } else {
            statusElement.innerHTML = '<i class="fas fa-times-circle"></i> No Face';
            statusElement.className = 'status-indicator not-detected';
        }
    }
    
    updateEmotionColor(color) {
        const indicator = document.getElementById('emotionIndicator');
        indicator.style.borderColor = color;
        indicator.style.background = `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`;
    }
    
    addToHistory(emotionData) {
        const timestamp = new Date().toLocaleTimeString();
        
        this.emotionHistory.unshift({
            emotion: emotionData.emotion,
            emoji: emotionData.emoji,
            confidence: emotionData.confidence,
            timestamp: timestamp
        });
        
        // Keep only last 10 emotions
        if (this.emotionHistory.length > 10) {
            this.emotionHistory.pop();
        }
        
        this.updateTimeline();
    }
    
    updateTimeline() {
        if (this.emotionHistory.length === 0) {
            this.emotionTimeline.innerHTML = `
                <div class="timeline-placeholder">
                    <i class="fas fa-chart-line"></i>
                    <p>Emotion history will appear here</p>
                </div>
            `;
            return;
        }
        
        this.emotionTimeline.innerHTML = this.emotionHistory.map(item => `
            <div class="emotion-item">
                <span class="emoji">${item.emoji}</span>
                <div class="info">
                    <div class="name">${item.emotion.charAt(0).toUpperCase() + item.emotion.slice(1)}</div>
                    <div class="time">${item.timestamp} (${Math.round(item.confidence * 100)}%)</div>
                </div>
            </div>
        `).join('');
    }
    
    resetEmotionDisplay() {
        this.emotionEmoji.textContent = '😐';
        this.emotionText.textContent = 'Neutral';
        this.emotionDescription.textContent = 'Calm and composed';
        this.confidenceFill.style.width = '0%';
        this.confidenceText.textContent = '0%';
        this.updateFaceStatus(false);
        this.updateEmotionColor('#FFFFFF');
    }
    
    updateUI(action, state) {
        switch (action) {
            case 'camera':
                if (state === 'started') {
                    this.startBtn.disabled = true;
                    this.stopBtn.disabled = false;
                    this.captureBtn.disabled = false;
                } else {
                    this.startBtn.disabled = false;
                    this.stopBtn.disabled = true;
                    this.captureBtn.disabled = true;
                }
                break;
        }
    }
    
    captureImage() {
        if (!this.stream) return;
        
        // Create a temporary canvas for capture
        const captureCanvas = document.createElement('canvas');
        const captureCtx = captureCanvas.getContext('2d');
        
        captureCanvas.width = this.video.videoWidth;
        captureCanvas.height = this.video.videoHeight;
        
        // Draw current frame
        captureCtx.drawImage(this.video, 0, 0);
        
        // Create download link
        const link = document.createElement('a');
        link.download = `emotion-avatar-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.png`;
        link.href = captureCanvas.toDataURL();
        link.click();
    }
    
    showLoading(message = 'Loading...') {
        this.loadingOverlay.style.display = 'flex';
        this.loadingOverlay.querySelector('p').textContent = message;
    }
    
    hideLoading() {
        this.loadingOverlay.style.display = 'none';
    }
    
    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorModal').style.display = 'block';
    }
}

// Global functions for modal
function closeErrorModal() {
    document.getElementById('errorModal').style.display = 'none';
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EmotionAvatarApp();
});

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('errorModal');
    if (event.target === modal) {
        closeErrorModal();
    }
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, could pause processing here if needed
        console.log('Page hidden');
    } else {
        // Page is visible again
        console.log('Page visible');
    }
}); 