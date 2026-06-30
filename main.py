from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

# -------- AI MOCK (şimdilik ücretsiz dummy AI) --------
def fake_ai_response(text: str):
    return f"🤖 AI: '{text}' için güçlü bir yanıt üretiyorum..."

# -------- API --------
@app.post("/chat")
def chat(req: ChatRequest):
    return {"response": fake_ai_response(req.message)}

# -------- UI --------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI SaaS Pro</title>

<style>
body {
    margin:0;
    font-family: Arial;
    background:#0b0f1a;
    color:white;
    display:flex;
    height:100vh;
}

.sidebar {
    width:260px;
    background:#0f172a;
    padding:20px;
}

.chat {
    flex:1;
    display:flex;
    flex-direction:column;
}

.messages {
    flex:1;
    padding:20px;
    overflow:auto;
}

.inputBox {
    display:flex;
    padding:10px;
    background:#111827;
}

input {
    flex:1;
    padding:10px;
    border:none;
    border-radius:8px;
}

button {
    margin-left:10px;
    padding:10px 20px;
    background:#4f46e5;
    border:none;
    color:white;
    border-radius:8px;
    cursor:pointer;
}

.msg {
    background:#1f2937;
    padding:10px;
    margin:10px 0;
    border-radius:8px;
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
    let msg = input.value;

    if(!msg) return;

    document.getElementById("messages").innerHTML +=
        `<div class='msg'>👤 ${msg}</div>`;

    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({message: msg})
    });

    const data = await res.json();

    document.getElementById("messages").innerHTML +=
        `<div class='msg'>${data.response}</div>`;
}

</script>

</body>
</html>
"""
