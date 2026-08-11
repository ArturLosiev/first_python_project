from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FactDB(Base):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True,index=True)
    new_fact = Column(String)
    author = Column(String)