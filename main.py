from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time

app = FastAPI()

# =========================
# SIMPLE AI ENGINE
# =========================
def ai_engine(message: str):
    return f"🤖 AI: {message} için analiz yapıyorum..."

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str

# =========================
# CHAT API (STREAMING SIMULATION)
# =========================
@app.post("/chat-stream")
def chat_stream(req: ChatRequest):
    def generate():
        response = ai_engine(req.message)
        for char in response:
            yield char
            time.sleep(0.02)  # typing effect

    return app.response_class(generate(), media_type="text/plain")

# =========================
# UI
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI SaaS Pro v3</title>

<style>
body {
    margin:0;
    font-family: Arial;
    background:#0a0f1f;
    color:white;
    display:flex;
    height:100vh;
}

.sidebar {
    width:260px;
    background:#0f172a;
    padding:20px;
}

.sidebar h2 {
    color:#8b5cf6;
}

.chat {
    flex:1;
    display:flex;
    flex-direction:column;
}

.messages {
    flex:1;
    padding:20px;
    overflow-y:auto;
}

.msg {
    padding:12px;
    margin:10px 0;
    border-radius:10px;
    background:rgba(255,255,255,0.05);
}

.user {
    background:#1f2937;
}

.ai {
    background:#111827;
    border-left:3px solid #8b5cf6;
}

.inputBox {
    display:flex;
    padding:10px;
    background:#0f172a;
}

input {
    flex:1;
    padding:12px;
    border:none;
    border-radius:8px;
    background:#111827;
    color:white;
}

button {
    margin-left:10px;
    padding:12px 18px;
    background:#8b5cf6;
    border:none;
    border-radius:8px;
    color:white;
    cursor:pointer;
}
</style>
</head>

<body>

<div class="sidebar">
<h2>⚡ AI SaaS</h2>
<p>Dashboard</p>
<p>History</p>
<p>Settings</p>
</div>

<div class="chat">

<div class="messages" id="messages"></div>

<div class="inputBox">
<input id="input" placeholder="Ask AI..." />
<button onclick="send()">Send</button>
</div>

</div>

<script>

async function send() {
    let input = document.getElementById("input");
    let text = input.value;

    if(!text) return;

    document.getElementById("messages").innerHTML +=
        `<div class='msg user'>👤 ${text}</div>`;

    input.value = "";

    const res = await fetch("/chat-stream", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({message: text})
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    let aiMsg = document.createElement("div");
    aiMsg.className = "msg ai";
    document.getElementById("messages").appendChild(aiMsg);

    let textContent = "";

    while(true){
        const {value, done} = await reader.read();
        if(done) break;

        textContent += decoder.decode(value);
        aiMsg.innerText = textContent;
    }
}

</script>

</body>
</html>
"""
