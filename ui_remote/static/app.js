/**
 * ui_remote/static/app.js
 * 
 * AynCoding Remote Client (GravityRemote Clone for AynCoding-Gemma2 on :4000)
 * Handles:
 * - Real-time SSE token streaming
 * - Telemetry polling (CPU, RAM, Ollama status)
 * - Collapsible <ayn_mantiq> reasoning drawers
 * - In-browser 5-Pillar Static Epistemic Audit modal
 * - In-browser Epistemic Code Purification modal
 * - 1-Click Code copy & quick prompts
 */

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const modelSelect = document.getElementById('model-select');
const cpuStat = document.getElementById('cpu-stat');
const ramStat = document.getElementById('ram-stat');
const ollamaStat = document.getElementById('ollama-stat');

let isGenerating = false;
let abortController = null;

// ==========================================================================
// Telemetry & Model Management
// ==========================================================================
async function fetchTelemetry() {
    try {
        const resp = await fetch('/api/stats');
        if (!resp.ok) return;
        const data = await resp.json();

        if (cpuStat) cpuStat.textContent = `${data.cpu_percent}%`;
        if (ramStat) ramStat.textContent = `${data.mem_used_mb} / ${data.mem_total_mb} MB`;
        
        if (ollamaStat) {
            if (data.ollama_online) {
                ollamaStat.textContent = 'ONLINE';
                ollamaStat.style.color = 'var(--accent-green)';
            } else {
                ollamaStat.textContent = 'OFFLINE';
                ollamaStat.style.color = 'var(--accent-red)';
            }
        }
    } catch (e) {
        console.warn('Telemetry fetch error:', e);
    }
}

async function loadModels() {
    try {
        const resp = await fetch('/api/models');
        if (!resp.ok) return;
        const data = await resp.json();
        if (data.models && data.models.length > 0) {
            const currentVal = modelSelect.value;
            modelSelect.innerHTML = '';
            
            // Prioritize ayncoding-gemma2
            const sortedModels = [...data.models].sort((a, b) => {
                if (a.includes('gemma2')) return -1;
                if (b.includes('gemma2')) return 1;
                return 0;
            });

            sortedModels.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m;
                opt.textContent = m === 'ayncoding-gemma2' ? 'ayncoding-gemma2 (2.6B NUMA-16)' : m;
                modelSelect.appendChild(opt);
            });

            if (data.models.includes(currentVal)) {
                modelSelect.value = currentVal;
            } else {
                modelSelect.value = 'ayncoding-gemma2';
            }
        }
    } catch (e) {
        console.warn('Model list fetch error:', e);
    }
}

