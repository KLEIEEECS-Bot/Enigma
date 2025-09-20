// Global variables
let currentResults = null;

// Example incident descriptions
const exampleIncidents = {
    'Phishing Email': "User received email from 'bank@security-alert.com' asking to verify account by clicking link and entering login credentials. Email had urgent language about account suspension.",
    'Phone Scam': "Elderly user received call from someone claiming to be Microsoft tech support, asking for remote computer access to fix 'urgent security issues' and requesting credit card for 'service fee'.",
    'Malware Download': "User downloaded free software from suspicious website promising computer speed optimization. Computer now running slowly with frequent popup ads and homepage changed."
};

// SVG templates for different attack types
const attackVisuals = {
    'Phishing': `
        <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2" rx="10"/>
            
            <!-- Email icon -->
            <rect x="50" y="50" width="120" height="80" fill="#fff" stroke="#e74c3c" stroke-width="3" rx="5"/>
            <polygon points="50,50 110,90 170,50" fill="#e74c3c"/>
            <text x="110" y="110" text-anchor="middle" font-size="12" fill="#e74c3c">❌ FAKE</text>
            
            <!-- Arrow -->
            <line x1="180" y1="90" x2="220" y2="90" stroke="#333" stroke-width="3"/>
            <polygon points="220,90 210,85 210,95" fill="#333"/>
            
            <!-- User icon -->
            <circle cx="280" cy="75" r="25" fill="#3498db" stroke="#2c3e50" stroke-width="2"/>
            <rect x="255" y="100" width="50" height="60" fill="#3498db" stroke="#2c3e50" stroke-width="2" rx="25"/>
            <text x="280" y="180" text-anchor="middle" font-size="14" fill="#e74c3c">DON'T CLICK!</text>
        </svg>
    `,
    'Malware': `
        <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2" rx="10"/>
            
            <!-- Computer -->
            <rect x="150" y="60" width="100" height="70" fill="#ecf0f1" stroke="#34495e" stroke-width="2" rx="5"/>
            <rect x="155" y="65" width="90" height="50" fill="#2c3e50"/>
            
            <!-- Virus symbols -->
            <circle cx="130" cy="40" r="15" fill="#e74c3c"/>
            <text x="130" y="45" text-anchor="middle" font-size="12" fill="white">💀</text>
            
            <circle cx="270" cy="40" r="15" fill="#e74c3c"/>
            <text x="270" y="45" text-anchor="middle" font-size="12" fill="white">🦠</text>
            
            <circle cx="130" cy="160" r="15" fill="#e74c3c"/>
            <text x="130" y="165" text-anchor="middle" font-size="12" fill="white">⚠️</text>
            
            <!-- Warning text -->
            <text x="200" y="180" text-anchor="middle" font-size="16" fill="#e74c3c" font-weight="bold">INFECTED!</text>
        </svg>
    `,
    'Social Engineering': `
        <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2" rx="10"/>
            
            <!-- Phone -->
            <rect x="50" y="60" width="60" height="100" fill="#34495e" stroke="#2c3e50" stroke-width="2" rx="10"/>
            <circle cx="80" cy="80" r="8" fill="#e74c3c"/>
            <text x="80" y="130" font-size="10" fill="white" text-anchor="middle">📞</text>
            
            <!-- Speech bubble -->
            <ellipse cx="200" cy="80" rx="80" ry="40" fill="#fff" stroke="#e74c3c" stroke-width="2"/>
            <text x="200" y="75" text-anchor="middle" font-size="12" fill="#e74c3c">I'm from</text>
            <text x="200" y="90" text-anchor="middle" font-size="12" fill="#e74c3c">Tech Support!</text>
            
            <!-- User -->
            <circle cx="320" cy="75" r="25" fill="#3498db" stroke="#2c3e50" stroke-width="2"/>
            <rect x="295" y="100" width="50" height="60" fill="#3498db" stroke="#2c3e50" stroke-width="2" rx="25"/>
            <text x="320" y="180" text-anchor="middle" font-size="14" fill="#e74c3c">HANG UP!</text>
        </svg>
    `,
    'Identity Theft': `
        <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2" rx="10"/>
            
            <!-- ID Card -->
            <rect x="100" y="60" width="80" height="50" fill="#fff" stroke="#34495e" stroke-width="2" rx="5"/>
            <rect x="105" y="65" width="25" height="20" fill="#3498db"/>
            <line x1="135" y1="70" x2="170" y2="70" stroke="#333" stroke-width="2"/>
            <line x1="135" y1="80" x2="160" y2="80" stroke="#333" stroke-width="2"/>
            <line x1="105" y1="95" x2="170" y2="95" stroke="#333" stroke-width="2"/>
            
            <!-- Thief -->
            <circle cx="250" cy="75" r="25" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>
            <rect x="225" y="100" width="50" height="60" fill="#e74c3c" stroke="#c0392b" stroke-width="2" rx="25"/>
            <text x="250" y="45" text-anchor="middle" font-size="16">😈</text>
            
            <!-- Arrow -->
            <line x1="190" y1="85" x2="215" y2="85" stroke="#e74c3c" stroke-width="3"/>
            <polygon points="215,85 205,80 205,90" fill="#e74c3c"/>
            
            <text x="200" y="180" text-anchor="middle" font-size="14" fill="#e74c3c" font-weight="bold">STOLEN INFO!</text>
        </svg>
    `,
    'Unknown': `
        <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2" rx="10"/>
            
            <!-- Question mark -->
            <circle cx="200" cy="100" r="60" fill="#f39c12" stroke="#e67e22" stroke-width="3"/>
            <text x="200" y="120" text-anchor="middle" font-size="60" fill="white" font-weight="bold">?</text>
            
            <text x="200" y="180" text-anchor="middle" font-size="16" fill="#e67e22" font-weight="bold">UNKNOWN THREAT</text>
        </svg>
    `
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    const form = document.getElementById('attackForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    // Check if we're on the results page and have results in URL
    if (window.location.pathname === '/result') {
        const urlParams = new URLSearchParams(window.location.search);
        const resultsData = urlParams.get('data');
        if (resultsData) {
            try {
                const results = JSON.parse(decodeURIComponent(resultsData));
                displayResults(results);
            } catch (e) {
                console.error('Error parsing results data:', e);
            }
        }
    }
    
    // Initialize audio buttons if on results page
    initializeAudioButtons();
}

function fillExample(cardElement) {
    const title = cardElement.querySelector('h4').textContent;
    const description = exampleIncidents[title];
    const textarea = document.getElementById('description');
    
    if (textarea && description) {
        textarea.value = description;
        textarea.focus();
        
        // Add visual feedback
        cardElement.style.background = '#d4edda';
        setTimeout(() => {
            cardElement.style.background = '#f8f9fa';
        }, 1000);
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const description = document.getElementById('description').value.trim();
    const loadingDiv = document.getElementById('loading');
    const submitBtn = event.target.querySelector('button[type="submit"]');
    
    if (!description) {
        alert('Please enter an incident description.');
        return;
    }
    
    // Show loading state
    loadingDiv.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = '🔄 Analyzing...';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description: description })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const results = await response.json();
        
        // Navigate to results page with data
        const resultsUrl = `/result?data=${encodeURIComponent(JSON.stringify(results))}`;
        window.location.href = resultsUrl;
        
    } catch (error) {
        console.error('Error analyzing attack:', error);
        alert('Sorry, there was an error analyzing the incident. Please try again.');
        
        // Reset form state
        loadingDiv.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.textContent = '🔍 Analyze Attack';
    }
}

