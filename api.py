from fastapi import FastAPI
from pydantic import BaseModel
import time

from brain.engine import generate
from brain.logger import update_stats
from brain.memory import add_memory
from brain.scorer import viral_score
from brain.content_builder import build_viral_package
from brain.translator import translate_pack
from auth import login

app = FastAPI(
    title="AI Content Factory API",
    version="11.0"
)


class GenerateRequest(BaseModel):
    user: str
    password: str
    prompt: str
    mode: str = "youtube"
    model: str = "qwen2.5:7b"


class GenerateResponse(BaseModel):
    success: bool
    user: str
    mode: str
    model: str
    time: float
    viral_score: int
    viral_level: str
    output: str
    content: dict
    translations: dict


@app.get("/")
def root():
    return {
        "status": "online",
        "name": "AI Content Factory",
        "version": "11.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/generate", response_model=GenerateResponse)
def generate_api(data: GenerateRequest):

    if not login(data.user, data.password):
        return {
            "success": False,
            "user": data.user,
            "mode": data.mode,
            "model": data.model,
            "time": 0.0,
            "viral_score": 0,
            "viral_level": "none",
            "output": "Kullanıcı adı veya şifre hatalı.",
            "content": {},
            "translations": {}
        }

    start = time.time()

    result = generate(
        prompt=data.prompt,
        mode=data.mode,
        model=data.model
    )

    elapsed = round(time.time() - start, 2)

    output = result["output"]

    # memory + stats
    add_memory("user", data.prompt)
    add_memory("assistant", output)
    update_stats()

    # viral scoring
    score = viral_score(output)

    # 🔥 NEW: viral content pack
    viral_pack = build_viral_package(output)

    # 🌍 NEW: multi-language layer
    translations = translate_pack(viral_pack)

    return {
        "success": True,
        "user": data.user,
        "mode": result["mode"],
        "model": result["model"],
        "time": elapsed,
        "viral_score": score["score"],
        "viral_level": score["level"],
        "output": output,
        "content": viral_pack,
        "translations": translations
    }
