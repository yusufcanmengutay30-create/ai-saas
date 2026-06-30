import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_memory(role: str, content: str):
    """
    role: user / assistant
    content: yazı
    """

    memory = load_memory()

    memory.append({
        "role": role,
        "content": content,
        "time": datetime.now().isoformat()
    })

    # çok büyümesin diye son 200 kayıt
    memory = memory[-200:]

    save_memory(memory)


def get_memory(limit: int = 20):
    memory = load_memory()
    return memory[-limit:]


def clear_memory():
    save_memory([])
