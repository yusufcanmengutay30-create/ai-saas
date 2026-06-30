import json
import os
from datetime import datetime

LOG_FILE = "stats.json"


def load_stats():
    if not os.path.exists(LOG_FILE):
        return {
            "total_requests": 0,
            "created_at": datetime.now().isoformat()
        }

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_stats(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_stats():
    stats = load_stats()

    stats["total_requests"] += 1
    stats["last_update"] = datetime.now().isoformat()

    save_stats(stats)
