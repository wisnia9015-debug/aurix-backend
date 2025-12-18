from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("AURIX_API_KEY")

app = FastAPI(title="AURIX AI API")

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "ok", "service": "aurix-backend"}

@app.post("/generate")
def generate(data: Prompt, x_api_key: str = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": data.prompt}
            ]
        )
        return {
            "result": response.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
