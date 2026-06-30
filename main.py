from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import sqlite3
import asyncio
import json
import requests

app = FastAPI()

# ---------------- DB ----------------
conn = sqlite3.connect("saas.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
id INTEGER PRIMARY KEY AUTOINCREMENT,
role TEXT,
content TEXT
)
""")
conn.commit()


# ---------------- REQUEST ----------------
class Msg(BaseModel):
    message: str


def save(role, content):
    cur.execute("INSERT INTO messages (role, content) VALUES (?,?)", (role, content))
    conn.commit()


def load():
    cur.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 10")
    return cur.fetchall()[::-1]


# ---------------- UI ----------------
@app.get("/", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI SaaS Live</title>

<style>
body{margin:0;font-family:Arial;background:#05060a;color:white;overflow:hidden}
.container{display:flex;height:100vh}
.sidebar{width:260px;background:#111;padding:20px}
.chat{flex:1;display:flex;flex-direction:column;padding:20px}
.msg{padding:10px;margin:8px;border-radius:10px;max-width:70%}
.user{background:#4c8dff;margin-left:auto}
.ai{background:#222}
.input{display:flex;gap:10px;margin-top:10px}
input{flex:1;padding:12px;background:#222;border:none;color:white}
button{padding:12px;background:#4c8dff;border:none;color:white}
.messages{flex:1;overflow:auto}
</style>
</head>

<body>
<div class="container">

<div class="sidebar">
<h3>⚡ AI SaaS</h3>
<p>Public Zero Cost Product</p>
</div>

<div class="chat">

<div class="messages" id="m"></div>

<div class="input">
<input id="i">
<button onclick="send()">Send</button>
</div>

</div>

</div>

<script>

async function send(){
 let text=i.value;
 add(text,"user");
 i.value="";

 const r=await fetch("/chat",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({message:text})
 });

 const reader=r.body.getReader();
 const dec=new TextDecoder();

 let ai=document.createElement("div");
 ai.className="msg ai";
 m.appendChild(ai);

 while(true){
  let {value,done}=await reader.read();
  if(done)break;
  ai.innerHTML+=dec.decode(value);
  m.scrollTop=m.scrollHeight;
 }
}

function add(t,type){
 let d=document.createElement("div");
 d.className="msg "+type;
 d.innerText=t;
 m.appendChild(d);
}
</script>

</body>
</html>
"""


# ---------------- AI ENGINE (FREE HYBRID) ----------------
@app.post("/chat")
async def chat(req: Msg):

    save("user", req.message)

    history = load()
    context = "\n".join([f"{r[0]}:{r[1]}" for r in history])

    # TRY LOCAL OLLAMA FIRST
    def try_ollama():
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5",
                    "stream": True,
                    "prompt": f"History:\n{context}\nUser:{req.message}\nAI:"
                },
                stream=True,
                timeout=2
            )
            return r
        except:
            return None

    async def stream():

        r = try_ollama()

        # fallback if no local AI
        if not r:
            response = f"AI (free mode): I received -> {req.message}"

            for c in response:
                yield c
                await asyncio.sleep(0.01)

            save("ai", response)
            return

        full = ""

        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode())
                token = data.get("response","")
                full += token
                yield token
                await asyncio.sleep(0.01)

        save("ai", full)

    return StreamingResponse(stream(), media_type="text/plain")
