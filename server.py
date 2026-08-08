from fastapi import FastAPI

app = FastAPI()

@app.get("/facts")
def read_facts():
    return {"facts": ["Fact1","Fact2","Fact3"]}