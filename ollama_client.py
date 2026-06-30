import requests

class OllamaClient:
    def __init__(self, model="llama3.1"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def ask(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": f"""
You are a viral Shorts creator.

Return EXACTLY 5 ideas.

Format each:

Title
HOOK (0-2s)
CONTENT (10-30s)
RETENTION trick

No extra text.

Topic:
{prompt}
""",
                "stream": False
            }
        )

        return response.json()["response"]