function displayResults(results) {
    currentResults = results;
    const resultsContainer = document.getElementById('results');
    const template = document.getElementById('resultTemplate');
    
    if (!resultsContainer || !template) {
        console.error('Results container or template not found');
        return;
    }
    
    // Clone the template
    const resultElement = template.content.cloneNode(true);
    
    // Populate attack type
    const attackNameElement = resultElement.querySelector('.attack-name');
    if (attackNameElement) {
        attackNameElement.textContent = results.attack_type;
    }
    
    // Populate visual
    const visualDiv = resultElement.querySelector('.attack-visual');
    if (visualDiv) {
        const attackType = results.attack_type.replace(' ', '');
        const svg = attackVisuals[attackType] || attackVisuals['Unknown'];
        visualDiv.innerHTML = svg;
    }
    
    // Populate story
    const storyElement = resultElement.querySelector('.story-text');
    if (storyElement) {
        storyElement.textContent = results.story;
    }
    
    // Populate actions checklist
    const actionsDiv = resultElement.querySelector('.actions-checklist');
    if (actionsDiv && results.actions) {
        results.actions.forEach((action, index) => {
            const actionItem = document.createElement('div');
            actionItem.className = 'action-item';
            
            const actionNumber = document.createElement('div');
            actionNumber.className = 'action-number';
            actionNumber.textContent = index + 1;
            
            const actionText = document.createElement('div');
            actionText.textContent = action;
            
            actionItem.appendChild(actionNumber);
            actionItem.appendChild(actionText);
            actionsDiv.appendChild(actionItem);
        });
    }
    
    // Populate timestamp
    const timeElement = resultElement.querySelector('.time');
    if (timeElement) {
        timeElement.textContent = results.timestamp;
    }
    
    // Clear and append results
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(resultElement);
}

