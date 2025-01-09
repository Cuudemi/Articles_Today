from src.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_source = Column(Integer, ForeignKey("source.id"))
    content = Column(String)
    url = Column(String)
    theme_name = Column(String)