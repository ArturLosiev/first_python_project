from fastapi import FastAPI
from pydantic import BaseModel

class FactRequest(BaseModel):
    new_fact: str
    author: str = "Anonymous"

app = FastAPI()

@app.get("/facts")
def read_facts():
    return {"facts": ["Fact 1", "Fact 2", "Fact 3"]}

@app.post("/add-fact")
def create_fact(payload: FactRequest):
    return {
        "status": "success",
        "received": payload.new_fact,
        "author": payload.author
    }