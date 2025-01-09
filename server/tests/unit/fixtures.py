import pytest
from src.db import SessionLocal
from src.models.article import Article
from src.models.source import Source

@pytest.fixture
def setup_database():
    with SessionLocal() as session:
        session.query(Article).delete()
        session.query(Source).delete()
        session.commit()
        # Добавляем источник для тестов
        source = Source(
            id=1,
            name="Test Source",
            theme="Test Theme",
            url="Test url"
        )
        session.add(source)
        session.commit()
        yield session
        session.close()