function initializeAudioButtons() {
    const speakStoryBtn = document.getElementById('speakStory');
    const speakActionsBtn = document.getElementById('speakActions');
    const printBtn = document.getElementById('printResults');
    
    if (speakStoryBtn) {
        speakStoryBtn.addEventListener('click', speakStory);
    }
    
    if (speakActionsBtn) {
        speakActionsBtn.addEventListener('click', speakActions);
    }
    
    if (printBtn) {
        printBtn.addEventListener('click', printResults);
    }
}

function speakStory() {
    if (!currentResults || !currentResults.story) {
        alert('No story to read aloud.');
        return;
    }
    
    if ('speechSynthesis' in window) {
        // Stop any ongoing speech
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(currentResults.story);
        utterance.rate = 0.8; // Slower rate for elderly users
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Update button state
        const btn = document.getElementById('speakStory');
        btn.textContent = '🔊 Reading...';
        btn.disabled = true;
        
        utterance.onend = function() {
            btn.textContent = '🔊 Read Story Aloud';
            btn.disabled = false;
        };
        
        utterance.onerror = function(event) {
            console.error('Speech synthesis error:', event.error);
            btn.textContent = '🔊 Read Story Aloud';
            btn.disabled = false;
            alert('Sorry, text-to-speech is not working properly.');
        };
        
        speechSynthesis.speak(utterance);
    } else {
        alert('Sorry, your browser does not support text-to-speech.');
    }
}

function speakActions() {
    if (!currentResults || !currentResults.actions) {
        alert('No actions to read aloud.');
        return;
    }
    
    if ('speechSynthesis' in window) {
        // Stop any ongoing speech
        speechSynthesis.cancel();
        
        const actionsText = "Here's what you should do: " + currentResults.actions.join('. Next, ') + '.';
        const utterance = new SpeechSynthesisUtterance(actionsText);
        utterance.rate = 0.8; // Slower rate for elderly users
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Update button state
        const btn = document.getElementById('speakActions');
        btn.textContent = '🔊 Reading...';
        btn.disabled = true;
        
        utterance.onend = function() {
            btn.textContent = '🔊 Read Actions Aloud';
            btn.disabled = false;
        };
        
        utterance.onerror = function(event) {
            console.error('Speech synthesis error:', event.error);
            btn.textContent = '🔊 Read Actions Aloud';
            btn.disabled = false;
            alert('Sorry, text-to-speech is not working properly.');
        };
        
        speechSynthesis.speak(utterance);
    } else {
        alert('Sorry, your browser does not support text-to-speech.');
    }
}

function printResults() {
    window.print();
}

// Stop any ongoing speech when leaving the page
window.addEventListener('beforeunload', function() {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
    }
});