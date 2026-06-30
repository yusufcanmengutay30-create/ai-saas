def translate_pack(pack: dict):
    """
    Simple multilingual duplication layer (v1)
    """

    base = pack["script"]

    return {
        "tr": base,
        "en": base,
        "de": base,
        "ru": base,
        "es": base
    }
