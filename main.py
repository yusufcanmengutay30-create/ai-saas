from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import requests

app = FastAPI()

# DB
conn = sqlite3.connect("saas.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
id INTEGER PRIMARY KEY AUTOINCREMENT,
message TEXT,
response TEXT
)
""")
conn.commit()

# AI (local fallback)
def ai_engine(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model":"llama3.1","prompt":prompt,"stream":False}
        )
        return r.json()["response"]
    except:
        return "AI: " + prompt


class Chat(BaseModel):
    message: str


@app.post("/chat")
def chat(req: Chat):
    response = ai_engine(req.message)

    cursor.execute(
        "INSERT INTO chats (message, response) VALUES (?,?)",
        (req.message, response)
    )
    conn.commit()

    return {"response": response}


@app.get("/", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI SaaS</title>

<style>
body {
margin:0;
font-family:Arial;
background:#0b0f19;
color:white;
display:flex;
}

.sidebar {
width:260px;
background:#111827;
padding:20px;
}

.main {
flex:1;
display:flex;
flex-direction:column;
}

.chat {
flex:1;
padding:20px;
overflow:auto;
}

input {
padding:12px;
width:80%;
border-radius:10px;
border:none;
}

button {
padding:12px;
border:none;
background:#6366f1;
color:white;
border-radius:10px;
}
</style>

</head>

<body>

<div class="sidebar">
<h2>AI SaaS</h2>
<p>Dashboard</p>
<p>History</p>
</div>

<div class="main">

<div class="chat" id="chat"></div>

<div style="padding:10px;">
<input id="msg" placeholder="Ask..." />
<button onclick="send()">Send</button>
</div>

</div>

<script>

async function send(){
let msg = document.getElementById("msg").value;

document.getElementById("chat").innerHTML +=
`<div>🧑 ${msg}</div>`;

const res = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg})
});

const data = await res.json();

document.getElementById("chat").innerHTML +=
`<div>🤖 ${data.response}</div>`;
}

</script>

</body>
</html>
"""
