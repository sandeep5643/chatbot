// Include this in your index.html head or before closing </body>
// <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

async function sendMessage() {
    const input = document.getElementById("msg");
    const msg = input.value.trim();
    if (!msg) return; // Empty message ignore
    input.value = "";

    append("You: " + msg, "user-message");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();
        append(data.reply, "bot-message"); // Bot reply
    } catch (err) {
        append("Error: " + err.message, "bot-message");
    }
}

// Append message to chat box
function append(text, className = "") {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");
    if (className) div.classList.add(className);

    // Use marked.js to render Markdown into HTML
    div.innerHTML = marked.parse(text);

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
