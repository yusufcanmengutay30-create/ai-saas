import argparse
import json

from brain.engine import generate
from brain.memory import add_memory
from brain.scorer import viral_score
from brain.logger import update_stats


def run_once(prompt, mode, model):
    print("\n🤖 AI çalışıyor...\n")

    result = generate(
        prompt=prompt,
        mode=mode,
        model=model
    )

    output = result["output"]

    # Memory
    add_memory("user", prompt)
    add_memory("assistant", output)

    # Stats
    update_stats()

    # Score
    score = viral_score(output)

    response = {
        "mode": result.get("mode"),
        "model": result.get("model"),
        "output": output,
        "viral_score": score.get("score"),
        "viral_level": score.get("level")
    }

    print("\n📦 SONUÇ:\n")
    print(json.dumps(response, indent=2, ensure_ascii=False))


def chat_mode():
    print("\n🚀 AI Content Factory CLI (CHAT MODE)")
    print("Çıkmak için: exit\n")

    while True:
        prompt = input("Prompt > ")

        if prompt.lower() == "exit":
            print("Çıkılıyor...")
            break

        run_once(
            prompt=prompt,
            mode="youtube",
            model="qwen2.5:7b"
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="AI Content Factory CLI")

    parser.add_argument("--prompt", type=str, help="Tek seferlik prompt")
    parser.add_argument("--mode", type=str, default="youtube")
    parser.add_argument("--model", type=str, default="qwen2.5:7b")
    parser.add_argument("--chat", action="store_true", help="Sohbet modu")

    args = parser.parse_args()

    # CHAT MODE
    if args.chat:
        chat_mode()

    # TEK ÇALIŞTIRMA
    elif args.prompt:
        run_once(
            prompt=args.prompt,
            mode=args.mode,
            model=args.model
        )

    else:
        print("\nKullanım:")
        print("Tek kullanım:")
        print("  python cli.py --prompt \"youtube fikir ver\"")
        print("\nChat mod:")
        print("  python cli.py --chat")
