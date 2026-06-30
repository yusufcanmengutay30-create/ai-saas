from brain.prompts import (
    youtube_prompt,
    tiktok_prompt,
    affiliate_prompt,
)


def handle_command(user_input: str):

    text = user_input.strip()

    # -------------------------
    # YouTube
    # -------------------------
    if text.startswith("/youtube"):

        topic = text.replace("/youtube", "").strip()

        if not topic:
            return (
                "youtube",
                "Bana bir konu yaz.\n\n"
                "Örnek:\n"
                "/youtube yapay zeka"
            )

        return (
            "youtube",
            youtube_prompt(topic)
        )

    # -------------------------
    # TikTok
    # -------------------------
    if text.startswith("/tiktok"):

        topic = text.replace("/tiktok", "").strip()

        if not topic:
            return (
                "tiktok",
                "Örnek:\n"
                "/tiktok iphone"
            )

        return (
            "tiktok",
            tiktok_prompt(topic)
        )

    # -------------------------
    # Affiliate
    # -------------------------
    if text.startswith("/affiliate"):

        topic = text.replace("/affiliate", "").strip()

        if not topic:
            return (
                "affiliate",
                "Örnek:\n"
                "/affiliate iPhone 17"
            )

        return (
            "affiliate",
            affiliate_prompt(topic)
        )

    # -------------------------
    # Yardım
    # -------------------------
    if text == "/help":

        return (
            "system",
            """
Kullanılabilir Komutlar

/youtube konu

/tiktok konu

/affiliate ürün

/help
"""
        )

    return (
        "youtube",
        user_input
    )
