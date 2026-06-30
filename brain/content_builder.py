def build_viral_package(text: str):
    """
    Raw AI output → viral content pack
    """

    title = f"🔥 {text[:60].strip()}..."

    hashtags = [
        "#viral",
        "#shorts",
        "#trending",
        "#ai",
        "#content"
    ]

    script = f"""
Hook: Stop scrolling!

{text}

Call to action: Follow for more!
"""

    thumbnail_prompt = f"""
Create a high CTR YouTube thumbnail:
- Bold emotion
- High contrast
- Focus on: {text[:80]}
- Style: MrBeast level clickbait
"""

    caption = f"{title} 🚀\n\n{' '.join(hashtags)}"

    return {
        "title": title,
        "hashtags": hashtags,
        "script": script,
        "thumbnail_prompt": thumbnail_prompt,
        "caption": caption
    }
