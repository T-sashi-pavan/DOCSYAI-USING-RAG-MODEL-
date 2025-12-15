const API_BASE_URL = 'http://localhost:10000';
let queryCount = 0;

// DOM Elements
const uploadCard = document.getElementById('uploadCard');
const pdfInput = document.getElementById('pdfInput');
const uploadProgress = document.getElementById('uploadProgress');
const statusText = document.getElementById('statusText');
const statusDot = document.getElementById('statusDot');
const statusBox = document.querySelector('.status-box');
const totalChunks = document.getElementById('totalChunks');
const queryCountEl = document.getElementById('queryCount');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const clearBtn = document.getElementById('clearBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // File upload - click
    uploadCard.addEventListener('click', () => {
        pdfInput.click();
    });

    // File upload - change
    pdfInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadCard.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadCard.style.background = 'rgba(255, 255, 255, 0.25)';
    });

    uploadCard.addEventListener('dragleave', () => {
        uploadCard.style.background = 'rgba(255, 255, 255, 0.15)';
    });

    uploadCard.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadCard.style.background = 'rgba(255, 255, 255, 0.15)';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFileUpload(file);
        } else {
            showError('Please upload a PDF file');
        }
    });

    // Send question
    sendBtn.addEventListener('click', handleSendQuestion);
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendQuestion();
        }
    });

    // Clear chat
    clearBtn.addEventListener('click', handleClearChat);
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
}

// Handle file upload
async function handleFileUpload(file) {
    if (!file.type.includes('pdf')) {
        showError('Please select a PDF file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        // Show uploading state
        uploadCard.classList.add('uploading');
        statusText.textContent = 'Uploading & Processing...';
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showSuccess(`✓ Uploaded: ${file.name}`);
            statusText.textContent = 'Ready to answer questions';
            statusBox.classList.add('ready');
            questionInput.disabled = false;
            sendBtn.disabled = false;
            
            // Update stats
            await loadStats();

            // Add welcome message
            addMessage(`PDF "${file.name}" loaded successfully! You can now ask questions about it.`, 'bot');
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('Upload failed: ' + error.message);
        statusText.textContent = 'Upload failed';
    } finally {
        uploadCard.classList.remove('uploading');
    }
}

// Handle send question
async function handleSendQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) return;

    // Add user message
    addMessage(question, 'user');
    questionInput.value = '';

    // Add loading message
    const loadingMsg = addLoadingMessage();

    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // Remove loading message
        loadingMsg.remove();

        if (response.ok) {
            addMessage(data.answer, 'bot');
            queryCount++;
            queryCountEl.textContent = queryCount;
        } else {
            throw new Error(data.error || 'Failed to get answer');
        }
    } catch (error) {
        console.error('Question error:', error);
        loadingMsg.remove();
        addMessage('Sorry, I encountered an error: ' + error.message, 'bot');
    }
}

// Add message to chat
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

// Add loading message
function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot loading';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

// Load stats
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        if (response.ok) {
            totalChunks.textContent = data.total_chunks || 0;
            
            // Update status if document is loaded
            if (data.total_chunks > 0) {
                statusText.textContent = 'Ready to answer questions';
                statusBox.classList.add('ready');
                questionInput.disabled = false;
                sendBtn.disabled = false;
            }
        }
    } catch (error) {
        console.error('Stats error:', error);
    }
}

// Clear chat
async function handleClearChat() {
    if (!confirm('Clear all chat messages and uploaded documents?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/clear`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Clear chat messages
            chatMessages.innerHTML = '<div class="message bot"><div class="message-content">Upload a PDF and start asking questions.</div></div>';
            
            // Reset state
            questionInput.disabled = true;
            sendBtn.disabled = true;
            questionInput.value = '';
            statusText.textContent = 'Waiting for PDF';
            statusBox.classList.remove('ready');
            queryCount = 0;
            
            // Update stats
            totalChunks.textContent = '0';
            queryCountEl.textContent = '0';
            
            showSuccess('Chat cleared successfully');
        }
    } catch (error) {
        console.error('Clear error:', error);
        showError('Failed to clear chat');
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    setTimeout(() => errorDiv.remove(), 5000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    chatMessages.appendChild(successDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    setTimeout(() => successDiv.remove(), 3000);
}