// ==========================================================================
// Markdown & Logic Tag Parsing
// ==========================================================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function parseModelOutput(rawText) {
    let text = rawText;
    let mantiqHtml = '';

    // 1. Extract <ayn_mantiq>...</ayn_mantiq>
    const mantiqRegex = /<ayn_mantiq>([\s\S]*?)(?:<\/ayn_mantiq>|$)/i;
    const mantiqMatch = text.match(mantiqRegex);
    if (mantiqMatch) {
        const mantiqContent = mantiqMatch[1].trim();
        mantiqHtml = `
            <div class="mantiq-drawer">
                <div class="mantiq-drawer-header" onclick="this.parentElement.classList.toggle('collapsed')">
                    <span>⟨ayn_mantiq: Classical Logic Formulation⟩</span>
                    <span class="mantiq-toggle-icon">▼</span>
                </div>
                <div class="mantiq-drawer-content">${escapeHtml(mantiqContent)}</div>
            </div>
        `;
        text = text.replace(mantiqRegex, '').trim();
    }

    // 2. Parse fenced code blocks ```lang ... ```
    const codeBlockRegex = /```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g;
    let parts = [];
    let lastIdx = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
        // Text before code block
        const prevText = text.substring(lastIdx, match.index);
        if (prevText) {
            parts.push(renderPlainText(prevText));
        }

        const lang = match[1] || 'code';
        const codeSnippet = match[2];
        const encodedCode = encodeURIComponent(codeSnippet);

        parts.push(`
            <div class="code-container">
                <div class="code-header">
                    <span>${lang.toUpperCase()}</span>
                    <div class="code-actions">
                        <button class="code-btn" onclick="copySnippet('${encodedCode}', this)">📋 Copy</button>
                        <button class="code-btn" onclick="auditSnippet('${encodedCode}')">🧪 Audit</button>
                        <button class="code-btn" onclick="purifySnippet('${encodedCode}')">🌿 Purify</button>
                    </div>
                </div>
                <pre class="code-block"><code>${escapeHtml(codeSnippet)}</code></pre>
            </div>
        `);
        lastIdx = match.index + match[0].length;
    }

    // Trailing text or streaming incomplete code block
    const remainingText = text.substring(lastIdx);
    if (remainingText) {
        if (remainingText.includes('```')) {
            const incompleteMatch = remainingText.match(/```([a-zA-Z0-9_-]*)\n([\s\S]*)$/);
            if (incompleteMatch) {
                const lang = incompleteMatch[1] || 'code';
                const codeSnippet = incompleteMatch[2];
                parts.push(`
                    <div class="code-container">
                        <div class="code-header">
                            <span>${lang.toUpperCase()} (Streaming...)</span>
                        </div>
                        <pre class="code-block"><code>${escapeHtml(codeSnippet)}</code></pre>
                    </div>
                `);
            } else {
                parts.push(renderPlainText(remainingText));
            }
        } else {
            parts.push(renderPlainText(remainingText));
        }
    }

    return mantiqHtml + parts.join('');
}

function renderPlainText(text) {
    return text.split('\n\n').map(p => {
        if (!p.trim()) return '';
        // Bold formatting
        let formatted = escapeHtml(p).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Inline code
        formatted = formatted.replace(/`([^`]+)`/g, '<code style="background:var(--bg-code);padding:2px 5px;border-radius:3px;font-family:var(--font-mono);font-size:12px;">$1</code>');
        return `<p style="margin-bottom: 8px;">${formatted.replace(/\n/g, '<br>')}</p>`;
    }).join('');
}

// Global Snippet Actions
window.copySnippet = function(encodedCode, btnElement) {
    const code = decodeURIComponent(encodedCode);
    navigator.clipboard.writeText(code).then(() => {
        const originalText = btnElement.textContent;
        btnElement.textContent = '✓ Copied!';
        setTimeout(() => {
            btnElement.textContent = originalText;
        }, 1500);
    });
};

window.auditSnippet = function(encodedCode) {
    const code = decodeURIComponent(encodedCode);
    document.getElementById('audit-code-input').value = code;
    openModal('modal-audit');
    document.getElementById('btn-run-audit-modal').click();
};

window.purifySnippet = function(encodedCode) {
    const code = decodeURIComponent(encodedCode);
    document.getElementById('purify-code-input').value = code;
    openModal('modal-purify');
    document.getElementById('btn-run-purify-modal').click();
};

