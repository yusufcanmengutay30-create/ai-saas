import re


def viral_score(text: str):
    """
    Basit ama genişletilebilir viral skor sistemi
    """

    score = 0

    # 🔥 Uzunluk etkisi
    length = len(text)

    if length > 500:
        score += 30
    elif length > 200:
        score += 20
    else:
        score += 10

    # 🔥 Hook / dikkat çekme kelimeleri
    hooks = ["şok", "inanılmaz", "acil", "para", "bedava", "viral", "kesin", "yeni"]

    for h in hooks:
        if h in text.lower():
            score += 10

    # 🔥 Emoji kullanımı
    emoji_count = len(re.findall(r"[^\w\s,]", text))
    if emoji_count > 5:
        score += 20
    elif emoji_count > 2:
        score += 10

    # 🔥 Yapı kontrolü (madde varsa iyi içerik)
    if "-" in text or "•" in text:
        score += 10

    # 🔥 Final seviyeler
    if score >= 70:
        level = "VIRAL 🔥"
    elif score >= 40:
        level = "GOOD 👍"
    else:
        level = "LOW ⚠️"

    return {
        "score": score,
        "level": level
    }
