/**
 * Nanobot Dashboard - Complete Interactive Script
 * Features: Gateway monitoring, bookmarks, tasks, schedule, chat, topology
 */

class DashboardApp {
    constructor() {
        this.activeTab = 'gateway';
        this.bookmarks = [];
        this.tasks = [];
        this.schedule = [];
        this.chatHistory = [];
        this.topologyData = {};
        this.apiBase = '/dashboard/api';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.updateClock();
        setInterval(() => this.updateClock(), 1000);
        this.logActivity('Dashboard initialized');
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const tabId = btn.dataset.tab;
                this.switchTab(tabId);
            });
        });

        // Initialize each tab
        this.setupBookmarks();
        this.setupTasks();
        this.setupSchedule();
        this.setupChat();
        this.setupTopology();
    }

    switchTab(tabId) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

        // Show/hide tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabId}-tab`).classList.add('active');

        this.activeTab = tabId;

        // Load tab-specific data
        if (tabId === 'bookmarks') {
            this.loadBookmarks();
        } else if (tabId === 'tasks') {
            this.loadTasks();
        } else if (tabId === 'schedule') {
            this.loadSchedule();
        } else if (tabId === 'topology') {
            this.loadTopology();
        }
    }

    loadInitialData() {
        this.loadBookmarks();
        this.loadTasks();
        this.loadSchedule();
        this.loadChatHistory();
    }

    updateClock() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: true });
        const dateStr = now.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });

        const clockTime = document.getElementById('clock-time');
        const clockDate = document.getElementById('clock-date');
        const footerTime = document.getElementById('footer-time');

        if (clockTime) clockTime.textContent = timeStr;
        if (clockDate) clockDate.textContent = dateStr;
        if (footerTime) footerTime.textContent = dateStr + ' ' + timeStr;
    }

    async apiRequest(endpoint, options = {}) {
        try {
            const url = `${this.apiBase}${endpoint}`;
            const response = await fetch(url, options);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            this.logActivity(`API Error: ${error.message}`, 'error');
            throw error;
        }
    }

    logActivity(message, type = 'info') {
        const log = document.getElementById('activity-log');
        if (!log) return;

        const entry = document.createElement('div');
        entry.className = `log-entry log-${type}`;
        entry.innerHTML = `
            <span class="log-time">${new Date().toLocaleTimeString()}</span>
            <span class="log-badge ${type}">${type.toUpperCase()}</span>
            <span class="log-message">${message}</span>
        `;

        log.insertBefore(entry, log.firstChild);

        // Keep only last 20 entries
        while (log.children.length > 20) {
            log.removeChild(log.lastChild);
        }
    }

    // Bookmark functions
    setupBookmarks() {
        const addBtn = document.getElementById('add-bookmark-btn');
        const modal = document.getElementById('bookmark-modal');
        const closeBtn = modal?.querySelector('.close-modal');
        const saveBtn = document.getElementById('save-bm-btn');

        if (addBtn) {
            addBtn.addEventListener('click', () => {
                modal.style.display = 'flex';
                document.getElementById('bm-title').value = '';
                document.getElementById('bm-url').value = '';
                document.getElementById('bm-tags').value = '';
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => modal.style.display = 'none');
        }

        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveBookmark());
        }

        // Search functionality
        const searchInput = document.getElementById('bookmark-search');
        if (searchInput) {
            searchInput.addEventListener('input', () => this.filterBookmarks());
        }

        // Folder navigation
        document.querySelectorAll('.folder-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.folder-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.filterBookmarks();
            });
        });
    }

    async loadBookmarks() {
        try {
            this.bookmarks = await this.apiRequest('/bookmarks');
            this.renderBookmarks();
        } catch (error) {
            console.error('Failed to load bookmarks:', error);
        }
    }

    renderBookmarks() {
        const grid = document.getElementById('bookmarks-grid');
        if (!grid) return;

        grid.innerHTML = '';

        this.bookmarks.forEach(bookmark => {
            const card = document.createElement('div');
            card.className = 'bookmark-card';
            card.innerHTML = `
                <div class="bookmark-header">
                    <h4>${bookmark.title}</h4>
                    <div class="bookmark-actions">
                        <button class="btn-icon" onclick="dashboard.editBookmark(${bookmark.id})" title="Edit">✏️</button>
                        <button class="btn-icon" onclick="dashboard.deleteBookmark(${bookmark.id})" title="Delete">🗑️</button>
                    </div>
                </div>
                <a href="${bookmark.url}" target="_blank" class="bookmark-url">${bookmark.url}</a>
                <div class="bookmark-meta">
                    <span class="bookmark-folder">${bookmark.folder}</span>
                    ${bookmark.tags ? `<span class="bookmark-tags">${bookmark.tags}</span>` : ''}
                </div>
            `;
            grid.appendChild(card);
        });

        if (this.bookmarks.length === 0) {
            grid.innerHTML = '<div class="empty-state">No bookmarks yet. Add your first bookmark!</div>';
        }
    }

    async saveBookmark() {
        const bookmark = {
            title: document.getElementById('bm-title').value,
            url: document.getElementById('bm-url').value,
            folder: document.getElementById('bm-folder').value,
            tags: document.getElementById('bm-tags').value
        };

        if (!bookmark.title || !bookmark.url) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            await this.apiRequest('/bookmarks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bookmark)
            });

            document.getElementById('bookmark-modal').style.display = 'none';
            this.loadBookmarks();
            this.logActivity(`Bookmark added: ${bookmark.title}`, 'success');
        } catch (error) {
            alert('Failed to save bookmark');
        }
    }

    async editBookmark(id) {
        const bookmark = this.bookmarks.find(b => b.id === id);
        if (!bookmark) return;

        document.getElementById('bm-title').value = bookmark.title;
        document.getElementById('bm-url').value = bookmark.url;
        document.getElementById('bm-folder').value = bookmark.folder;
        document.getElementById('bm-tags').value = bookmark.tags || '';
        document.getElementById('bookmark-modal').style.display = 'flex';

        // Change save handler to update
        const saveBtn = document.getElementById('save-bm-btn');
        saveBtn.onclick = async () => {
            const updated = {
                title: document.getElementById('bm-title').value,
                url: document.getElementById('bm-url').value,
                folder: document.getElementById('bm-folder').value,
                tags: document.getElementById('bm-tags').value
            };

            try {
                await this.apiRequest(`/bookmarks/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updated)
                });

                document.getElementById('bookmark-modal').style.display = 'none';
                this.loadBookmarks();
                this.logActivity('Bookmark updated', 'success');
            } catch (error) {
                alert('Failed to update bookmark');
            }
        };
    }

    async deleteBookmark(id) {
        if (!confirm('Delete this bookmark?')) return;

        try {
            await this.apiRequest(`/bookmarks/${id}`, { method: 'DELETE' });
            this.loadBookmarks();
            this.logActivity('Bookmark deleted', 'success');
        } catch (error) {
            alert('Failed to delete bookmark');
        }
    }

    filterBookmarks() {
        const search = document.getElementById('bookmark-search').value.toLowerCase();
        const activeFolder = document.querySelector('.folder-btn.active')?.dataset.folder || 'all';

        const filtered = this.bookmarks.filter(b => {
            const matchesSearch = !search || 
                b.title.toLowerCase().includes(search) ||
                b.url.toLowerCase().includes(search) ||
                (b.tags && b.tags.toLowerCase().includes(search));

            const matchesFolder = activeFolder === 'all' || b.folder === activeFolder;

            return matchesSearch && matchesFolder;
        });

        this.renderFilteredBookmarks(filtered);
    }

    renderFilteredBookmarks(bookmarks) {
        const grid = document.getElementById('bookmarks-grid');
        if (!grid) return;

        grid.innerHTML = '';
        bookmarks.forEach(bookmark => {
            const card = document.createElement('div');
            card.className = 'bookmark-card';
            card.innerHTML = `
                <div class="bookmark-header">
                    <h4>${bookmark.title}</h4>
                    <div class="bookmark-actions">
                        <button class="btn-icon" onclick="dashboard.editBookmark(${bookmark.id})" title="Edit">✏️</button>
                        <button class="btn-icon" onclick="dashboard.deleteBookmark(${bookmark.id})" title="Delete">🗑️</button>
                    </div>
                </div>
                <a href="${bookmark.url}" target="_blank" class="bookmark-url">${bookmark.url}</a>
                <div class="bookmark-meta">
                    <span class="bookmark-folder">${bookmark.folder}</span>
                    ${bookmark.tags ? `<span class="bookmark-tags">${bookmark.tags}</span>` : ''}
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // Task functions
    setupTasks() {
        // Tasks will be populated by backend
    }

    async loadTasks() {
        try {
            this.tasks = await this.apiRequest('/tasks');
            this.renderTasks();
        } catch (error) {
            console.error('Failed to load tasks:', error);
        }
    }

    renderTasks() {
        const container = document.getElementById('tasks-list');
        if (!container) return;

        container.innerHTML = '';

        if (this.tasks.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">⚡</div>
                    <p>No active tasks</p>
                    <p class="empty-sub">Running tasks will appear here automatically</p>
                </div>
            `;
            return;
        }

        this.tasks.forEach(task => {
            const item = document.createElement('div');
            item.className = 'task-item';
            item.innerHTML = `
                <div class="task-name">${task.name}</div>
                <div class="task-status status-${task.status}">${task.status}</div>
                <div class="task-time">${new Date(task.created).toLocaleString()}</div>
            `;
            container.appendChild(item);
        });
    }

    // Schedule functions
    setupSchedule() {
        const addBtn = document.getElementById('add-reminder-btn');
        const modal = document.getElementById('reminder-modal');
        const closeBtn = modal?.querySelector('.close-modal');
        const saveBtn = document.getElementById('save-rem-btn');

        if (addBtn) {
            addBtn.addEventListener('click', () => {
                modal.style.display = 'flex';
                document.getElementById('rem-date').value = new Date().toISOString().slice(0, 16);
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => modal.style.display = 'none');
        }

        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveReminder());
        }
    }

    async loadSchedule() {
        try {
            this.schedule = await this.apiRequest('/schedule');
            this.renderSchedule();
        } catch (error) {
            console.error('Failed to load schedule:', error);
        }
    }

    renderSchedule() {
        const container = document.getElementById('reminders-list');
        if (!container) return;

        container.innerHTML = '';

        const sortedReminders = this.schedule.sort((a, b) => 
            new Date(a.date) - new Date(b.date)
        ).slice(0, 10); // Show next 10

        sortedReminders.forEach(reminder => {
            const item = document.createElement('div');
            item.className = 'reminder-item';
            item.innerHTML = `
                <div class="reminder-title">${reminder.title}</div>
                <div class="reminder-datetime">${new Date(reminder.date).toLocaleString()}</div>
                <span class="reminder-type">${reminder.type}</span>
            `;
            container.appendChild(item);
        });
    }

    async saveReminder() {
        const reminder = {
            title: document.getElementById('rem-title').value,
            date: document.getElementById('rem-date').value,
            type: document.getElementById('rem-type').value
        };

        if (!reminder.title || !reminder.date) {
            alert('Please fill in all required fields');
            return;
        }

        reminder.id = Date.now().toString();

        try {
            this.schedule.push(reminder);
            await this.apiRequest('/schedule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reminder)
            });

            document.getElementById('reminder-modal').style.display = 'none';
            this.loadSchedule();
            this.logActivity('Reminder added', 'success');
        } catch (error) {
            alert('Failed to save reminder');
        }
    }

    // Chat functions
    setupChat() {
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const fileInput = document.getElementById('file-upload');

        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.handleFileUpload(file);
                }
            });
        }

        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendChatMessage());
        }

        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendChatMessage();
                }
            });
        }
    }

    async loadChatHistory() {
        try {
            this.chatHistory = await this.apiRequest('/chat');
            this.renderChat();
        } catch (error) {
            console.error('Failed to load chat:', error);
        }
    }

    renderChat() {
        const container = document.getElementById('chat-messages');
        if (!container) return;

        // Don't clear the welcome message, just add to it
        const existingMessages = container.querySelectorAll('.message');
        existingMessages.forEach(m => m.remove());

        this.chatHistory.forEach(msg => {
            const msgEl = document.createElement('div');
            msgEl.className = `message ${msg.role}`;
            msgEl.innerHTML = `
                <div class="message-avatar">${msg.role === 'user' ? '👤' : '🐱'}</div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p>${msg.message}</p>
                    </div>
                    <span class="message-time">${new Date(msg.timestamp).toLocaleTimeString()}</span>
                </div>
            `;
            container.appendChild(msgEl);
        });

        // Scroll to bottom
        container.scrollTop = container.scrollHeight;
    }

    async sendChatMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Add user message
        const userMsg = {
            role: 'user',
            message: message,
            timestamp: new Date().toISOString()
        };

        this.chatHistory.push(userMsg);
        this.renderChat();

        // Clear input
        input.value = '';

        try {
            await this.apiRequest('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userMsg)
            });

            // Simulate bot response (in real implementation, this would come from backend)
            setTimeout(() => {
                const botMsg = {
                    role: 'assistant',
                    message: 'Message received. Processing...',
                    timestamp: new Date().toISOString()
                };
                this.chatHistory.push(botMsg);
                this.renderChat();
            }, 1000);

            this.logActivity('Chat message sent', 'success');
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    }

    handleFileUpload(file) {
        const preview = document.getElementById('file-preview');
        if (preview) {
            preview.innerHTML = `
                <div class="file-item">
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">${(file.size / 1024).toFixed(1)} KB</span>
                    <button class="btn-icon" onclick="this.parentElement.remove()">✕</button>
                </div>
            `;
            preview.style.display = 'block';
        }
        this.logActivity(`File uploaded: ${file.name}`, 'success');
    }

    // Topology functions
    setupTopology() {
        const refreshBtn = document.getElementById('refresh-topology-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadTopology());
        }
    }

    async loadTopology() {
        try {
            this.topologyData = await this.apiRequest('/topology');
            this.renderTopology();
            this.updateTopologyStats();
        } catch (error) {
            console.error('Failed to load topology:', error);
        }
    }

    renderTopology() {
        const svg = document.getElementById('topology-svg');
        if (!svg) return;

        // Clear existing content
        svg.innerHTML = '';

        const width = svg.clientWidth || 800;
        const height = 600;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = 180;

        // Define node types and colors
        const nodeTypes = {
            skills: { color: '#4facfe', positions: [] },
            channels: { color: '#00f2fe', positions: [] },
            providers: { color: '#a855f7', positions: [] },
            tools: { color: '#f59e0b', positions: [] }
        };

        // Create connections
        const connections = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        connections.className = 'topology-connections';

        // Draw central node (Nanobot)
        const centralNode = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        centralNode.setAttribute('cx', centerX);
        centralNode.setAttribute('cy', centerY);
        centralNode.setAttribute('r', 50);
        centralNode.setAttribute('fill', 'rgba(255,255,255,0.1)');
        centralNode.setAttribute('stroke', 'rgba(255,255,255,0.3)');
        centralNode.setAttribute('stroke-width', '2');

        const centralText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        centralText.setAttribute('x', centerX);
        centralText.setAttribute('y', centerY);
        centralText.setAttribute('text-anchor', 'middle');
        centralText.setAttribute('dominant-baseline', 'middle');
        centralText.setAttribute('fill', 'white');
        centralText.setAttribute('font-size', '14');
        centralText.setAttribute('font-weight', 'bold');
        centralText.textContent = 'Nanobot';

        svg.appendChild(centralNode);
        svg.appendChild(centralText);

        // Calculate positions for each category
        let angleOffset = 0;
        Object.keys(nodeTypes).forEach((type, typeIndex) => {
            const nodes = this.topologyData[type] || [];
            const count = nodes.length;
            
            if (count > 0) {
                const angleStep = 90 / Math.max(count, 1);
                const baseAngle = typeIndex * 90 + angleOffset;

                nodes.forEach((node, index) => {
                    const angle = (baseAngle + index * angleStep) * Math.PI / 180;
                    const nodeX = centerX + Math.cos(angle) * radius;
                    const nodeY = centerY + Math.sin(angle) * radius;

                    // Store position for connection
                    nodeTypes[type].positions.push({ x: nodeX, y: nodeY, name: node.name });

                    // Draw line to central node
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', centerX);
                    line.setAttribute('y1', centerY);
                    line.setAttribute('x2', nodeX);
                    line.setAttribute('y2', nodeY);
                    line.setAttribute('stroke', 'rgba(255,255,255,0.2)');
                    line.setAttribute('stroke-width', '1');
                    connections.appendChild(line);
                });
            }
        });

        svg.appendChild(connections);

        // Draw nodes
        Object.keys(nodeTypes).forEach(type => {
            const nodes = this.topologyData[type] || [];
            const positions = nodeTypes[type].positions;

            nodes.forEach((node, index) => {
                if (index < positions.length) {
                    const pos = positions[index];
                    
                    const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    nodeGroup.className = 'topology-node';
                    nodeGroup.setAttribute('data-type', type);
                    nodeGroup.setAttribute('data-name', node.name);

                    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    circle.setAttribute('cx', pos.x);
                    circle.setAttribute('cy', pos.y);
                    circle.setAttribute('r', 15);
                    circle.setAttribute('fill', nodeTypes[type].color);
                    circle.setAttribute('fill-opacity', '0.7');
                    circle.setAttribute('stroke', nodeTypes[type].color);
                    circle.setAttribute('stroke-width', '2');

                    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    text.setAttribute('x', pos.x);
                    text.setAttribute('y', pos.y + 30);
                    text.setAttribute('text-anchor', 'middle');
                    text.setAttribute('fill', 'white');
                    text.setAttribute('font-size', '10');
                    text.textContent = node.name;

                    // Add hover tooltip
                    nodeGroup.addEventListener('mouseenter', (e) => {
                        const tooltip = document.createElement('div');
                        tooltip.className = 'topology-tooltip';
                        tooltip.innerHTML = `
                            <strong>${node.name}</strong><br>
                            ${node.description || node.status || ''}
                        `;
                        tooltip.style.left = e.pageX + 10 + 'px';
                        tooltip.style.top = e.pageY + 10 + 'px';
                        document.body.appendChild(tooltip);
                    });

                    nodeGroup.addEventListener('mouseleave', () => {
                        const tooltips = document.querySelectorAll('.topology-tooltip');
                        tooltips.forEach(t => t.remove());
                    });

                    nodeGroup.appendChild(circle);
                    nodeGroup.appendChild(text);
                    svg.appendChild(nodeGroup);
                }
            });
        });
    }

    updateTopologyStats() {
        const skillCount = document.getElementById('skill-count');
        const channelCount = document.getElementById('channel-count');
        const providerCount = document.getElementById('provider-count');

        if (skillCount) skillCount.textContent = (this.topologyData.skills || []).length;
        if (channelCount) channelCount.textContent = (this.topologyData.channels || []).length;
        if (providerCount) providerCount.textContent = (this.topologyData.providers || []).length;
    }
}

// Initialize dashboard when DOM is ready
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new DashboardApp();
    
    // Add welcome time
    const welcomeTime = document.getElementById('welcome-time');
    if (welcomeTime) {
        welcomeTime.textContent = new Date().toLocaleTimeString();
    }

    // Add some initial log entries
    setTimeout(() => {
        dashboard.logActivity('System status: Online', 'success');
        dashboard.logActivity('Connected to LLM provider', 'success');
        dashboard.logActivity('Memory usage: Normal', 'info');
    }, 1000);
});

// Handle file upload
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file && dashboard) {
                dashboard.handleFileUpload(file);
                e.target.value = ''; // Reset
            }
        });
    }
});

console.log('🚀 Nanobot Dashboard initialized successfully!');
