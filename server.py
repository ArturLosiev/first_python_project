from fastapi import FastAPI,Depends
from database import engine,SessionLocal
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models

class FactRequest(BaseModel):
    new_fact: str
    author: str = "Anonymous"

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/facts")
def read_facts(db: Session = Depends(get_db)):
    facts = db.query(models.FactDB).all()
    return {"facts": facts}

@app.post("/add-fact")
def create_fact(payload: FactRequest, db: Session = Depends(get_db)):
    new_record = models.FactDB(
        new_fact = payload.new_fact,
        author = payload.author
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "status": "success",
        "saved_id": new_record.id,
        "fact": new_record.new_fact,
    }