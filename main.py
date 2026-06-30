from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# =========================
# AI ENGINE (BASIC)
# =========================
def ai_engine(message: str):
    return f"🤖 AI: '{message}' için analiz yapıyorum... (v2 engine aktif)"

# =========================
# API
# =========================
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    return {"response": ai_engine(req.message)}

# =========================
# UI (CHATGPT STYLE)
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI SaaS Pro v2</title>

<style>
body {
    margin:0;
    font-family: Arial;
    background:#0a0f1f;
    color:white;
    display:flex;
    height:100vh;
}

/* SIDEBAR */
.sidebar {
    width:260px;
    background:#0f172a;
    padding:20px;
    border-right:1px solid rgba(255,255,255,0.05);
}

.sidebar h2 {
    color:#7c3aed;
}

.sidebar p {
    opacity:0.7;
    cursor:pointer;
}

/* MAIN CHAT */
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
    border-left:3px solid #7c3aed;
}

/* INPUT */
.inputArea {
    display:flex;
    padding:10px;
    background:#0f172a;
    border-top:1px solid rgba(255,255,255,0.05);
}

input {
    flex:1;
    padding:12px;
    border:none;
    border-radius:8px;
    outline:none;
    background:#111827;
    color:white;
}

button {
    margin-left:10px;
    padding:12px 18px;
    background:#7c3aed;
    border:none;
    border-radius:8px;
    color:white;
    cursor:pointer;
}
</style>
</head>

<body>

<div class="sidebar">
<h2>⚡ AI SaaS v2</h2>
<p>Dashboard</p>
<p>History</p>
<p>Settings</p>
</div>

<div class="chat">

<div class="messages" id="messages"></div>

<div class="inputArea">
<input id="input" placeholder="Ask AI..." />
<button onclick="send()">Send</button>
</div>

</div>

<script>

async function send() {
    let input = document.getElementById("input");
    let text = input.value;

    if(!text) return;

    // USER MESSAGE
    document.getElementById("messages").innerHTML +=
        `<div class='msg user'>👤 ${text}</div>`;

    input.value = "";

    // AI REQUEST
    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({message: text})
    });

    const data = await res.json();

    // AI MESSAGE
    document.getElementById("messages").innerHTML +=
        `<div class='msg ai'>${data.response}</div>`;
}

</script>

</body>
</html>
"""
