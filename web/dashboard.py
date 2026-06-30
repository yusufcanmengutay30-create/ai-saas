from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from brain.engine import generate
from brain.memory import add_memory
from brain.scorer import viral_score
from brain.logger import update_stats

app = FastAPI(title="AI Content Factory Dashboard")


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Content Factory</title>
    <meta charset="UTF-8">

    <style>
        body {
            margin:0;
            font-family: Arial;
            background:#0d0d0d;
            color:white;
        }

        .container {
            display:flex;
            height:100vh;
        }

        .left {
            width:30%;
            padding:20px;
            background:#141414;
        }

        .right {
            width:70%;
            padding:20px;
            overflow:auto;
        }

        input, select, button {
            width:100%;
            padding:12px;
            margin-top:10px;
            border:none;
            border-radius:8px;
        }

        button {
            background:#00c853;
            color:white;
            cursor:pointer;
        }

        .card {
            background:#1e1e1e;
            padding:15px;
            margin-bottom:15px;
            border-radius:10px;
        }

        .score {
            color:#00e676;
            font-weight:bold;
        }
    </style>
</head>

<body>

<div class="container">

    <div class="left">
        <h2>🚀 AI Factory</h2>

        <form action="/generate" method="post">

            <input name="prompt" placeholder="Ne üretmek istiyorsun?" required>

            <select name="mode">
                <option value="youtube">YouTube</option>
                <option value="tiktok">TikTok</option>
                <option value="affiliate">Affiliate</option>
            </select>

            <button type="submit">ÜRET</button>
        </form>
    </div>

    <div class="right">
        {%CONTENT%}
    </div>

</div>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML.replace("{%CONTENT%}", "<h2>Hazır. Prompt yaz ve üret.</h2>")


@app.post("/generate", response_class=HTMLResponse)
def generate_web(prompt: str = Form(...), mode: str = Form(...)):

    result = generate(prompt=prompt, mode=mode)

    output = result["output"]

    add_memory("user", prompt)
    add_memory("assistant", output)

    update_stats()

    score = viral_score(output)

    content = f"""
    <div class="card">
        <h3>📌 Sonuç</h3>
        <pre style="white-space:pre-wrap">{output}</pre>

        <p class="score">🔥 Viral Score: {score['score']} ({score['level']})</p>
    </div>
    """

    return HTML.replace("{%CONTENT%}", content)
