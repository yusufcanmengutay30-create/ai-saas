import re


def optimize_prompt(prompt: str, mode: str = "youtube"):
    """
    Ham promptu viral, net ve üretilebilir hale getirir
    """

    prompt = prompt.strip()

    # 🔥 boşsa fallback
    if not prompt:
        return "viral içerik fikri üret"

    # 🔥 mode bazlı güçlendirme
    if mode == "youtube":
        return build_youtube_prompt(prompt)

    if mode == "tiktok":
        return build_tiktok_prompt(prompt)

    if mode == "affiliate":
        return build_affiliate_prompt(prompt)

    return prompt


def build_youtube_prompt(prompt: str):
    return f"""
YouTube için viral içerik üret.

Konu: {prompt}

Kurallar:
- İlk 3 saniye hook çok güçlü olsun
- İzleyiciyi merakta bırak
- Basit ve anlaşılır hikaye akışı kur
- Yüksek izlenme potansiyeli hedefle
- Clickbait ama mantıklı başlık üret

Çıktı formatı:
- Başlık
- Hook
- Senaryo
- Final CTA
"""


def build_tiktok_prompt(prompt: str):
    return f"""
TikTok viral video üret.

Konu: {prompt}

Kurallar:
- 0-2 saniye şok etkisi
- hızlı akış
- düşük dikkat süresi için optimize
- trend uyumu

Çıktı:
- Konsept
- sahne sahne akış
"""


def build_affiliate_prompt(prompt: str):
    return f"""
Affiliate satış içeriği üret.

Ürün/Konu: {prompt}

Kurallar:
- Problem → çözüm → güven → satış
- ikna odaklı yaz
- sade ve net

Çıktı:
- satış metni
"""