// ==========================================================================
// Streaming Chat Execution
// ==========================================================================
async function sendMessage(promptOverride = null) {
    const prompt = promptOverride !== null ? promptOverride : chatInput.value.trim();
    if (!prompt || isGenerating) return;

    if (promptOverride === null) {
        chatInput.value = '';
        chatInput.style.height = 'auto';
    }

    // Append User Message Row
    const userRow = document.createElement('div');
    userRow.className = 'message-row user';
    userRow.innerHTML = `
        <div class="message-header avatar-user">
            <span>👤 You</span>
        </div>
        <div class="message-body">
            <p>${escapeHtml(prompt)}</p>
        </div>
    `;
    chatContainer.appendChild(userRow);

    // Append AI Streaming Response Row
    const aiRow = document.createElement('div');
    aiRow.className = 'message-row';
    const selectedModel = modelSelect.value || 'ayncoding-gemma2';
    aiRow.innerHTML = `
        <div class="message-header avatar-ai">
            <span>🏛️ ${escapeHtml(selectedModel)}</span>
        </div>
        <div class="message-body ai-body">
            <span style="color: var(--text-muted); font-style: italic;">Thinking with classical logic...</span>
        </div>
    `;
    chatContainer.appendChild(aiRow);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    const aiBody = aiRow.querySelector('.ai-body');
    let fullResponseText = '';
    isGenerating = true;
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span>⏳</span> ...';

    abortController = new AbortController();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: prompt,
                model: selectedModel
            }),
            signal: abortController.signal
        });

        if (!response.ok) {
            throw new Error(`HTTP Error ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n\n');
            buffer = lines.pop(); // Keep last partial line in buffer

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const rawJson = line.replace('data: ', '').trim();
                    if (!rawJson) continue;
                    try {
                        const parsed = JSON.parse(rawJson);
                        if (parsed.token) {
                            fullResponseText += parsed.token;
                            aiBody.innerHTML = parseModelOutput(fullResponseText);
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                        if (parsed.error) {
                            fullResponseText += `\n\n[Error: ${parsed.error}]`;
                            aiBody.innerHTML = parseModelOutput(fullResponseText);
                        }
                        if (parsed.done) {
                            break;
                        }
                    } catch (err) {
                        console.error('SSE JSON parse error:', err);
                    }
                }
            }
        }
    } catch (err) {
        if (err.name !== 'AbortError') {
            aiBody.innerHTML = `<p style="color: var(--accent-red);">Stream Error: ${escapeHtml(err.message)}</p>`;
        }
    } finally {
        isGenerating = false;
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<span>Send</span> ↵';
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// ==========================================================================
// Modal Handlers & Logic
// ==========================================================================
window.openModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
};

window.closeModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
};

// Close modal when clicking on backdrop
document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});

// Epistemic Audit Modal Runner
document.getElementById('btn-run-audit-modal').addEventListener('click', async () => {
    const code = document.getElementById('audit-code-input').value.trim();
    const resultsContainer = document.getElementById('audit-results-container');
    if (!code) return;

    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = '<p style="color: var(--text-muted);">Executing 5-Pillar Static Epistemic Audit...</p>';

    try {
        const resp = await fetch('/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, language: 'python' })
        });
        const data = await resp.json();

        let pillarsHtml = '';
        if (data.pillars) {
            for (const [key, p] of Object.entries(data.pillars)) {
                pillarsHtml += `
                    <div style="background: var(--bg-card); padding: 8px 12px; margin-bottom: 6px; border-radius: 4px; border-left: 3px solid var(--accent);">
                        <div style="display:flex; justify-content:space-between; font-weight:700; font-size:12px;">
                            <span>${escapeHtml(p.title)}</span>
                            <span style="color: var(--accent-cyan);">${p.score}/100</span>
                        </div>
                        <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 3px;">${escapeHtml(p.critique)}</div>
                    </div>
                `;
            }
        }

        let fallaciesHtml = '';
        if (data.fallacies && data.fallacies.length > 0) {
            fallaciesHtml = `
                <div style="margin-top: 10px; padding: 10px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 4px;">
                    <div style="color: var(--accent-red); font-weight: bold; font-size: 12px;">Classical Fallacies Detected:</div>
                    <div style="font-size: 11.5px; color: #fca5a5; margin-top: 4px; font-weight: 600;">
                        ${data.fallacies.join(', ')}
                    </div>
                    ${data.fallacy_remediation ? `<div style="font-size: 11.5px; color: #f8fafc; margin-top: 4px;"><strong>Remediation:</strong> ${escapeHtml(data.fallacy_remediation)}</div>` : ''}
                    ${data.citation ? `<div style="font-size: 10.5px; color: var(--text-muted); margin-top: 4px; font-style: italic;">Axiom: ${escapeHtml(data.citation)}</div>` : ''}
                </div>
            `;
        }

        resultsContainer.innerHTML = `
            <div class="scorecard-banner">
                <div>
                    <div class="scorecard-metric" style="color: ${data.grade.startsWith('A') ? 'var(--accent-green)' : 'var(--accent-gold)'}">${data.grade}</div>
                    <div class="scorecard-label">Grade</div>
                </div>
                <div>
                    <div class="scorecard-metric">${data.overall_score}%</div>
                    <div class="scorecard-label">Score</div>
                </div>
                <div>
                    <div class="scorecard-metric" style="color: ${data.syntax_valid ? 'var(--accent-green)' : 'var(--accent-red)'}">
                        ${data.syntax_valid ? 'VALID' : 'INVALID'}
                    </div>
                    <div class="scorecard-label">AST Syntax</div>
                </div>
            </div>
            <div style="margin-top: 12px;">${pillarsHtml}</div>
            ${fallaciesHtml}
        `;
    } catch (err) {
        resultsContainer.innerHTML = `<p style="color: var(--accent-red);">Audit Error: ${escapeHtml(err.message)}</p>`;
    }
});

// Epistemic Purifier Modal Runner
document.getElementById('btn-run-purify-modal').addEventListener('click', async () => {
    const code = document.getElementById('purify-code-input').value.trim();
    const resultsContainer = document.getElementById('purify-results-container');
    if (!code) return;

    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = '<p style="color: var(--text-muted);">Executing Epistemic Code Purification...</p>';

    try {
        const resp = await fetch('/api/purify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });
        const data = await resp.json();

        const encodedCleaned = encodeURIComponent(data.purified_code);

        resultsContainer.innerHTML = `
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 8px 12px; border-radius: 4px; margin-bottom: 10px; font-size: 12px; color: var(--accent-green);">
                ✓ Code successfully cleansed. Bare exceptions purged: <strong>${data.purged_bare_exceptions}</strong>. Unlogical names purged: <strong>${data.purged_unlogical_names.length}</strong>.
            </div>
            <div class="code-container">
                <div class="code-header">
                    <span>PURIFIED PYTHON</span>
                    <button class="code-btn" onclick="copySnippet('${encodedCleaned}', this)">📋 Copy Cleaned</button>
                </div>
                <pre class="code-block"><code>${escapeHtml(data.purified_code)}</code></pre>
            </div>
            <div style="margin-top: 8px; font-size: 11px; color: var(--text-muted);">
                <strong>Classical Justifications:</strong>
                <ul style="margin-left: 18px; margin-top: 4px;">
                    ${data.justifications.map(j => `<li>${escapeHtml(j)}</li>`).join('')}
                </ul>
            </div>
        `;
    } catch (err) {
        resultsContainer.innerHTML = `<p style="color: var(--accent-red);">Purification Error: ${escapeHtml(err.message)}</p>`;
    }
});

// ==========================================================================
// Event Listeners & Initialization
// ==========================================================================
sendBtn.addEventListener('click', () => sendMessage());

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-expand input height
chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + 'px';
});

// Quick Prompt Chips
document.querySelectorAll('.quick-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        const prompt = chip.getAttribute('data-prompt');
        chatInput.value = prompt;
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + 'px';
        sendMessage(prompt);
    });
});

// Control Bar Buttons
document.getElementById('btn-new-chat').addEventListener('click', () => {
    chatContainer.innerHTML = `
        <div class="message-row">
            <div class="message-header avatar-ai">
                <span>🏛️ AynCoding Gemma-2 (Autonomous Epistemic Agent)</span>
            </div>
            <div class="message-body">
                <p>New session initialized. Select a challenge above or submit your requirements below.</p>
            </div>
        </div>
    `;
});

document.getElementById('btn-open-purify').addEventListener('click', () => {
    openModal('modal-purify');
});

document.getElementById('btn-open-audit').addEventListener('click', () => {
    openModal('modal-audit');
});

document.getElementById('btn-reload-stats').addEventListener('click', () => {
    fetchTelemetry();
    loadModels();
});

// Bootstrapping
fetchTelemetry();
loadModels();
setInterval(fetchTelemetry, 2500);
