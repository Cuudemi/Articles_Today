from src.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    theme = Column(String)
    url = Column(String)