"""
модели БД
"""
from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_source = Column(Integer, ForeignKey("source.id"))
    content = Column(String)
    url = Column(String, ForeignKey("theme.name"))
    theme_name = Column(String)

    source = relationship("Source", back_populates="articles")


class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    theme = Column(String)
    url = Column(String)

    articles = relationship("Article", back_populates="source")


class Theme(Base):
    __tablename__ = "theme"
    name = Column(String, primary_key=True)
