document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("send-button");
    const messageInput = document.getElementById("message-input");
    const chatMessages = document.getElementById("chat-messages");

    let contextId = null;
    let messageCounter = 0;

    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    function generateId() {
        return "neo-" + (++messageCounter).toString().padStart(3, "0");
    }

    function appendMessage(sender, text) {
        const div = document.createElement("div");
        div.className = "message " + (sender === "user" ? "user-message" : "smith-message");
        div.innerHTML =
            '<span class="sender">' + (sender === "user" ? "NEO" : "SMITH") + "</span>" +
            '<span class="text">' + escapeHtml(text) + "</span>";
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        const div = document.createElement("div");
        div.className = "message smith-message typing";
        div.id = "typing-indicator";
        div.innerHTML = '<span class="sender">SMITH</span><span class="text">...</span>';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTyping() {
        const el = document.getElementById("typing-indicator");
        if (el) el.remove();
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    async function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        appendMessage("user", text);
        messageInput.value = "";
        sendButton.disabled = true;
        showTyping();

        const msgId = generateId();
        const payload = {
            jsonrpc: "2.0",
            id: msgId,
            method: "SendMessage",
            params: {
                message: {
                    role: "ROLE_USER",
                    parts: [{ text: text }],
                    messageId: msgId,
                },
            },
        };

        if (contextId) {
            payload.params.message.contextId = contextId;
        }

        try {
            const response = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "A2A-Version": "1.0",
                },
                body: JSON.stringify(payload),
            });

            const contentType = response.headers.get("content-type") || "";

            if (contentType.includes("text/event-stream")) {
                await handleStream(response);
            } else {
                const data = await response.json();
                extractAndDisplayResponse(data);
            }
        } catch (error) {
            removeTyping();
            appendMessage("smith", "Connection lost... the Matrix is unstable.");
        } finally {
            sendButton.disabled = false;
            messageInput.focus();
        }
    }

    async function handleStream(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let smithText = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n");
            buffer = lines.pop();

            for (const line of lines) {
                if (line.startsWith("data:")) {
                    const data = line.substring(5).trim();
                    if (!data) continue;
                    try {
                        const json = JSON.parse(data);
                        if (json.contextId && !contextId) {
                            contextId = json.contextId;
                        }
                        const text = extractText(json);
                        if (text) smithText += text;
                    } catch (e) {}
                }
            }
        }

        removeTyping();
        if (smithText) {
            appendMessage("smith", smithText);
        }
    }

    function extractText(obj) {
        if (obj.artifact && obj.artifact.parts) {
            for (const part of obj.artifact.parts) {
                if (part.text) return part.text;
            }
        }
        if (obj.parts) {
            for (const part of obj.parts) {
                if (part.text) return part.text;
            }
        }
        if (obj.status && obj.status.message && obj.status.message.parts) {
            for (const part of obj.status.message.parts) {
                if (part.text) return part.text;
            }
        }
        return null;
    }

    function findTextInObject(obj) {
        if (!obj || typeof obj !== "object") return null;
        if (obj.text && typeof obj.text === "string") return obj.text;
        if (Array.isArray(obj)) {
            for (const item of obj) {
                const found = findTextInObject(item);
                if (found) return found;
            }
        }
        for (const key of Object.keys(obj)) {
            if (key === "text" && typeof obj[key] === "string") return obj[key];
            const found = findTextInObject(obj[key]);
            if (found) return found;
        }
        return null;
    }

    function extractAndDisplayResponse(data) {
        removeTyping();

        if (data.result) {
            if (data.result.contextId) contextId = data.result.contextId;

            const text = extractText(data.result);
            if (text) {
                appendMessage("smith", text);
                return;
            }

            if (data.result.artifacts) {
                for (const artifact of data.result.artifacts) {
                    const text = extractText(artifact);
                    if (text) {
                        appendMessage("smith", text);
                        return;
                    }
                }
            }

            const deepText = findTextInObject(data.result);
            if (deepText) {
                appendMessage("smith", deepText);
                return;
            }
        }

        if (data.error) {
            appendMessage("smith", data.error.message || "An error occurred.");
            return;
        }

        appendMessage("smith", "...");
    }
});
