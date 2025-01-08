from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()

class User(Base):
    __tablename__ = 'USER'
    idx = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), primary_key=True, default=str(uuid4()))
    nickname = Column(String(30))
