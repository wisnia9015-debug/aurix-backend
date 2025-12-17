from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "ok", "service": "aurix-backend"}

@app.post("/generate")
def generate(data: Prompt):
    try:
        response = client.chat.completions.create(
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
