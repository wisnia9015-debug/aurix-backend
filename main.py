from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="AURIX API")

jobs = {}

class MusicRequest(BaseModel):
    prompt: str
    duration: int = 30
    style: str = "pop"

@app.post("/music/request")
def request_music(data: MusicRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "prompt": data.prompt,
        "duration": data.duration,
        "style": data.style,
        "file": None
    }
    return {"job_id": job_id}

@app.get("/music/status/{job_id}")
def music_status(job_id: str):
    return jobs.get(job_id, {"status": "ok", "service": "aurix-backend"})

@app.post("/music/complete/{job_id}")
def complete_job(job_id: str, file_url: str):
    if job_id in jobs:
        jobs[job_id]["status"] = "done"
        jobs[job_id]["file"] = file_url
        return {"ok": True}
    return {"error": "job not found"}
