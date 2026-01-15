// ---------- VARIABLES ----------
let isTyping = false;
let currentChatId = null;
const CHATS_STORAGE_KEY = 'super_ai_chats';
const CURRENT_CHAT_KEY = 'super_ai_current_chat';

// ---------- INITIALIZE ----------
function initializeChat() {
    loadChats();
    const input = document.getElementById("msg");
    input.focus();
    
    // Load current chat or start new one
    const savedCurrentChat = localStorage.getItem(CURRENT_CHAT_KEY);
    if (savedCurrentChat) {
        loadChat(savedCurrentChat);
    } else {
        startNewChat();
    }
}

// ---------- CHAT MANAGEMENT ----------
function startNewChat() {
    currentChatId = 'chat_' + Date.now();
    
    // Clear chat box except initial welcome
    const box = document.getElementById("chat-box");
    while (box.children.length > 1) {
        box.removeChild(box.lastChild);
    }
    
    // Add welcome message
    setTimeout(() => {
        appendMessage("💡 **Tip**: You can ask me to help with writing, coding, explanations, or even creative tasks!", "bot", true);
    }, 1000);
    
    // Save empty chat
    saveCurrentChat();
    updateSidebar();
    localStorage.setItem(CURRENT_CHAT_KEY, currentChatId);
}

function saveCurrentChat() {
    const box = document.getElementById("chat-box");
    const messages = [];
    
    // Get all messages except initial welcome
    for (let i = 1; i < box.children.length; i++) {
        const container = box.children[i];
        const sender = container.classList.contains('user-container') ? 'user' : 'bot';
        const messageBubble = container.querySelector('.message-bubble');
        
        if (messageBubble) {
            let originalText = messageBubble.getAttribute('data-original-text') || 
                             messageBubble.textContent || 
                             messageBubble.innerText;
            
            messages.push({
                sender: sender,
                text: originalText,
                isMarkdown: sender === 'bot',
                timestamp: Date.now() - (box.children.length - i) * 1000
            });
        }
    }
    
    // Get chat title from first user message
    let chatTitle = "New Chat";
    if (messages.length > 0) {
        const firstUserMsg = messages.find(m => m.sender === 'user');
        if (firstUserMsg) {
            chatTitle = firstUserMsg.text.substring(0, 30) + (firstUserMsg.text.length > 30 ? '...' : '');
        }
    }
    
    // Save chat
    const chats = getChats();
    chats[currentChatId] = {
        id: currentChatId,
        title: chatTitle,
        messages: messages,
        createdAt: Date.now(),
        updatedAt: Date.now()
    };
    
    localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
}

function loadChat(chatId) {
    const chats = getChats();
    const chat = chats[chatId];
    
    if (!chat) {
        startNewChat();
        return;
    }
    
    currentChatId = chatId;
    
    // Clear chat box
    const box = document.getElementById("chat-box");
    while (box.children.length > 1) {
        box.removeChild(box.lastChild);
    }
    
    // Load messages
    chat.messages.forEach(msg => {
        appendMessage(msg.text, msg.sender, msg.isMarkdown, msg.text);
    });
    
    // Update sidebar
    updateSidebar();
    localStorage.setItem(CURRENT_CHAT_KEY, chatId);
}

function getChats() {
    const chatsJson = localStorage.getItem(CHATS_STORAGE_KEY);
    return chatsJson ? JSON.parse(chatsJson) : {};
}

