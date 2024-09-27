from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ErrorModel(Base):
    __tablename__ = "errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    text = Column(String(1024), nullable=False)
    date = Column(DateTime, nullable=False)
    user_name = Column(String(64))
    level = Column(String(10), nullable=False)
    