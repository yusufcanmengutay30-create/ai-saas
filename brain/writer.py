import os
from datetime import datetime

def save(content, prefix="content"):
    os.makedirs("outputs", exist_ok=True)

    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    path = os.path.join("outputs", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path
