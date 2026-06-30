import time

from brain.commands import handle_command
from brain.engine import generate
from brain.memory import add_memory
from brain.logger import write_log, update_stats
from brain.scorer import viral_score


print("=" * 60)
print("🚀 AI CONTENT FACTORY v10")
print("Komutlar:")
print("/youtube konu")
print("/tiktok konu")
print("/affiliate ürün")
print("/help")
print("Çıkmak için: exit")
print("=" * 60)

while True:

    user_input = input("\nSen > ").strip()

    if user_input.lower() == "exit":
        break

    mode, prompt = handle_command(user_input)

    start = time.time()

    result = generate(
        prompt=prompt,
        mode=mode
    )

    elapsed = round(time.time() - start, 2)

    output = result["output"]

    add_memory("user", user_input)
    add_memory("assistant", output)

    update_stats()

    score = viral_score(output)

    write_log(
        f"""MODE: {mode}

PROMPT:
{user_input}

OUTPUT:
{output}

VIRAL SCORE:
{score["score"]}

LEVEL:
{score["level"]}

TIME:
{elapsed} saniye
"""
    )

    print("\n" + "=" * 60)
    print(f"🤖 Mod: {mode}")
    print(f"⚡ Süre: {elapsed} sn")
    print(f"🔥 Viral Score: {score['score']}/100")
    print(f"📈 Seviye: {score['level']}")
    print("=" * 60)
    print("\nAI:\n")
    print(output)
