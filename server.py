from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine,SessionLocal
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models

class FactRequest(BaseModel):
    new_fact: str
    author: str = "Anonymous"

app = FastAPI(
    title="Artur's Fact API",
    description="A containerized microservice collecting and storing facts.",
    version="1.0.0"
)

# Enable CORS so any frontend app or web browser can query your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In strict production, replace "*" with specific domain URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Artur's Fact API!",
        "documentation": "/docs",
        "endpoints": {
            "all_facts": "/facts",
            "fact_by_id": "/facts/{id}",
            "add_fact": "/add-fact"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}

@app.get("/facts")
def read_facts(db: Session = Depends(get_db)):
    facts = db.query(models.FactDB).all()
    return {"facts": facts}

@app.get("/facts/{fact_id}")
def read_fact(fact_id: int, db: Session = Depends(get_db)):
    fact = db.query(models.FactDB).filter(models.FactDB.id == fact_id).first()
    if fact is None:
        raise HTTPException(status_code=404, detail="Fact not found")
    return {"fact": fact.new_fact}


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