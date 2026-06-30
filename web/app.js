async function generate() {
  const user = document.getElementById("user").value;
  const password = document.getElementById("pass").value;
  const prompt = document.getElementById("prompt").value;
  const mode = document.getElementById("mode").value;

  const res = await fetch("http://127.0.0.1:8000/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user,
      password,
      prompt,
      mode,
    }),
  });

  const data = await res.json();

  document.getElementById("result").innerHTML = `
        <h3>📦 Output</h3>
        <pre>${data.output || data.error}</pre>

        <h3>🔥 Score: ${data.score?.score || "?"}</h3>
        <h3>📊 Level: ${data.score?.level || "?"}</h3>
    `;
}
