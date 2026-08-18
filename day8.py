from fastapi import FastAPI, status
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

app = FastAPI(title="Fastapi apis")

class JobApplicationCreate(BaseModel):
    id: int
    

APPLICATION_DB: list[dict[str, Any]] = []

@app.get("/")
def home():
    return {"status":"online"}