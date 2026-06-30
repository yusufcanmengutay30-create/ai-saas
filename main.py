from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import uuid

app = FastAPI()

# DB
conn = sqlite3.connect("saas.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
token TEXT PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
id INTEGER PRIMARY KEY AUTOINCREMENT,
token TEXT,
message TEXT,
response TEXT
)
""")

conn.commit()

# --------------------
# AI ENGINE (fake safe)
# --------------------
def ai_engine(msg):
    return f"AI RESPONSE: {msg}"

# --------------------
# LOGIN
# --------------------
class Login(BaseModel):
    username: str

@app.post("/login")
def login(req: Login):
    token = str(uuid.uuid4())
    cursor.execute("INSERT INTO users VALUES (?)", (token,))
    conn.commit()
    return {"token": token}

# --------------------
# CHAT
# --------------------
class Chat(BaseModel):
    token: str
    message: str

@app.post("/chat")
def chat(req: Chat):

    cursor.execute("SELECT token FROM users WHERE token=?", (req.token,))
    user = cursor.fetchone()

    if not user:
        return {"error": "invalid token"}

    response = ai_engine(req.message)

    cursor.execute(
        "INSERT INTO chats (token, message, response) VALUES (?,?,?)",
        (req.token, req.message, response)
    )
    conn.commit()

    return {"response": response}

# --------------------
# HISTORY
# --------------------
@app.get("/history/{token}")
def history(token: str):
    cursor.execute("SELECT message, response FROM chats WHERE token=?", (token,))
    return {"data": cursor.fetchall()}

# --------------------
# UI
# --------------------
@app.get("/", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
<title>VC SaaS v2</title>

<style>
body{margin:0;font-family:Arial;background:#0b0f19;color:white;display:flex;height:100vh}

.sidebar{width:250px;background:#111827;padding:20px}
.main{flex:1;display:flex;flex-direction:column}

.top{padding:10px;background:#0f172a;display:flex;justify-content:space-between}

.chat{flex:1;padding:20px;overflow:auto}

.msg{padding:10px;margin:5px;border-radius:10px;max-width:70%}
.user{background:#1f2937;margin-left:auto}
.ai{background:#111827;border-left:3px solid #6366f1}

.input{display:flex;padding:10px;background:#0f172a}
input{flex:1;padding:10px;border:none;border-radius:10px}
button{margin-left:10px;padding:10px;background:#6366f1;color:white;border:none;border-radius:10px}
</style>

</head>

<body>

<div class="sidebar">
<h2>VC SAAS</h2>

<button onclick="login()">Login</button>
<p id="token"></p>

</div>

<div class="main">

<div class="top">
<div>VC MODE</div>
</div>

<div class="chat" id="chat"></div>

<div class="input">
<input id="msg" placeholder="ask..." />
<button onclick="send()">Send</button>
</div>

</div>

<script>

let TOKEN = ""

async function login(){

let username = "user"

const res = await fetch("/login",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({username})
})

const data = await res.json()
TOKEN = data.token

document.getElementById("token").innerText = TOKEN
}

async function send(){

let msg = document.getElementById("msg").value

document.getElementById("chat").innerHTML +=
`<div class='msg user'>${msg}</div>`

const res = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
token:TOKEN,
message:msg
})
})

const data = await res.json()

document.getElementById("chat").innerHTML +=
`<div class='msg ai'>${data.response}</div>`
}

</script>

</body>
</html>
"""
