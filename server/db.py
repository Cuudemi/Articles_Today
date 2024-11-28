from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "postgresql+psycopg2://postgres:1@localhost/ArticlesToday"
engine = create_engine(database_url, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