function loadChats() {
    const chats = getChats();
    const container = document.getElementById("conversation-list");
    
    if (Object.keys(chats).length === 0) {
        container.innerHTML = `
            <div class="empty-history">
                <i class="fas fa-comments"></i>
                <p>No chat history yet</p>
            </div>
        `;
        return;
    }
    
    // Sort chats by updated time (newest first)
    const sortedChats = Object.values(chats).sort((a, b) => b.updatedAt - a.updatedAt);
    
    let html = '';
    sortedChats.forEach(chat => {
        const date = new Date(chat.updatedAt);
        const dateStr = date.toLocaleDateString();
        const timeStr = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        html += `
            <div class="conversation-item ${chat.id === currentChatId ? 'active' : ''}" 
                 onclick="loadChat('${chat.id}')">
                <div class="conversation-icon">
                    <i class="fas fa-message"></i>
                </div>
                <div class="conversation-content">
                    <div class="conversation-title">${escapeHtml(chat.title)}</div>
                    <div class="conversation-meta">
                        <span class="conversation-date">${dateStr}</span>
                        <span>${timeStr}</span>
                    </div>
                </div>
                <div class="conversation-actions">
                    <button class="conv-action-btn" onclick="renameChat('${chat.id}'); event.stopPropagation()" 
                            title="Rename">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="conv-action-btn" onclick="deleteChat('${chat.id}'); event.stopPropagation()" 
                            title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function updateSidebar() {
    const chats = getChats();
    const container = document.getElementById("conversation-list");
    
    if (Object.keys(chats).length === 0) {
        container.innerHTML = `
            <div class="empty-history">
                <i class="fas fa-comments"></i>
                <p>No chat history yet</p>
            </div>
        `;
        return;
    }
    
    loadChats();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function searchConversations() {
    const searchTerm = document.getElementById('history-search').value.toLowerCase();
    const items = document.querySelectorAll('.conversation-item');
    
    items.forEach(item => {
        const title = item.querySelector('.conversation-title').textContent.toLowerCase();
        if (title.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

function renameCurrentChat() {
    const chats = getChats();
    const chat = chats[currentChatId];
    
    if (!chat) return;
    
    const newTitle = prompt("Enter new chat title:", chat.title);
    if (newTitle && newTitle.trim()) {
        chat.title = newTitle.trim();
        chat.updatedAt = Date.now();
        localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
        updateSidebar();
    }
}

function renameChat(chatId) {
    const chats = getChats();
    const chat = chats[chatId];
    
    if (!chat) return;
    
    const newTitle = prompt("Enter new chat title:", chat.title);
    if (newTitle && newTitle.trim()) {
        chat.title = newTitle.trim();
        chat.updatedAt = Date.now();
        localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
        updateSidebar();
    }
}

function deleteCurrentChat() {
    if (confirm("Delete this chat? This action cannot be undone.")) {
        deleteChat(currentChatId);
    }
}

function deleteChat(chatId) {
    const chats = getChats();
    delete chats[chatId];
    
    localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
    
    if (currentChatId === chatId) {
        startNewChat();
    }
    
    updateSidebar();
}

function clearAllHistory() {
    if (confirm("Clear ALL chat history? This action cannot be undone.")) {
        localStorage.removeItem(CHATS_STORAGE_KEY);
        localStorage.removeItem(CURRENT_CHAT_KEY);
        startNewChat();
        updateSidebar();
    }
}

function exportAllChats() {
    const chats = getChats();
    if (Object.keys(chats).length === 0) {
        alert("No chats to export.");
        return;
    }
    
    const blob = new Blob([JSON.stringify(chats, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `super-ai-chats-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ---------- CHAT FUNCTIONS ----------
async function sendMessage() {
    const input = document.getElementById("msg");
    const msg = input.value.trim();
    
    if (!msg || isTyping) return;

    // Disable input
    input.value = "";
    input.disabled = true;
    isTyping = true;

    // Show user message
    appendMessage(msg, "user", false, msg);
    saveCurrentChat();
    
    // Show typing
    const typingIndicator = document.getElementById("typing-indicator");
    typingIndicator.style.display = "flex";
    
    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();
        
        // Hide typing and show response
        typingIndicator.style.display = "none";
        appendMessage(data.reply, "bot", true, data.reply);
        saveCurrentChat();
        
    } catch (err) {
        typingIndicator.style.display = "none";
        appendMessage("⚠️ Sorry, I encountered an error. Please try again.", "bot", true);
        saveCurrentChat();
        console.error("Chat Error:", err);
    } finally {
        // Re-enable input
        input.disabled = false;
        input.focus();
        isTyping = false;
    }
}

function quickAsk(text) {
    const input = document.getElementById("msg");
    input.value = text;
    sendMessage();
}

// ---------- APPEND MESSAGE WITH ENHANCED MARKDOWN ----------
function appendMessage(text, sender, markdown = false, originalText = null) {
    const box = document.getElementById("chat-box");

    const container = document.createElement("div");
    container.className = `message-container ${sender}-container`;

    // Avatar
    const avatar = document.createElement("div");
    avatar.className = `avatar ${sender}-avatar`;

    if (sender === "user") {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
    } else {
        const img = document.createElement("img");
        img.src = "/static/images/Super AIP.jpg";
        img.alt = "Super AI";
        img.className = "avatar-img";
        avatar.appendChild(img);
    }

    // Message bubble
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${sender}-message`;

    // Store original text (important for Edit)
    bubble.setAttribute(
        "data-original-text",
        originalText || text
    );

    // ---------- CONTENT ----------
    if (markdown) {
        bubble.innerHTML = marked.parse(text);
        setTimeout(() => {
            bubble.querySelectorAll("pre code").forEach(block => {
                if (typeof hljs !== "undefined") {
                    hljs.highlightElement(block);
                }
            });
            addCopyButtons(); // bot code copy
        }, 50);
    } else {
        bubble.textContent = text;
    }

    // ---------- USER MESSAGE ACTIONS (EDIT + COPY) ----------
    if (sender === "user") {
        const actions = document.createElement("div");
        actions.className = "user-msg-actions";

        // Copy button
        const copyBtn = document.createElement("button");
        copyBtn.innerHTML = `<i class="far fa-copy"></i>`;
        copyBtn.title = "Copy";

        copyBtn.onclick = () => {
            navigator.clipboard.writeText(
                bubble.getAttribute("data-original-text")
            );
            copyBtn.innerHTML = `<i class="fas fa-check"></i>`;
            setTimeout(() => {
                copyBtn.innerHTML = `<i class="far fa-copy"></i>`;
            }, 1000);
        };

        // Edit button
        const editBtn = document.createElement("button");
        editBtn.innerHTML = `<i class="fas fa-edit"></i>`;
        editBtn.title = "Edit";

        editBtn.onclick = () => {
            const input = document.getElementById("msg");
            input.value = bubble.getAttribute("data-original-text");
            input.focus();
        };

        actions.appendChild(copyBtn);
        actions.appendChild(editBtn);
        bubble.appendChild(actions);
    }

    // ---------- ASSEMBLE ----------
    if (sender === "user") {
        container.appendChild(bubble);
        container.appendChild(avatar);
    } else {
        container.appendChild(avatar);
        container.appendChild(bubble);
    }

    box.appendChild(container);
    box.scrollTop = box.scrollHeight;
}


// ---------- EVENT LISTENERS ----------
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    
    // Auto-hide sidebar on mobile when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 1024) {
            const sidebar = document.getElementById("sidebar");
            const sidebarToggle = document.querySelector('.sidebar-toggle');
            
            if (sidebar.classList.contains('active') && 
                !sidebar.contains(e.target) && 
                !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('active');
                sidebarToggle.style.display = 'flex';
            }
        }
    });
});

// Input enhancements
document.getElementById("msg").addEventListener("input", function(e) {
    const sendBtn = document.getElementById("sendBtn");
    if (e.target.value.trim()) {
        sendBtn.style.background = "linear-gradient(135deg, #667eea, #764ba2)";
    } else {
        sendBtn.style.background = "";
    }
});

function addCopyButtons() {
    document.querySelectorAll('.bot-message pre').forEach((pre) => {

        // Prevent duplicate
        if (pre.parentElement.classList.contains('code-wrapper')) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'code-wrapper';

        const header = document.createElement('div');
        header.className = 'code-header';

        const label = document.createElement('span');
        label.className = 'code-label';
        label.innerText = 'Code';

        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.innerHTML = `
            <i class="far fa-copy"></i>
            <span>Copy code</span>
        `;

        button.addEventListener('click', () => {
            navigator.clipboard.writeText(pre.innerText);

            button.classList.add('copied');
            button.innerHTML = `
                <i class="fas fa-check"></i>
                <span>Copied!</span>
            `;

            setTimeout(() => {
                button.classList.remove('copied');
                button.innerHTML = `
                    <i class="far fa-copy"></i>
                    <span>Copy code</span>
                `;
            }, 1500);
        });

        header.appendChild(label);
        header.appendChild(button);

        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(header);
        wrapper.appendChild(pre);
    });
}

function toggleSidebarDesktop() {
    const sidebar = document.getElementById("sidebar");

    if (window.innerWidth <= 1024) {
        sidebar.classList.toggle("active");   // mobile
    } else {
        sidebar.classList.toggle("collapsed"); // desktop
    }
}