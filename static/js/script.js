const userInput = document.getElementById("userInput");
const chatBox = document.getElementById("chatMessages");
const loading = document.getElementById("loading");

function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    addMessage("user-message", question);
    userInput.value = "";
    loading.style.display = "block";

    setTimeout(() => {
        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        })
            .then(response => response.json())
            .then(data => {
                const confidence = data.confidence || 0;
                let response = "";

                if (data.answer.includes("I'm not sure")) {
                    response = `<div class="no-match">${data.answer}</div>`;
                    response += '<div class="suggestion-buttons">';
                    const suggestions = [
                        "How long does shipping take?",
                        "Do you offer customer support?",
                        "What is your privacy policy?"
                    ];
                    suggestions.forEach(q => {
                        response += `<span class="suggestion-btn" onclick="askQuestion('${q}')">${q}</span>`;
                    });
                    response += '</div>';
                } else {
                    response = `${data.answer}`;
                }

                setTimeout(() => {
                    loading.style.display = "none";
                    addMessage("bot-message", response);
                }, 500);
            })
            .catch(error => {
                console.error("Error:", error);
                loading.style.display = "none";
                addMessage("bot-message", "❌ Oops! Something went wrong.");
            });
    }, 100);
}

function addMessage(type, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${type}`;
    msgDiv.innerHTML = `<div class="message-bubble">${text}</div>`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKeyPress(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
}

function askQuestion(q) {
    userInput.value = q;
    sendMessage();
}
