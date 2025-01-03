from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    idx = Column(Integer, primary_key=True)
    id = Column(String(30), primary_key=True, default=str(uuid4()))
    name = Column(String(30))
    email = Column(String(30))
