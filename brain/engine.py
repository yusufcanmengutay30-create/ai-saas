import time
from brain.prompt_optimizer import optimize_prompt


def generate(prompt: str, mode: str = "youtube", model: str = "qwen2.5:7b"):
    """
    TEK AI MOTORU (CLI + API + WEB ortak)
    """

    start = time.time()

    # 🧠 PROMPT OPTIMIZER KATMANI
    optimized_prompt = optimize_prompt(prompt, mode)

    # 🔥 OUTPUT ÜRETİMİ
    output = build_output(optimized_prompt, mode)

    elapsed = round(time.time() - start, 2)

    return {
        "mode": mode,
        "model": model,
        "prompt": prompt,
        "optimized_prompt": optimized_prompt,
        "output": output,
        "time": elapsed
    }


def build_output(prompt: str, mode: str):

    if mode == "youtube":
        return f"""
🎬 YOUTUBE VİRAL İÇERİK

Konu: {prompt}

🔥 HOOK:
İlk 3 saniyede izleyiciyi yakala (soru veya şok bilgi)

📖 AKIŞ:
- Problem ortaya koy
- Gerilim oluştur
- Çözümü adım adım ver

🎯 FİNAL:
Güçlü CTA (abone ol / yorum bırak)
"""

    elif mode == "tiktok":
        return f"""
📱 TIKTOK VİRAL İÇERİK

Konu: {prompt}

0-2s: Şok giriş
2-8s: hızlı gelişim
8-15s: beklenmedik twist

Amaç: tekrar izlenme döngüsü
"""

    elif mode == "affiliate":
        return f"""
💰 AFFILIATE SATIŞ İÇERİĞİ

Konu: {prompt}

- Problem anlat
- Çözüm sun
- Güven oluştur
- Satışa yönlendir
"""

    else:
        return f"OUTPUT: {prompt}"
