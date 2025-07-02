document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const resetButton = document.getElementById('resetButton');
    const chatMessages = document.getElementById('chatMessages');

    const minimizeBtn = document.querySelector('.minimize-btn');
    const closeBtn = document.querySelector('.close-btn');
    const chatModal = document.querySelector('.chat-modal');

    // Function to display initial assistant messages
    function displayInitialMessages() {
        const now = new Date();
        const timeString = now.toLocaleString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });

        // First message with avatar and timestamp
        const firstMessage = document.createElement('div');
        firstMessage.className = 'message assistant-message';
        firstMessage.innerHTML = `
            <div class="message-avatar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <rect x="4" y="5" width="16" height="2" rx="1"/>
                    <rect x="4" y="11" width="16" height="2" rx="1"/>
                    <rect x="4" y="17" width="16" height="2" rx="1"/>
                </svg>
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="message-sender">Autodesk Assistant</span>
                    <span class="message-time">${timeString}</span>
                </div>
                <div class="message-text">Hi, I'm Autodesk Assistant. I can help with product selection, purchasing, and support. If needed, you can also request an agent at any time via the input bar.</div>
            </div>
        `;

        // Second message without avatar
        const secondMessage = document.createElement('div');
        secondMessage.className = 'message assistant-message no-avatar';
        secondMessage.innerHTML = `
            <div class="message-content">
                <div class="message-text">I use AI to recommend solutions. I'm still learning, so please leave feedback to help me improve my answers.</div>
            </div>
        `;

        // Third message without avatar, with Examples dropdown
        const thirdMessage = document.createElement('div');
        thirdMessage.className = 'message assistant-message no-avatar';
        thirdMessage.innerHTML = `
            <div class="message-content">
                <div class="message-text">Please describe your question in detail using complete sentences, and mention product name and version, if applicable.
                
Examples   ▼</div>
            </div>
        `;

        chatMessages.appendChild(firstMessage);
        chatMessages.appendChild(secondMessage);
        chatMessages.appendChild(thirdMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Display initial assistant messages
    displayInitialMessages();

    // Function to process input and generate assistant response
    function processInputAndRespond(text) {
        if (text.trim() === '') return;

        // Clear input
        messageInput.value = '';

        // Generate assistant response based on input
        addAssistantResponse(text);
    }



    // Function to add assistant response
    function addAssistantResponse(inputText) {
        // Clear any existing messages first
        chatMessages.innerHTML = '';
        
        // Create the response message that displays only the input text
        const responseMessage = document.createElement('div');
        responseMessage.className = 'message assistant-message';
        
        // Display only the input text, preserving formatting
        const formattedInput = inputText.trim();

        responseMessage.innerHTML = `
            <div class="message-content">
                <div class="message-text">${formattedInput}</div>
            </div>
        `;

        chatMessages.appendChild(responseMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listeners
    sendButton.addEventListener('click', function() {
        const text = messageInput.value;
        processInputAndRespond(text);
    });

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = messageInput.value;
            processInputAndRespond(text);
        }
    });

    // Reset button event listener
    resetButton.addEventListener('click', function() {
        // Clear the input text
        messageInput.value = '';
        
        // Clear chat messages and display initial messages
        chatMessages.innerHTML = '';
        displayInitialMessages();
        
        // Focus on input
        messageInput.focus();
    });

    // Chat modal controls
    minimizeBtn.addEventListener('click', function() {
        chatModal.style.transform = 'scale(0.8)';
        chatModal.style.opacity = '0.5';
        setTimeout(() => {
            chatModal.style.transform = 'scale(1)';
            chatModal.style.opacity = '1';
        }, 500);
    });

    closeBtn.addEventListener('click', function() {
        chatModal.style.transform = 'scale(0)';
        chatModal.style.opacity = '0';
        setTimeout(() => {
            chatModal.style.transform = 'scale(1)';
            chatModal.style.opacity = '1';
        }, 1000);
    });

    // Auto-focus on message input
    messageInput.focus();

    // Add some example interactions
    setTimeout(() => {
        messageInput.placeholder = "Try typing something and send it to see AI assistance!";
    }, 2000);
}); 